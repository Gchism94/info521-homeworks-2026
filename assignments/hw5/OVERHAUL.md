# hw5 — Overhaul draft (Scope A pilot · pure written-derivation template)

Instantiates `OVERHAUL_FRAMEWORK.md` on hw5 (MLE for a Bernoulli parameter). **Draft only
— no hw5 files are modified.** This is the template for the whole written-derivation
cluster (hw5, 7, 8, 9, 12, 13 → Unit 2): per-step credit replaces the 1/0.5/0 gate, and a
short interpretation part lifts the ceiling from *derive* to *interpret*.

hw5 is written-only (LaTeX, hard-copy). There is **no autograder** — the "Correctness"
layer here is a **per-step derivation rubric**, not pytest. Answer markers
`%%% Answer START %%%` / `%%% Answer END %%%` are preserved.

---

## 1. Prompt rewritten into the 8-part template (replaces `hw5/hw.tex` body + README)

**1. Context & purpose.** The Bernoulli MLE — "the estimate is just the sample proportion"
— is the simplest case of a pattern (write a likelihood, maximize a log-likelihood) you'll
repeat all term for Gaussians, Poissons, and logistic models. Doing it carefully once makes
the rest mechanical.

**2. Learning objectives.** By the end you can:
- **O1** Write the likelihood of an i.i.d. dataset from its per-sample distribution.
  *(Apply — rubric step A)*
- **O2** Show a log-likelihood has a unique maximum via the second derivative.
  *(Analyze — rubric step B)*
- **O3** Derive the MLE in closed form. *(Analyze — rubric step C)*
- **O4** Interpret the estimator: why it equals the sample mean, and when that misleads.
  *(Evaluate — interpretation rubric)*

**3. The task.** For `N` i.i.d. samples `x₁,…,x_N` from `Bernoulli(r)` with
`P(x|r) = rˣ(1−r)¹⁻ˣ`:
(1) write the likelihood `L`; (2) show `L` has a unique maximum; (3) derive the MLE `r̂`.

**4. What you may and may not use.** Any valid route is accepted: maximize `L` directly or
the log-likelihood; the second-derivative test **or** a concavity/convexity argument for
uniqueness. You must **show the steps** — a bare final answer earns only the result step.

**5. How you'll be assessed (shown up front).** Per-step derivation rubric (60%, §3 below:
setup → key move → result, each partial-creditable) + interpretation rubric (30%, prompt in
§6) + communication (10%, legible, correct notation). Specs bundle: "Derivation = PASS"
needs steps A–C each ≥ Proficient; one revise-and-resubmit otherwise.

**6. Required interpretation** (1 short paragraph): Explain *why* `r̂ = (Σxᵢ)/N` is the
sample proportion, and give **one** situation where it misleads (e.g., `N` very small, or
all observed outcomes identical so `r̂ ∈ {0,1}`).

**7. Going further (optional).** Add a `Beta(a,b)` prior and find the MAP estimate; comment
on how the prior pulls `r̂` away from the sample proportion for small `N`.

**8. Submission.** LaTeX → PDF, hard-copy as today (the written cluster keeps its medium;
only the *grading* changes). Include the workload + acknowledgments sections unchanged.

---

## 2. Per-step derivation rubric — `hw5/rubric.md` (replaces 1/0.5/0)

Three steps, each scored 0–3; this is the "Correctness" layer for written HWs.

| Step | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
|------|---------------|----------------|----------------|---|
| **A · Setup (O1)** | `L = ∏ rˣⁱ(1−r)¹⁻ˣⁱ`, independence stated | product right, independence implicit | partial product / wrong exponents | missing/incorrect |
| **B · Uniqueness (O2)** | `∂²/∂r² log L < 0` shown for all `r∈(0,1)` ⇒ unique max | second derivative taken, sign argued loosely | first derivative only / asserts w/o showing | missing/incorrect |
| **C · Result (O3)** | sets `∂log L/∂r = 0`, clean algebra to `r̂ = (Σxᵢ)/N` | right answer, minor algebra slip | sets up but can't solve | missing/incorrect |

## 3. Interpretation rubric — shared analytic rubric (the §6 paragraph)

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | correctly says `r̂` = sample proportion | mostly | partial | missing |
| **Evidence** | references the derived form / a concrete N | some | vague | none |
| **Reasoning** | links "maximize likelihood" → counting successes/N | sound | superficial | absent |
| **Limits** | names a real failure (small N, `r̂∈{0,1}`) | one weakly | minimal | none |

---

## 4. Files touched (when applied)

- `hw5/hw.tex` — add the 8-part framing (Context/Objectives/allowed-methods/interpretation
  prompt/optional MAP extension) around the **unchanged** problem statement; keep the
  `%%% Answer … %%%` solution block exactly as-is so `make_release` still strips it.
- `hw5/README.md` — replace the 1/0.5/0 rubric text with the per-step + interpretation
  rubric and the specs PASS/revise rule; state the criteria up front (TILT).
- `hw5/rubric.md` — **new** (§2 + §3), shipped to students so they see the criteria.

**No code; no autograder.** Note: LLM pre-grading (framework §9) is weak on math
*derivations* — humans grade steps A–C; the LLM at most checks the final closed-form answer
and drafts the interpretation-paragraph score for human confirmation.

## 5. Alignment & effort

| Objective | Assessed by |
|-----------|-------------|
| O1/O2/O3 derivation | rubric steps A/B/C |
| O4 interpretation | interpretation rubric |

Every objective maps to a rubric row (none unmeasurable). **Effort:** +~10 min for the
interpretation paragraph; derivation length unchanged. Well within budget.
