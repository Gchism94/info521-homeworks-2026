# Unit 2a — Specifications (Unit 1 template applied; mixed Correctness bundle)

Same template as Unit 1 (`assignments/unit1/specs.md`): each former rubric row → one
met/not-met **spec**; bundles **Correctness** (core/gateway), **Interpretation**, **Process**;
MUST-MEET vs independent (threshold ≤ 1 missed independent); pass / revise-and-resubmit; per-HW
weights are moot.

> **TEMPLATE-FIT NOTE — mixed Correctness bundle (clean application, no structural change).**
> Unit 2a's Correctness bundle holds **two kinds of spec**: *autograded* (Part A, hw4) and
> *human-graded per-step derivation* (Parts B/C, hw5/hw9). This is a clean fit, not a structural
> change: (1) each derivation step is still **one binary spec** — *met = tier ≥ Proficient* — the
> same tier→binary rule the Interpretation bundle uses for CERL; (2) the framework defines
> Correctness as "autograded thresholds **or** per-step rubric for written," so both belong in one
> Correctness/gateway bundle; (3) MUST-MEET / independent come from each derivation's load-bearing
> flags; (4) revise-and-resubmit replaces per-step partial credit (the point of specs grading). The
> **only** addition is a *Verified by* column (autograder vs. human per-step).

## Bundle 1 — Correctness · CORE / GATEWAY

PASS rule: **every MUST-MEET spec met, and ≤ 1 missed among the independent specs.**

| Spec | From | Verified by | Test / step | Type |
|------|------|-------------|-------------|------|
| **A1** P(2≤X≤6) closed-form (rel 1e-6) | hw4 | autograder | `test_pmf_a_closed_form` | MUST-MEET |
| **A2** (a) = actual range-sum (anti-constant guard) | hw4 | autograder | `test_pmf_a_is_range_sum_not_constant` | MUST-MEET |
| **A3** complement `(a)+(b)=1` | hw4 | autograder | `test_complement` | MUST-MEET |
| **A-pmf** pmf matches `λˣ/x!·e^{−λ}` at several x | hw4 | autograder | `test_poisson_pmf_values` | independent |
| **A-dist** pmf ∈ [0,1], sums to 1 | hw4 | autograder | `test_poisson_is_valid_distribution` | independent |
| **B1** Bernoulli likelihood (independence) | hw5 | human per-step | step B1 ≥ Proficient | MUST-MEET (foundation) |
| **B2** unique maximum (strict concavity) | hw5 | human per-step | step B2 ≥ Proficient | independent |
| **B3** solve → `r̂ = (Σxₙ)/N` | hw5 | human per-step | step B3 ≥ Proficient | MUST-MEET (result) |
| **C1** Fisher-info definition (curvature / score-variance) | hw9 | human per-step | step C1 ≥ Proficient | MUST-MEET (foundation) |
| **C2** score `y/r − (1−y)/(1−r)` | hw9 | human per-step | step C2 ≥ Proficient | independent |
| **C3** curvature `−y/r² − (1−y)/(1−r)²` | hw9 | human per-step | step C3 ≥ Proficient | independent |
| **C4** expectation → `1/(r(1−r))` | hw9 | human per-step | step C4 ≥ Proficient | MUST-MEET (result) |

7 MUST-MEET (A1, A2, A3, B1, B3, C1, C4) + 5 independent (A-pmf, A-dist, B2, C2, C3); threshold ≤ 1.

## Bundle 2 — Interpretation  (CERL; LLM-pre-grade + human-confirm)

| Spec | Prompt | PASS when… |
|------|--------|-----------|
| **I1** | Poisson probability + complement meaning | ≥2 on every CERL dimension |
| **I2** | `r̂` = sample proportion; when misleading | ≥2 on every CERL dimension |
| **I3** | where `I(r)` is largest/smallest; informativeness | ≥2 on every CERL dimension |

Bundle PASS = all three (each load-bearing for O4).

## Bundle 3 — Process

| Spec | PASS when… |
|------|-----------|
| **P1** Part A uses `math` only; no hard-coded answers | met |
| **P2** `import hw` cheap | < ~0.05 s |
| **P3** `.qmd` renders clean (Typst); derivations legible | met |

## Objective → spec → bundle coverage (nothing dropped)

| Source objective | Specs | Bundle |
|------------------|-------|--------|
| hw4 Poisson pmf + probabilities + complement | A1, A2, A3, A-pmf, A-dist | Correctness |
| hw5 Bernoulli MLE (likelihood → unique max → solve) | B1, B2, B3 | Correctness |
| hw9 Fisher information (def → score → curvature → expectation) | C1, C2, C3, C4 | Correctness |
| interpret Poisson / MLE / Fisher | I1, I2, I3 | Interpretation |
| reproducibility & communication | P1–P3 | Process |

**Every source objective maps to ≥1 spec. Through-line B→C (`1/(N·I(r))=r(1−r)/N`) preserved.**
