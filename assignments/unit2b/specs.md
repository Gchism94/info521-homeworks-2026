# Unit 2b — Specifications (Unit 1 template; written-only, all-human Correctness)

Same template as Unit 1: rows → met/not-met specs; bundles Correctness (core/gateway),
Interpretation, Process; MUST-MEET vs independent (threshold ≤ 1); pass / revise-resubmit.

> **TEMPLATE-FIT NOTE — all-human Correctness (clean; the inverse of U2a, still no structural
> change).** U2b is written-only, so **every** Correctness spec is human-graded per-step (each step
> met at *Proficient+*). Same bundle structure as Unit 1; only the *Verified by* metadata is
> uniformly "human." No autograder — the shared conditional `classroom.yml` skips pytest when no
> `test_hw.py` is present (the written-cluster infra fix). The Process bundle drops the code-only
> specs (import/seed) and keeps notation + render — spec *text*, not structure.

## Bundle 1 — Correctness · CORE / GATEWAY  (all human per-step)

PASS rule: **every MUST-MEET spec met, and ≤ 1 missed among the independent specs.**

| Spec | From | Verified by | Step | Type |
|------|------|-------------|------|------|
| **A1** `∂w/∂w = I` | hw7 | human per-step | A1 ≥ Proficient | independent |
| **A2** `∂/∂wᵀ f = (∂f/∂w)ᵀ` (row=col transpose) | hw7 | human per-step | A2 ≥ Proficient | independent |
| **A3** `∂/∂wᵀ(Cw) = C` (Kronecker collapse) | hw7 | human per-step | A3 ≥ Proficient | MUST-MEET (used in U1 & U5) |
| **B1** diagonal Gaussian ⇒ independent univariate Gaussians | hw8 | human per-step | B1 ≥ Proficient | MUST-MEET (foundation) |
| **B2** Bernoulli MLE unbiased `E[r̂]=r` | hw8 | human per-step | B2 ≥ Proficient | independent |
| **B3** Beta mean `α/(α+β)` | hw8 | human per-step | B3 ≥ Proficient | MUST-MEET (feeds B4) |
| **B4** Beta variance `αβ/((α+β)²(α+β+1))` | hw8 | human per-step | B4 ≥ Proficient | MUST-MEET (result) |

4 MUST-MEET (A3, B1, B3, B4) + 3 independent (A1, A2, B2); threshold ≤ 1.

## Bundle 2 — Interpretation  (CERL; LLM-pre-grade + human-confirm)

| Spec | Prompt | PASS when… |
|------|--------|-----------|
| **I1** | symmetry in A3 / where the identities are used downstream | ≥2 on every CERL dimension |
| **I2** | what unbiasedness guarantees and what it does not | ≥2 on every CERL dimension |
| **I3** | `α,β` as pseudo-counts; Beta as a prior as `α+β→∞` | ≥2 on every CERL dimension |

Bundle PASS = all three.

## Bundle 3 — Process

| Spec | PASS when… |
|------|-----------|
| **P1** assumptions stated (symmetry of C; i.i.d./`E[xₙ]=r`; `α,β>0`) | met |
| **P2** notation consistent; each line follows; `.qmd` renders clean (Typst) | met |

## Objective → spec → bundle coverage (nothing dropped)

| Source objective | Specs | Bundle |
|------------------|-------|--------|
| hw7 three Jacobian identities | A1, A2, A3 | Correctness |
| hw8 diagonal-Gaussian independence | B1 | Correctness |
| hw8 MLE unbiasedness | B2 | Correctness |
| hw8 Beta mean / variance | B3, B4 | Correctness |
| interpret symmetry / unbiasedness / Beta-as-prior | I1, I2, I3 | Interpretation |
| notation & communication | P1, P2 | Process |

**Every source objective maps to ≥1 spec.** Forward/back references: A1–A3 ↔ U1 (applied) & U5
(Hessian); B2 ↔ U2a (MLE); B3–B4 ↔ U4 (conjugate Beta prior).
