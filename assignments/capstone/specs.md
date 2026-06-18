# Capstone — Specifications (ratified template, ADAPTED for an OPEN task)

> **TEMPLATE ADAPTATION (directed): open task, no reference answer.** Because the Capstone has no
> source HW and no answer key, the **Correctness/gateway bundle assesses METHOD VALIDITY + INTERNAL
> CONSISTENCY + RUNNABLE CODE**, not a pinned value — every spec passes for any sound Bayesian
> approach and fails a degenerate one (mutation-verified). Interpretation is CERL on the results
> **and the ethics report**; Process as usual. Same bundle structure (gateway / MUST-MEET /
> independent / threshold ≤1 / revise) — only what Correctness *checks* changed, as directed for
> the open build.

## Bundle 1 — Correctness · CORE / GATEWAY  (method validity, not a pinned answer)

PASS rule: **every MUST-MEET met, and ≤ 1 missed among the independent specs.**

| Spec | Kind | Test | Type |
|------|------|------|------|
| **R1** code runs; `predict`/`predictive_std` return finite, correctly-shaped output | runnable | `test_runs_and_shapes` | MUST-MEET |
| **V1** the model fits — beats the constant-mean baseline | method validity | `test_model_fits_beats_baseline` | MUST-MEET |
| **V2** predictive std ≥ 0; posterior covariance symmetric PSD | method validity | `test_uncertainty_nonneg_and_cov_psd` | MUST-MEET |
| **C1** predictive std grows under **extrapolation** vs the dense-data region | internal consistency | `test_uncertainty_grows_off_data` | MUST-MEET (the point of the task) |
| **C2** predictive std ≥ the model's own noise floor | internal consistency | `test_predictive_std_exceeds_noise_floor` | independent |

4 MUST-MEET (R1, V1, V2, C1) + 1 independent (C2); threshold ≤ 1.

> **C1 is extrapolation-only.** Growth in the *interior gap* [0.5, 2.0] is method-dependent (a
> smooth model may interpolate a narrow gap confidently), so it is **not a floor** — it moved to
> **Interpretation (I1)**, where students must describe and *justify* their method's gap behaviour.
> Extrapolation growth, by contrast, is shared by every valid parameter-uncertainty method.

## Bundle 2 — Interpretation  (CERL + ethics; LLM-pre-grade + human-confirm)

| Spec | Prompt | PASS when… |
|------|--------|-----------|
| **I1** | results: fit + where/why uncertainty is large/small + real limits + **describe the method's predictive uncertainty in the [0.5, 2.0] gap and justify why it does or does not grow there** | ≥2 on every CERL dimension |
| **I2** | ethics/impact of acting on the (over-confident) predictions + one safeguard | ≥2 on every CERL dimension |

Bundle PASS = both (each load-bearing for O4). Human confirms; the ethics note is required, not optional.

## Bundle 3 — Process

| Spec | PASS when… |
|------|-----------|
| **P1** any RNG seeded; `import hw` cheap | reproducible |
| **P2** `.qmd` renders clean (Typst); the ±band figure labeled | met |

## Objective → spec → bundle coverage

| Objective | Specs | Bundle |
|-----------|-------|--------|
| O1 fit a model | V1 | Correctness |
| O2 quantify uncertainty (valid method) | V2, C1, C2 | Correctness |
| O3 runnable/reproducible to the contract | R1, P1 | Correctness/Process |
| O4 interpret results + ethics | I1, I2 | Interpretation |

**Every objective maps to a spec.** Method-validity specs are mutation-checked: a constant-σ
submission fails C1; a no-fit (constant-mean) submission fails V1.
