# Unit 1 — Specifications (PROPOSAL — templates every unit; needs Greg's ratification)

Derived from `docs/OVERHAUL_FRAMEWORK.md` §9 (specifications grading) + the analytic rubric
rows of the source HWs (hw1, hw2, hw3). **No prior worked spec existed — this is the proposed
scheme.** The reconciliation rule:

- **Each former rubric row → one met/not-met *specification*.** No partial points within a
  spec — it is met or not.
- **Specifications group into three bundles:** **Correctness**, **Interpretation**, **Process**.
- **Load-bearing specs are MUST-MEET** (a single miss sends the bundle to REVISE). **Independent
  specs** pass with a **miss-threshold** (the bundle tolerates up to *k* missed independent
  specs, stated per bundle).
- **Correctness is the CORE / GATEWAY bundle:** the unit cannot PASS unless Correctness passes
  (you cannot pass a modeling unit without a working model). This *is* the only residue of the
  old component weights — **per-HW weights (55/35/10, 60/40, …) are moot and not carried.**
- **PASS / REVISE-and-RESUBMIT:** any unmet bundle gets **one** revise-and-resubmit in the
  posted window. Unit PASS = Correctness ∧ Interpretation ∧ Process all PASS.

## Bundle 1 — Correctness  ·  CORE / GATEWAY  (autograded by `test_hw.py`)

PASS rule: **every MUST-MEET spec met, and ≤ 1 missed among the independent specs.**

| Spec | From | Test | Type |
|------|------|------|------|
| **A1** scalar closed-form `w0,w1` (rel 1e-3) | hw1 | `test_scalar_closed_form` | MUST-MEET (foundation) |
| **A2** scalar residuals ⟂ `1`,`x` (normal eqns) | hw1 | `test_scalar_normal_equations` | independent |
| **A3** scalar beats mean-baseline (floor-AND-guard) | hw1 | `test_scalar_beats_baseline` | MUST-MEET |
| **B1** matrix order-1 **==** scalar fit @2012 (through-line) | hw2 | `test_matrix_order1_matches_scalar` | MUST-MEET (ties A↔B) |
| **B2** matrix residuals ⟂ design columns | hw2 | `test_matrix_normal_equations` | independent |
| **C1** `scale` maps to [0,1] | hw3 | `test_scale_is_unit_range` | independent |
| **C2** `scale` is affine-invertible | hw3 | `test_scale_is_affine_recoverable` | independent |
| **C3** design matrix shape + intercept column | hw3 | `test_design_matrix_shape_and_intercept` | MUST-MEET (downstream depends on it) |
| **C4** order-3 fit-quality floor (scaled RMSE ≤ 0.3) | hw3 | `test_fit_quality_floor_scaled` | MUST-MEET (capability) |
| **C5** CV return contract (length-P, finite, ≥0) | hw3 | `test_cv_returns_per_order_losses` | MUST-MEET (CV must run) |
| **C6** LOOCV runs | hw3 | `test_loocv_runs` | independent |
| **C7** CV penalizes overfitting (floor-AND-guard) | hw3 | `test_cv_penalizes_overfitting` | MUST-MEET (the O4 outcome) |

7 MUST-MEET + 5 independent (miss-threshold ≤ 1).

## Bundle 2 — Interpretation  (rubric; LLM-pre-grade + human-confirm)

The I1–I3 markdown answers, each scored **Claim / Evidence / Reasoning / Limits** (0–3).

| Spec | Prompt | PASS when… |
|------|--------|-----------|
| **I1** | CV order choice in bias–variance terms | ≥2 on every CERL dimension |
| **I2** | overfitting from the train/val + CV curves | ≥2 on every CERL dimension |
| **I3** | when CV misleads (small N / leakage / non-i.i.d.) | ≥2 on every CERL dimension |

Bundle PASS = all three specs met (no miss-threshold — only three, each is load-bearing for O5).
An LLM may draft per-dimension scores + one-line reasons; **a human confirms and is final.**

## Bundle 3 — Process

| Spec | PASS when… |
|------|-----------|
| **P1** seeded CV shuffle (`default_rng(0)`) | reproducible |
| **P2** `import hw` does no work (cheap) | measured < ~0.1 s |
| **P3** figures labeled; notebook/`.qmd` runs clean | renders top-to-bottom |

Bundle PASS = all three (binary process checks).

## Objective → spec → bundle coverage (nothing dropped in the merge)

| Source objective | Specs | Bundle |
|------------------|-------|--------|
| hw1: scalar least squares | A1, A2, A3 | Correctness |
| hw2: matrix normal equation (+ identities **applied**, derived in U2b) | B1, B2 | Correctness |
| hw3: scaling | C1, C2 | Correctness |
| hw3: design matrix / polynomial features | C3 | Correctness |
| hw3: fit capability | C4 | Correctness |
| hw3: cross-validation | C5, C6, C7 | Correctness |
| hw1/hw3: interpret fit / CV (bias–variance, overfitting, limits) | I1–I3 | Interpretation |
| all: reproducibility & communication | P1–P3 | Process |

**Every source objective maps to ≥1 spec in a bundle; no objective is dropped.** The hw2
matrix-calculus *derivation* is intentionally **not** a Correctness spec here — it is applied
(B1/B2) and its general derivation is assessed in **U2b** (forward-reference preserved).
