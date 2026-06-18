# Unit 5 — Specifications (Unit 1 template; largest Correctness bundle, four spec kinds)

Same template as Unit 1: rows → met/not-met specs; bundles Correctness (core/gateway),
Interpretation, Process; MUST-MEET vs independent (threshold ≤ 1); pass / revise-resubmit.

> **TEMPLATE-FIT NOTE — four spec *kinds* in one Correctness bundle (clean; new content, not new
> structure).** U5's gateway bundle is the unit's largest and holds: **autograded** (MAP, Laplace,
> MCMC), **human per-element structural** (the PGM, hw13), **human per-step derivation** (the two
> update rules, hw14/hw15 written), and **one new spec kind — cross-method agreement** (X1–X2: the
> "four ways, one posterior" check). This is a clean fit: each is still a binary met/not-met spec;
> the bundle structure (gateway / MUST-MEET / independent / threshold ≤1 / revise) is unchanged; the
> cross-method specs are new *content*, and structural/cross-method are new values in the *Verified
> by* column. **Flag:** this is the largest gateway (16 specs) — the ≤1 threshold is strict by
> design and cushioned by revise-and-resubmit; no threshold scaling was introduced (that would be a
> structural change requiring ratification).
>
> **Posterior mode ≠ mean (design note):** MCMC estimates the **mean** (≈[2.5,2.9]); Newton gives
> the **mode** (≈[1.64,2.0]). The cross-method specs therefore do **not** assert mean==mode; they
> assert the mode sits **inside** the MCMC bulk (X1) and Laplace matches the MCMC **spread** (X2).

## Bundle 1 — Correctness · CORE / GATEWAY  (autograded + human structural + human per-step)

PASS rule: **every MUST-MEET spec met, and ≤ 1 missed among the independent specs.**

| Spec | From | Verified by | Test / step | Type |
|------|------|-------------|-------------|------|
| **S1** nodes & roles (`σ²`,`w` random circles; `xₙ`,`tₙ` shaded) | hw13 | human structural | S1 ≥ Proficient | independent |
| **S2** edges `σ²→w`, `w→tₙ←xₙ`; no spurious | hw13 | human structural | S2 ≥ Proficient | MUST-MEET (the model) |
| **S3** plate over n; excludes shared `w`,`σ²` | hw13 | human structural | S3 ≥ Proficient | independent |
| **M1** MAP recovery floor `‖grad(w_MAP)‖<1e-4` | hw14 | autograder | `test_map_recovery_floor` | MUST-MEET |
| **M2** `w_MAP ≈ [1.640,2.000]` | hw14 | autograder | `test_map_matches_reference` | MUST-MEET |
| **M3** Hessian negative-definite at MAP | hw14 | autograder | `test_hessian_negative_definite` | independent |
| **L1** `g_cov=(−H)⁻¹`, symmetric PSD | hw15 | autograder | `test_laplace_is_inverse_neg_hessian_psd` | MUST-MEET |
| **L2** `g_cov ≈ [[3.507,…]]` | hw15 | autograder | `test_laplace_matches_reference` | independent |
| **MC1** log-prior formula | hw16 | autograder | `test_mcmc_log_prior` | independent |
| **MC2** log-likelihood + acceptance ratio | hw16 | autograder | `test_mcmc_log_likelihood_and_acceptance` | independent |
| **MC3** proposal seeded + shaped | hw16 | autograder | `test_mcmc_proposal_seeded_and_shaped` | independent |
| **MC4** posterior recovery + **mixing floor-AND-guard** | hw16 | autograder | `test_mcmc_recovers_posterior_and_mixes` | MUST-MEET |
| **D1** Poisson Newton–Raphson update (gradient→Hessian→update) | hw14 | human per-step | D1 ≥ Proficient | MUST-MEET |
| **D2** Beta–Binomial Laplace (mode `r̂` + curvature `ν`) | hw15 | human per-step | D2 ≥ Proficient | MUST-MEET |
| **X1** MAP mode inside MCMC posterior bulk | cross | autograder | `test_cross_method_map_mode_inside_mcmc_posterior` | independent |
| **X2** Laplace spread ≈ MCMC spread (std within 2×) | cross | autograder | `test_cross_method_laplace_matches_mcmc_spread` | MUST-MEET |

8 MUST-MEET (S2, M1, M2, L1, MC4, D1, D2, X2) + 8 independent; threshold ≤ 1.

## Bundle 2 — Interpretation  (CERL; LLM-pre-grade + human-confirm)

| Spec | Prompt | PASS when… |
|------|--------|-----------|
| **I1** | compare the four methods (cost/accuracy/failure modes) | ≥2 every CERL dim |
| **I2** | why mode ≠ mean; which to report | ≥2 every CERL dim |
| **I3** | did the chain mix; effect of `σ²_proposal` | ≥2 every CERL dim |

## Bundle 3 — Process

| Spec | PASS when… |
|------|-----------|
| **P1** MCMC seeded (`default_rng(seed)`) | reproducible |
| **P2** `import hw` cheap | < ~0.1 s |
| **P3** `.qmd` renders clean (Typst); trace/figures labeled | met |

## Objective → spec → bundle coverage (nothing dropped)

| Source objective | Specs | Bundle |
|------------------|-------|--------|
| hw13 PGM (nodes/edges/plate, conditional independence) | S1, S2, S3 | Correctness |
| hw14 MAP via Newton | M1, M2, M3 | Correctness |
| hw15 Laplace covariance | L1, L2 | Correctness |
| hw16 MH-MCMC (log-prior/likelihood, proposal, acceptance, recovery) | MC1–MC4 | Correctness |
| hw14 Poisson NR derivation | D1 | Correctness |
| hw15 Beta–Binomial Laplace derivation | D2 | Correctness |
| four-ways agreement (the unit spine) | X1, X2 | Correctness |
| compare methods / mode-vs-mean / mixing | I1, I2, I3 | Interpretation |
| reproducibility & communication | P1–P3 | Process |

**Every source objective maps to ≥1 spec. Nothing dropped** — incl. hw14's Poisson and hw15's
Beta–Binomial derivations (kept as D1/D2, the "derive the method" companions to the code).
