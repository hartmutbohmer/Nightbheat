#!/usr/bin/env python3
"""
Overnight breathing/coupling tone with stepped descending frequency band.

Inner cycle (20s): single continuous tone glides from BASE up to PEAK and back,
   using a cos^2 rise / flat plateau / cos^2 fall shape. Amplitude tracks
   frequency to compensate for speaker frequency response.

Outer schedule: every 9 minutes, the (BASE, PEAK) pair drops by 5 Hz.
   Starts at (95, 100), ends at (50, 55), then the script stops.

Phase is continuously integrated across both timescales, so there are no
discontinuities at any boundary.

Stop early with Ctrl+C.
"""
import numpy as np
import sounddevice as sd
import sys

# -------- Parameters --------
SAMPLE_RATE   = 44100      # Hz

# Outer schedule
START_PEAK    = 100.0      # Hz, highest frequency of step 1
START_BASE    = 95.0       # Hz, lowest frequency of step 1
STEP_HZ       = 5.0        # Hz drop per step
STEP_SEC      = 9 * 60     # 9 minutes per step
NUM_STEPS     = 10         # 100/95 down to 55/50

# Inner cycle (within each step)
CYCLE_SEC     = 20.0       # full inner cycle period
DUTY          = 0.50       # fraction of cycle gliding up (10s up / 10s at base)
RISE_FRAC     = 0.25       # cos^2 rise fraction of on-window
PLATEAU_FRAC  = 0.50       # plateau fraction of on-window
FALL_FRAC     = 0.25       # cos^2 fall fraction of on-window

# Amplitude compensation: louder at low freq, quieter at high freq
BASE_AMP      = 0.60       # amplitude at the LOWER frequency of each step
PEAK_AMP      = 0.30       # amplitude at the UPPER frequency of each step

BLOCK_SEC     = 0.05       # streaming block size (50 ms - robust on Windows)
# ----------------------------

block_size = int(SAMPLE_RATE * BLOCK_SEC)

# Inner-cycle envelope boundaries (seconds within the 20s cycle)
on_window   = DUTY * CYCLE_SEC
rise_end    = RISE_FRAC * on_window
plateau_end = rise_end + PLATEAU_FRAC * on_window
fall_end    = on_window

# Snap step length to a whole number of inner cycles so step boundaries
# always land exactly when the inner glide is at its BASE state.
cycles_per_step = round(STEP_SEC / CYCLE_SEC)
step_seconds    = cycles_per_step * CYCLE_SEC
total_seconds   = NUM_STEPS * step_seconds

def shape_factor(t_in_cycle):
    """0 at BASE state, 1 at PEAK state, cos^2 rise / plateau / cos^2 fall."""
    s = np.zeros_like(t_in_cycle)

    rise_mask = t_in_cycle < rise_end
    if rise_end > 0:
        x = t_in_cycle[rise_mask] / rise_end
        s[rise_mask] = np.sin(0.5 * np.pi * x) ** 2

    plat_mask = (t_in_cycle >= rise_end) & (t_in_cycle < plateau_end)
    s[plat_mask] = 1.0

    fall_mask = (t_in_cycle >= plateau_end) & (t_in_cycle < fall_end)
    fall_len = fall_end - plateau_end
    if fall_len > 0:
        x = (t_in_cycle[fall_mask] - plateau_end) / fall_len
        s[fall_mask] = np.cos(0.5 * np.pi * x) ** 2

    return s

def step_frequencies(t_global):
    """
    Returns (base_freq, peak_freq) arrays for each sample time.
    Step index = floor(t_global / step_seconds), clamped to NUM_STEPS-1.
    Step k uses BASE = START_BASE - k*STEP_HZ, PEAK = START_PEAK - k*STEP_HZ.
    """
    step_idx = np.floor(t_global / step_seconds).astype(np.int64)
    np.clip(step_idx, 0, NUM_STEPS - 1, out=step_idx)
    base = START_BASE - step_idx * STEP_HZ
    peak = START_PEAK - step_idx * STEP_HZ
    return base, peak

# Continuous phase accumulator
phase = 0.0
sample_index = 0
dt = 1.0 / SAMPLE_RATE
total_samples = int(total_seconds * SAMPLE_RATE)
finished = False

def callback(outdata, frames, time_info, status):
    global phase, sample_index, finished
    if status:
        print(status, file=sys.stderr)

    n = np.arange(sample_index, sample_index + frames)
    t_global   = n * dt
    t_in_cycle = np.mod(t_global, CYCLE_SEC)

    s = shape_factor(t_in_cycle)
    base_f, peak_f = step_frequencies(t_global)

    f_inst = base_f + (peak_f - base_f) * s
    a_inst = BASE_AMP + (PEAK_AMP - BASE_AMP) * s

    # Silence any samples beyond the scheduled end
    past_end = n >= total_samples
    if past_end.any():
        a_inst = a_inst.copy()
        a_inst[past_end] = 0.0
        if past_end.all():
            finished = True

    dphase = 2.0 * np.pi * f_inst * dt
    phase_array = phase + np.cumsum(dphase)
    phase = phase_array[-1] % (2.0 * np.pi)

    signal = a_inst * np.sin(phase_array)
    np.clip(signal, -1.0, 1.0, out=signal)

    outdata[:, 0] = signal.astype(np.float32)
    sample_index += frames

def main():
    print("Stepped overnight tone schedule:")
    print(f"  Step length: {step_seconds/60:.1f} min ({cycles_per_step} inner cycles)")
    print(f"  Total run:   {total_seconds/60:.1f} min")
    print(f"  Amplitudes:  base {BASE_AMP}, peak {PEAK_AMP}")
    print()
    print("  Step  |  Start min  |  Base Hz  |  Peak Hz")
    print("  ------+-------------+-----------+----------")
    for k in range(NUM_STEPS):
        print(f"  {k+1:>4d}  |  {k*step_seconds/60:>9.1f}  |  {START_BASE - k*STEP_HZ:>7.1f}  |  {START_PEAK - k*STEP_HZ:>7.1f}")
    print()
    print("Press Ctrl+C to stop early.\n")

    try:
        with sd.OutputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=block_size,
            callback=callback,
        ):
            while not finished:
                sd.sleep(500)
        print("Schedule complete. Stopped.")
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    main()