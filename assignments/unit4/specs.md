# Unit 4 — Specifications (Unit 1 template; mixed Correctness: autograded code + human derivation)

Same template as Unit 1: rows → met/not-met specs; bundles Correctness (core/gateway),
Interpretation, Process; MUST-MEET vs independent (threshold ≤ 1); pass / revise-resubmit.

> **TEMPLATE-FIT NOTE — mixed Correctness (clean, as U2a/U3/U5).** Correctness holds autograded
> specs (hw10 predictive variance, hw11 conjugacy — relationship/property/floor-AND-guard, no
> 100-element array pins) and one human per-step derivation spec (hw12 Inverse-Gamma). Each is one
> binary spec; bundle structure unchanged; only *Verified by* differs.

## Bundle 1 — Correctness · CORE / GATEWAY

PASS rule: **every MUST-MEET met, and ≤ 1 missed among the independent specs.**

| Spec | From | Verified by | Test / step | Type |
|------|------|-------------|-------------|------|
| **A1** `cov_w = σ̂²(XᵀX)⁻¹`, symmetric PSD | hw10 | autograder | `test_cov_w_definition_psd` | MUST-MEET |
| **A2** `predictive_variance = diag(X cov_w Xᵀ)`, ≥0 | hw10 | autograder | `test_predictive_variance_matches_cov_w` | MUST-MEET |
| **A3** variance larger in the data gap (floor-AND-guard) | hw10 | autograder | `test_variance_larger_in_gap` | MUST-MEET |
| **B1** Beta function `B(a,b)=Γ(a)Γ(b)/Γ(a+b)` | hw11 | autograder | `test_B_function` | independent |
| **B2** `Beta(r;a,b)` integrates to 1 | hw11 | autograder | `test_beta_normalizes` | independent |
| **B3** posterior conjugacy `Beta(a+y_N, b+N−y_N)` | hw11 | autograder | `test_posterior_is_conjugate_beta` | MUST-MEET (the result) |
| **B4** posterior mean `(a+y_N)/(a+b+N)` | hw11 | autograder | `test_posterior_mean_is_conjugate` | independent |
| **B5** marginal likelihood & P(win) are probabilities | hw11 | autograder | `test_marginal_likelihood_and_prob_win...` | independent |
| **D1** Inverse-Gamma conjugacy `α'=α+D/2, β'=β+½‖t−Xw‖²` | hw12 | human per-step | D1 ≥ Proficient | MUST-MEET |

5 MUST-MEET (A1, A2, A3, B3, D1) + 4 independent (B1, B2, B4, B5); threshold ≤ 1.

## Bundle 2 — Interpretation (CERL)

| Spec | Prompt | PASS when… |
|------|--------|-----------|
| **I1** | error bars / where the model is uncertain | ≥2 every CERL dim |
| **I2** | prior sensitivity as N grows; marginal likelihood | ≥2 every CERL dim |
| **I3** | what conjugacy buys and where it stops | ≥2 every CERL dim |

## Bundle 3 — Process

| Spec | PASS when… |
|------|-----------|
| **P1** `import hw` cheap | < ~0.2 s |
| **P2** `.qmd` renders clean (Typst); figures labeled | met |

## Objective → spec → bundle coverage (nothing dropped)

| Source objective | Specs | Bundle |
|------------------|-------|--------|
| hw10 cov_w + predictive variance | A1, A2, A3 | Correctness |
| hw11 Beta/posterior/marginal/P(win) | B1–B5 | Correctness |
| hw12 Inverse-Gamma conjugacy | D1 | Correctness |
| error bars / prior sensitivity / conjugacy | I1–I3 | Interpretation |
| reproducibility & communication | P1, P2 | Process |

**Every source objective maps to ≥1 spec.** Through-lines: B ↔ U2b Beta moments; C ↔ U1 Olympic
noise variance; both are conjugate updates (prior family in → same family out).
