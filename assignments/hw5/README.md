# HW5 — Maximum Likelihood for a Bernoulli Parameter

> Overhauled (Scope-A pilot, written-derivation template). Grading is **per-step +
> specifications-based**, not the old complete/incomplete gate. The full rubric ships with
> the assignment in `rubric.md`.

## Instructions

Compile `hw.tex` to a PDF (see HW0's `README.md` for how), and complete the exercise. Write
up your solution — hand-written or typeset in LaTeX — and submit a hard copy by the start of
class on the due date.

## What you'll do

Derive the maximum-likelihood estimator for the parameter `r` of a Bernoulli distribution
from `N` i.i.d. samples: (1) write the likelihood, (2) show it has a unique maximum, (3)
derive `r̂`. Then write one short paragraph interpreting the result (see `hw.tex` §"Required
interpretation").

## Allowed approaches

**Any mathematically valid derivation that reaches `r̂ = (Σxᵢ)/N` earns full credit** — no
single path is privileged. Maximize `L` or `log L`; argue uniqueness by the second-derivative
test, strict concavity, or a single sign-change of the score. Just **show the steps**.

## How you'll be assessed (criteria shown up front)

| Bundle | Weight | Pass when… |
|--------|:------:|------------|
| **Correctness** | **60%** | per-step derivation rubric (`rubric.md` §2a) — steps A (likelihood), B (unique max), C (closed-form `r̂`) each at **Proficient+**. Any sound route counts. |
| **Interpretation** | **30%** | the required paragraph reaches **Proficient+** on every Claim/Evidence/Reasoning/Limits dimension (`rubric.md` §2b). |
| **Process** | **10%** | clear notation, stated assumptions, legible justification (`rubric.md` §2c). |

**Revision:** if a bundle falls short you get **one revise-and-resubmit** in the posted
window. An LLM may draft per-dimension scores; a human confirms every grade and is final.
