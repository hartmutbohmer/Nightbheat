# Nightbheat

Personal learnings on REM-respiration bimodality as a candidate digital biomarker of autonomic sleep stability, framed for six different audiences.

## What this repository is

A multi-angle exploration of a single observation: across 3.5 years of personal Garmin Connect data, REM-stage respiration in one subject (the author) shows a stable bimodal distribution in approximately 90% of REM segments. Following a low-cost, non-pharmacological intervention applied in mid-December 2025, the bimodal fraction collapsed to 0% and has remained so for four months. The collapse was accompanied by a coherent shift in two independent autonomic markers (resting heart rate distribution and Garmin's calm-sleep classification).

The observation is single-subject. It is not, on its own, evidence of anything beyond what a careful n=1 record can establish. The repository exists because the underlying detection methodology is fully specified, computationally cheap, and falsifiable at population scale using data wearable platforms already collect — and because the asymmetry between the cost of running that test (low) and the potential public-health relevance of the result (non-zero) makes the case worth committing to writing.

Each document in the repository frames the same underlying observation for a different audience: a wearable platform's product team, a physiological researcher, an occupational-health pilot funder, a medical-publication audience, and a public-health context. The more angles, the more coherent the intent. None of the framings is a substitute for the population-scale test they all converge on.

## What this repository is not

Not a clinical claim. Not a diagnostic claim. Not a therapeutic recommendation. Not a treatment protocol. Not a substitute for medical advice. Not a commercial pitch — the detection methodology is open and the synthetic validation datasets are available on request. Not a finished body of work — every document in this repository is a working draft inviting engagement, replication, criticism, and improvement.

## Context: how this work started

The research direction originates from the 2019 Nightbheat presentation at the GAP Medical innovation hub in Pretoria, where the brief identified by the panel was reduction of dementia risk, motivated in part by the higher dementia prevalence observed on the Highveld. The author's subsequent personal post-COVID symptoms from February 2020 onward provided an extended single-subject record against which to examine sleep-autonomic markers. The repository documents what that record has produced in the years since.

A May 2026 review in *Science* by Maiken Nedergaard ("The oscillatory biology of sleep: Linkage to dementia", DOI: 10.1126/science.aeg2276) proposes that disrupted synchronisation of sleep-dependent brain rhythms impairs glymphatic clearance of amyloid-beta and tau, and explicitly identifies heart rate variability — already measurable on consumer wearables — as a candidate noninvasive biomarker for this pathway. This recent framing provides independent theoretical context for examining HRV and respiration-cardiac coupling as population-scale screening targets. The bimodality phenotype documented in this repository may represent one detectable signature of disrupted autonomic synchronisation during sleep, testable against direct glymphatic measurement in appropriately equipped studies. See `glymphatic_clearance_context.txt` for the supporting references and how they relate to the framings in this repository.

This is context, not a mechanism claim. The repository does not assert that the intervention examined here improves glymphatic clearance. It asserts that the bimodality metric is cheap to compute, falsifiable at population scale, and worth running against the Nedergaard framework once direct instrumentation becomes available.

## The seven framings

1. **garmin-bimodality-histogram.skill** — *the bimodality test.* The detection methodology as a self-contained skill bundle: a SKILL.md specification plus three reference scripts (extract_rem_samples.py, make_histogram.py, batch_extract.py). The methodology is the same one specified in Phase A of the Garmin Health submission: per-REM-segment Gaussian Mixture Model fitting with k=1 versus k=2 comparison via Bayesian Information Criterion, with explicit false-positive control against synthetic unimodal data. This is the technical core that all other framings reference.

2. **garmin-bimodality-histogram_user-manual.docx** — *the bimodality test user manual.* Companion user-facing documentation. Explains how to extract Garmin Connect sleep-timeline screenshots, run the scoring methodology on them, and interpret the per-night Bimodality Index. Intended for replication attempts by other researchers or by Garmin users curious about whether their own data shows the phenotype.

3. **Garmin_health_2026_submission_v21.pdf** — *the Garmin Health competition submission.* The base document from which the other framings are derived. Submitted to the 2026 Garmin Health Awards (Health Care & Research category). Documents the full n=1 record (figures, scoring tables, multi-year baseline stability, bradycardia resolution as co-marker) and specifies the Phase A population-scale detection pipeline in implementation-ready detail. Includes the appendix detailing the per-period scoring data and the synthetic validation datasets that anchor false-positive control. The most complete single-document treatment of the methodology and the data.

4. **preprint_v1 (1).docx** — *the medical preprint (HRV versus bimodality).* A medRxiv-formatted preprint framing the work as a case report. Structured for the medical-publication audience: abstract, methods, results, discussion, declarations, references. The primary scientific contribution beyond the Garmin submission is the within-subject effect-size comparison between two interventions on the same primary metrics — HRV pre-sleep biofeedback (September 2023 – November 2024, modest effect, no bimodality change) versus mechanical stochastic-resonance coupling (mid-December 2025 onwards, ~90% → 0% bimodality collapse and ~25% RMS reduction). The asymmetry between these two interventions is the most informative single comparison in the dataset about which physiological pathway dominates in this subject.

5. **Eskom_pilot_proposal_v1.docx** — *the occupational-pilot proposal.* A formal pilot-study proposal framing the methodology for an occupational-health audience, specifically Eskom (the South African national electricity utility, whose shift-working power-station staff are a natural cohort for sleep-autonomic monitoring). Documents protocol design, ethics framework, governance, indicative budget (ZAR 465,000 – 700,000), 9–12 month timeline, and worker-protection considerations. Designed as a deployable Phase A field test rather than a thought experiment.

6. **REM_bimodality_note_for_Dr_Thomas.pdf** — *note to a foundational researcher.* A short note to Dr Henry Hong-Chun Thomas, a foundational researcher in respiratory-pattern analysis during sleep. Frames the n=1 observation in the physiological-mechanism language his published work uses, and asks the specific question his prior research positions him to answer: whether the observed bimodal phenotype is consistent with the posture-dependent respiratory asymmetries he has characterised elsewhere, or whether it suggests a different underlying mechanism.

7. **BP_public_health_framing_v1.docx** — *the public-health framing.* Combines the Garmin Health submission's biomarker framework with the public-health context of the Gauteng Department of Health's May 2026 report that 26,088 of 69,125 new hypertension diagnoses in 2025/26 were in adults aged 18–44 — a daily rate of approximately 71 new under-45 diagnoses in one province. Adds a supporting observation from the n=1 record (Garmin calm-sleep night counts increased from 2 in the matched March–May 2025 baseline window to 15 in the same window in 2026, a ≈7.5× increase) and explicitly distinguishes what is claimed from what is not: calm-sleep counts are a proprietary aggregate, not a direct blood pressure measurement, and the chain from autonomic-sleep markers to measured BP outcome must be closed by formal study.

   Proposes a three-step pathway — Phase A bimodality detection (≈one analyst-week, < USD 5,000), cross-sectional cohort prevalence study (≈6 months, ZAR 5–10M), and intervention RCT with measured BP outcomes (12–18 months, ZAR 30–60M) — each independently abortable on a negative prior-step result. The case is that the cost asymmetry (the cheapest step is roughly four orders of magnitude cheaper than the most expensive) justifies running Step 1 even at moderate prior probability.

   The framing is the broadest of the seven and the one with the longest inference chain. It is included because adding angles strengthens coherence: the more independent framings converge on the same population-scale test, the stronger the case for running it.

## What ties the framings together

All seven documents converge on the same single ask: run a binary, falsifiable analytical pilot on existing wearable data using the specified GMM detection pipeline, and either confirm that REM-respiration bimodality is a real population-scale phenotype or rule it out. The framings differ in audience and in which downstream pathway they sketch beyond that test, but the test itself is shared, fully specified, and computationally cheap. A negative result is informative and worth publishing. A positive result opens distinct downstream possibilities — product, clinical, occupational, public-health — that the individual framings then explore.

## Next instrumentation step

The largest single gap in the current evidence chain is the move from wrist-derived screenshot scoring to direct, continuous measurement of HRV and respiration-cardiac coupling. The priority going forward is pillow-integrated instrumentation — ballistocardiography, piezo, or accelerometer-derived respiration with synchronised cardiac timing — to characterise the synchronisation fingerprint associated with the bimodality phenotype and its response to intervention. Pillow form factor is chosen because it removes the wrist-strap compliance problem at scale and because it places the sensor adjacent to the head, where mechanical coupling to the intervention is most direct. Closing this instrumentation gap would provide the basis for testing the proposed signature against direct glymphatic measurement in studies equipped to do so, consistent with the Nedergaard framework cited above.

## Status and limitations

Single-subject. Single-investigator. Subject–experimenter overlap. Screenshot-based scoring rather than raw-sample GMM fitting. No formal washout completed. No measured blood pressure data in the n=1 record. No cross-subject replication. No direct glymphatic measurement. Each document declares its own limitations section; read those.

The repository exists not because the case is closed but because it is unusually well-specified for an n=1 observation, and because the population-scale test that would settle it is unusually cheap to run. The asymmetry is the argument.

## Contact and contribution

The author is an electronic product design engineer based in Pretoria, South Africa, with personal post-COVID symptoms originating in February 2020 that motivated the original research direction. No commercial intent. No proprietary stake in any specific intervention. The detection methodology is open; the synthetic validation datasets are available on request.

Questions, requests for methodology detail, requests for the synthetic validation datasets, replication attempts, criticism, or expressions of interest in collaboration on any of the proposed studies are welcomed. The repository is offered in good faith as a starting point for conversation, not as a settled position.
