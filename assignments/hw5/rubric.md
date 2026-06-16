# HW5 — Grading rubric (per-step derivation + interpretation)

No autograder: this is a **written** derivation. Grading replaces the old 1/0.5/0 gate with
per-step partial credit. Criteria are shown here up front (see the repo-root `rubric.md` for
the shared analytic rubric this instantiates). Weights follow the written/derivation-HW canon
**60 / 30 / 10** (correctness is human-verified; see the repo-root `rubric.md`).

## §2a · Correctness (60) — per-step derivation rubric

Each step is scored on the **validity of the move**, *not* on matching this key's exact
algebra. **Any sound alternative route that reaches `r̂ = (Σxᵢ)/N` earns full credit.** Each
step gets a 0–3 tier (3 → 100% of its points, 2 → 80%, 1 → 45%, 0 → 0%).

| Step | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
|------|-----|:---:|---------------|----------------|----------------|---|
| **A · Likelihood** | O1 | 13 | `L = ∏ rˣⁱ(1−r)¹⁻ˣⁱ`, independence named | product right, independence implicit | partial / wrong exponents | missing/wrong |
| **B · Unique max** | O2 | 24 | uniqueness *shown* (strict concavity / `∂²log L/∂r²<0` / single sign-change) | 2nd derivative taken, sign argued loosely | 1st derivative only / asserted | missing/wrong |
| **C · MLE** | O3 | 23 | clean algebra to `r̂ = (Σxᵢ)/N` | right answer, minor slip | sets up, can't solve | missing/wrong |

**Load-bearing vs. independent.** A is load-bearing for the *values* in B and C but not their
*moves*: grade B and C on correct manipulation of the student's own `L`; an error in A caps
final correctness but not method credit. B and C are mutually independent — skipping
uniqueness (lose B) does not block full credit on C, and vice versa. The log-transform is an
optional enabling move, never required.

## §2b · Interpretation (30) — Claim / Evidence / Reasoning / Limits

The required paragraph, scored 0–3 on each dimension (12 raw → 30%). PASS = ≥2 each.

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | states `r̂` *is* the sample proportion of 1's | mostly | partial | missing |
| **Evidence** | grounds it in `Σxᵢ` counting successes, `/N` making a fraction (or a concrete `N`) | some | vague | none |
| **Reasoning** | links "maximize likelihood" → "match `r` to observed success rate" | sound | superficial | absent |
| **Limits** | names a real failure + the broken assumption (small `N`; all-identical ⇒ `r̂∈{0,1}`; non-i.i.d.) | one weakly | minimal | none |

## §2c · Process (10) — communication

| Sub-dim | Pts | Full credit when… |
|---------|:---:|-------------------|
| Notation | 4 | symbols defined/consistent; `log` base stated |
| Stated assumptions | 3 | i.i.d. given `r`, `xᵢ∈{0,1}`, `r∈(0,1)` explicit |
| Justification clarity | 3 | each implication follows; legible |

## Specifications bundle

- **Derivation = PASS:** steps A–C each ≥ Proficient. **Interpretation = PASS:** ≥2 on every
  CERL dimension. Otherwise **one revise-and-resubmit** in the posted window.
- An LLM may pre-draft per-dimension scores + one-line reasons; a **human confirms every
  grade and is final**. (LLM pre-grading is weak on derivations — humans grade A–C; the LLM
  at most checks the final closed form and drafts the interpretation score.)
