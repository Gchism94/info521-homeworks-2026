# Unit 3 — Specifications (Unit 1 template; mixed Correctness: autograded code + human derivations)

Same template as Unit 1: rows → met/not-met specs; bundles Correctness (core/gateway),
Interpretation, Process; MUST-MEET vs independent (threshold ≤ 1); pass / revise-resubmit.

> **TEMPLATE-FIT NOTE — mixed Correctness (clean, same as U2a/U5).** Correctness holds autograded
> stochastic specs (hw6 MC, hw17 π — distributional/convergence/floor-AND-guard, seeded, never
> pinned draws) and human per-step derivation specs (D1 analytic expectation, D2 the π formulas).
> Each is one binary spec; bundle structure unchanged; only the *Verified by* column differs.

## Bundle 1 — Correctness · CORE / GATEWAY

PASS rule: **every MUST-MEET met, and ≤ 1 missed among the independent specs.**

| Spec | From | Verified by | Test / step | Type |
|------|------|-------------|-------------|------|
| **A1** `f` matches the polynomial | hw6 | autograder | `test_f_values` | independent |
| **A2** MC recovers `E[f(X)]≈18.61` + convergence floor-AND-guard | hw6 | autograder | `test_mc_recovers...`, `test_mc_convergence_improves` | MUST-MEET |
| **B1** `number_of_orthants = 2ⁿ` | hw17 | autograder | `test_number_of_orthants` | independent |
| **B2** circle (2-D) converges | hw17 | autograder | `test_circle_converges` | MUST-MEET |
| **B3** circle stochastic (anti-constant guard) | hw17 | autograder | `test_circle_is_stochastic_not_constant` | independent |
| **B4** sphere (3-D) converges | hw17 | autograder | `test_sphere_converges` | independent |
| **B5** n-ball contract + converges; π convergence floor-AND-guard | hw17 | autograder | `test_n_ball...`, `test_pi_convergence_improves_with_n` | MUST-MEET |
| **D1** analytic `E[f(X)]=18.61` derivation | hw6 | human per-step | D1 ≥ Proficient | MUST-MEET |
| **D2** 2-D/3-D/n-D π formulas | hw17 | human per-step | D2 ≥ Proficient | MUST-MEET |

5 MUST-MEET (A2, B2, B5, D1, D2) + 4 independent (A1, B1, B3, B4); threshold ≤ 1.

## Bundle 2 — Interpretation (CERL)

| Spec | Prompt | PASS when… |
|------|--------|-----------|
| **I1** | empirical convergence rate / error vs N | ≥2 every CERL dim |
| **I2** | curse of dimensionality via acceptance rate | ≥2 every CERL dim |

## Bundle 3 — Process

| Spec | PASS when… |
|------|-----------|
| **P1** RNG seeded | reproducible |
| **P2** `import hw` cheap | < ~0.1 s |
| **P3** `.qmd` renders clean (Typst); plots labeled | met |

## Objective → spec → bundle coverage (nothing dropped)

| Source objective | Specs | Bundle |
|------------------|-------|--------|
| hw6 f + Monte-Carlo expectation | A1, A2 | Correctness |
| hw6 analytic expectation | D1 | Correctness |
| hw17 π estimators (orthants, circle, sphere, n-ball) | B1–B5 | Correctness |
| hw17 2-D/3-D/n-D derivations | D2 | Correctness |
| convergence rate / curse of dimensionality | I1, I2 | Interpretation |
| reproducibility & communication | P1–P3 | Process |

**Every source objective maps to ≥1 spec.**
