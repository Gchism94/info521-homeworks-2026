# hw8 — Overhaul draft (written-derivation pattern · Typst · four Gaussian/Beta derivations)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw8 ("Gaussian manipulation" + MLE unbiasedness +
Beta mean/variance). Matches the **hw5 / hw9 written-derivation pilots**. **Draft only — no hw8
files are modified; the diffs below are proposed, not applied.**

**Split: written/derivation → 60 / 30 / 10** (repo canon; correctness human-verified).
**No pytest** — the "Correctness" layer is a per-step derivation rubric.

> **STEP 0 — classification.** All four exercises are *"Show that…"* / *"Derive an expression
> for…"* tasks → **DERIVATION** (steps → result), so Correctness is a **per-step rubric**, not
> CERL. The interpretation layer is *not* forced (the hw11 lesson): the Beta mean/variance are
> the parameters of the **conjugate prior** for a probability `r`, and reading `α, β` as
> pseudo-counts / a prior sample size is the canonical, genuinely Evaluate-level interpretation
> of exactly these two formulas — and it links forward to the Bayesian-inference HWs (hw11,
> hw12). So a CERL Interpretation row (30) is legitimate, not manufactured.

> **Marker reconciliation (Typst, same as hw7/hw9).** hw8 is **Typst** (`hw.typ`). Strip = the
> `#answer([sol], [blank])` macro toggled by `make without_answers`
> (`--input show_answers=false`), which renders only the *second* argument. The **`#answer(...)`
> first argument is the answer marker**. All solution edits stay inside it; the strip was
> validated by simulation (§7), not compiled (format note).

> **Through-line preserved.** Exercise 2 ("Show the MLE from HW5 is unbiased") explicitly builds
> on hw5's `r̂ = (Σxᵢ)/N`; the prompt keeps that reference, and the interpretation ties the Beta
> prior back to the same Bernoulli rate `r`.

---

## 1. Prompt rewritten into the 8-part template (markdown)

> Authored here and mirrored into `README.md` (§4b). In `hw.typ` only two student-facing blocks
> (a global Allowed-approaches note + the Required-interpretation prompt) are added outside
> `#answer`; the rest of the framing lives in `README.md`.

**1. Context & purpose.** Four short derivations that are load-bearing for the rest of the
course: a diagonal Gaussian factorizes into independent coordinates (the basis for "uncorrelated
⇔ independent" *for Gaussians*); the HW5 sample-mean MLE is unbiased (an estimator-quality
property); and the Beta mean and variance — the parameters of the conjugate prior you will use
for Bayesian inference about a probability.

**2. Learning objectives** (Bloom verb + the rubric row each is measured by):
- **O1** *Show* a diagonal-covariance Gaussian equals a product of `D` univariate Gaussians
  (independence). *(Apply/Analyze — Correctness E1)*
- **O2** *Prove* the HW5 MLE `r̂ = (Σxᵢ)/N` is unbiased via linearity of expectation.
  *(Apply — Correctness E2; hw5 through-line)*
- **O3** *Derive* the Beta mean `E[r] = α/(α+β)`. *(Apply — Correctness E3)*
- **O4** *Derive* the Beta variance `var{r} = αβ/((α+β)²(α+β+1))`. *(Analyze — Correctness E4)*
- **O5** *Interpret* `α, β` as encoding prior strength/belief about a probability (the
  conjugate-prior role). *(Evaluate — Interpretation)*

**3. The task (outcome, not recipe).** Prove the four results: (1) diagonal `Σ` ⇒ independence;
(2) `E[r̂] = r`; (3) `E[r] = α/(α+β)`; (4) `var{r} = αβ/((α+β)²(α+β+1))`.

**4. Allowed approaches.** **Any mathematically valid route to each result earns full credit.**
State the identities and assumptions you invoke (diagonal determinant/inverse facts, the gamma
recursion `Γ(n+1) = nΓ(n)`, linearity of expectation, i.i.d. sampling). A bare final answer
earns only the result step.

**5. How you'll be assessed (criteria shown up front).**
- *Correctness (60%)* — the per-step rubric in §2a (E1–E4), each scored on the **validity of the
  move**, full credit for any sound alternative route.
- *Interpretation (30%)* — the §6 paragraph, scored Claim/Evidence/Reasoning/Limits.
- *Process (10%)* — identities/assumptions stated, notation consistent, justification legible.
- *Specs bundle:* "Derivation = PASS" needs E1–E4 each ≥ Proficient; "Interpretation = PASS"
  needs ≥2 on every CERL dimension; else one revise-and-resubmit.

**6. Required interpretation** (one short paragraph, no new algebra): a Beta density is the
standard prior for an unknown probability `r` (e.g. the Bernoulli rate from HW5). Using your
mean `α/(α+β)` and variance, explain **what `α` and `β` encode** about a prior belief in `r`,
**what happens to the spread as `α+β` grows and why**, and **one assumption or limiting case**
where this interpretation breaks.

**7. Going further (optional, ungraded).** For Exercise 1, state whether "uncorrelated ⇒
independent" holds for *non*-Gaussian distributions, and give (or sketch) a counterexample —
i.e. why this equivalence is special to the Gaussian.

**8. Submission contract.** Written derivation, hard copy as today (the written cluster keeps its
medium; only the *grading* changes). Keep Workload + Acknowledgments. The only build contract is
that every solution stays inside an `#answer([…], [])` first argument so `make without_answers`
strips it.

---

## 2. `hw8/rubric.md` — per-step derivation rubric (NO pytest)

### 2a. Correctness (60) — per-step derivation rubric

Four exercises; **each scored on the validity of the move, not on matching the reference's exact
algebra.** Any sound alternative route earns full credit. Each exercise gets a 0–3 tier mapping
to a fraction of its points (3→100%, 2→80%, 1→45%, 0→0%). Weights sum to 60; **E4 heaviest** (it
builds on E3 and carries the most algebra), **E2 lightest** (a short linearity argument).

| Exercise | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
|----------|-----|:---:|---------------|----------------|----------------|---|
| **E1 · diagonal `Σ` ⇒ independence** | O1 | 16 | substitutes `\|Σ\|=∏σ_d²` and `Σ⁻¹=diag(1/σ_d²)`, expands the quadratic form to `Σ(x_d−μ_d)²/σ_d²`, uses exp-of-sum = product, factorizes into `∏` univariate Gaussians, names independence | reaches the product, one step asserted (det / exp-split) | substitutes det/inverse but cannot factor | missing/wrong |
| **E2 · MLE unbiased** | O2 | 12 | `E[r̂]=E[Σxᵢ/N]`, pulls out `1/N`, **linearity** `Σ E[xᵢ]`, `E[xᵢ]=r`, `=Nr/N=r`; states the unbiasedness definition | correct, a step (linearity / `E[xᵢ]=r`) asserted | sets up `E[r̂]` but cannot complete | missing/wrong |
| **E3 · Beta mean** | O3 | 14 | `E[r]=∫ r·p(r)dr`, absorbs `r` (`α→α+1`), applies the normalization identity, uses `Γ(n+1)=nΓ(n)` → `α/(α+β)` | result reached, minor slip | sets up integral, cannot apply the identity | missing/wrong |
| **E4 · Beta variance** | O4 | 18 | `E[r²]` via `α→α+2` and the `Γ` identity → `α(α+1)/((α+β)(α+β+1))`, then `var=E[r²]−(E[r])²` → `αβ/((α+β)²(α+β+1))` | `E[r²]` right, final simplification slips | sets up `E[r²]`, cannot finish | missing/wrong |

**Load-bearing vs. independent:**
- **E1, E2, E3 are mutually independent** — grade each in isolation.
- **E4 depends on E3's `E[r]`** (the variance formula subtracts `(E[r])²`): grade E4's `E[r²]`
  derivation and the `var` assembly on the student's *own* `E[r]`. An error in E3 caps E4's final
  value, **not** its method credit.
- **Within E1 the load-bearing insight is the exp-of-sum → product factorization** (turning a
  single quadratic form into independent factors); award it even if the determinant/inverse
  substitution slips. **Within E3/E4 the load-bearing move is recognizing the integral as an
  unnormalized Beta** and applying the normalization identity.

### 2b. Interpretation (30) — Claim / Evidence / Reasoning / Limits (0–3 each)

The §6 paragraph (12 raw → 30%). PASS = ≥2 every dimension.

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | `α/(α+β)` is the prior mean (center of belief) and the variance **shrinks as `α+β` grows** | mostly right, minor gap | direction confused | missing |
| **Evidence** | grounds it in the two derived formulas — e.g. `α=β` ⇒ mean `1/2`; large `α+β` ⇒ small `αβ/((α+β)²(α+β+1))` | some numbers | vague | none |
| **Reasoning** | reads `α+β` as a **prior sample size** (`α`/`β` = pseudo successes/failures); connects Beta as the **conjugate prior** for the Bernoulli rate (HW5 / later Bayesian updates) | sound but thin | superficial | absent/wrong |
| **Limits** | names a real condition: needs `α,β>0` (proper); `α+β→∞` ⇒ prior dominates the data; `α,β→0` ⇒ improper/U-shaped, pseudo-count reading breaks | one weakly | minimal | none |

### 2c. Process (10) — identities, notation, clarity

| Sub-dim | Pts | Full credit when… |
|---------|:---:|-------------------|
| **Stated identities/assumptions** | 4 | the facts invoked are named: diagonal det/inverse, `Γ(n+1)=nΓ(n)`, linearity of expectation, i.i.d. given `r` |
| **Notation** | 3 | `Σ`, `μ`, `r̂`, `α`, `β`, `E`, `var` defined/consistent |
| **Justification clarity** | 3 | each line follows from the previous; legible |

---

## 3. Objective → rubric-row map (alignment contract)

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| **O1** diagonal Gaussian ⇒ independence | Apply/Analyze | Correctness **E1** | ✅ |
| **O2** MLE unbiased (hw5 through-line) | Apply | Correctness **E2** | ✅ |
| **O3** Beta mean | Apply | Correctness **E3** | ✅ |
| **O4** Beta variance | Analyze | Correctness **E4** | ✅ |
| **O5** interpret `α, β` (conjugate-prior role) | Evaluate | **Interpretation** rubric (CERL) | ✅ |
| *(communication)* | — | **Process** rubric (2c) | ✅ (cross-cutting, not an O#) |

**Every objective maps to a rubric row; none unmeasurable.** Process is the standard
objective-free communication layer.

---

## 4. Proposed unified diffs (per file — NOT applied)

### 4a. `hw.typ` — add framing (outside `#answer`); the four reference derivations left intact

The four existing derivations are already complete and correct, so they are **not rewritten**.
Only two student-facing blocks are added outside any `#answer`: a global Allowed-approaches note
under the Homework-8 header, and a Required-interpretation prompt + reference `#answer` block
after Exercise 4. No imports, headings, or the four original `#answer` boundaries are disturbed.

```diff
--- a/hw.typ
+++ b/hw.typ
@@
   #text(size: 14pt, fill: chili, smallcaps[Homework 8])
 ]
+
+#strong[Allowed approaches.] Any mathematically valid route to each result earns
+full credit — no canonical path is privileged. State the identities and
+assumptions you invoke (e.g. the diagonal determinant / inverse facts, the gamma
+recursion $Gamma(n+1) = n Gamma(n)$, linearity of expectation, i.i.d. sampling)
+and keep notation consistent. A bare final answer earns only the result step.
+Grading criteria are in #emph[rubric.md].

 = Gaussian manipulation
 ⋯ (E1, E2, E3, E4 prompts and #answer derivations unchanged) ⋯
@@  (after the Exercise-4 variance #answer block, before "= Workload")  @@
+= Interpretation
+<interpretation>
+#strong[Required interpretation.] After the four derivations, add #emph[one short
+paragraph] (no new algebra) on the Beta results above. A Beta density is the
+standard prior for an unknown probability $r$ (e.g. the Bernoulli rate from HW5).
+Using your mean $alpha slash (alpha + beta)$ and variance, explain: what do
+$alpha$ and $beta$ encode about a prior belief in $r$; what happens to the spread
+as $alpha + beta$ grows, and why; and one assumption or limiting case where this
+interpretation breaks.
+
+#answer(
+  [
+    #strong[Reference interpretation.] The Beta mean
+    $bb(E){r} = alpha slash (alpha + beta)$ is the center of the prior belief
+    about the probability $r$, and the variance
+    $alpha beta slash ((alpha + beta)^2 (alpha + beta + 1))$ shrinks toward $0$
+    as $alpha + beta arrow.r infinity$. So $alpha + beta$ behaves like a
+    #emph[prior sample size]: reading $alpha$ as a count of prior "successes" and
+    $beta$ as prior "failures," a larger total makes the prior more concentrated
+    (more confident), while $alpha = beta$ centers it at $1 slash 2$. This is
+    exactly why the Beta is the conjugate prior for the Bernoulli / binomial rate
+    estimated in HW5 and used in the Bayesian updates later in the course: the
+    posterior is again Beta with $alpha, beta$ incremented by the observed
+    successes and failures. The interpretation needs $alpha, beta > 0$ (a proper
+    density); in the limit $alpha + beta arrow.r infinity$ the prior dominates any
+    finite dataset, and as $alpha, beta arrow.r 0$ the density becomes improper /
+    U-shaped and the "pseudo-count" reading breaks down.
+  ],
+  []
+)
+
 = Workload
```

### 4b. `README.md` — 8-part framing + criteria up front (replaces the 1/0.5/0 gate)

```diff
--- a/README.md
+++ b/README.md
@@
-# README
-
-The solutions to the exercises in `hw.pdf` need to be written up and submitted
-to me in person as a hard copy at the beginning of class on the due date.
-
-# Grading
-
-- 1 point: Homework is complete and correct
-- 0.5 points: Homework is incomplete or has errors.
-- 0 points: Homework was not submitted on time.
+# HW8 — Gaussian manipulation, MLE unbiasedness, Beta mean & variance
+
+> Overhauled (written-derivation pattern). Grading is **per-step + specifications-based**, not
+> the old complete/incomplete gate. The full rubric ships in `rubric.md`.
+
+## 1. Context & purpose
+
+Four short derivations load-bearing for the rest of the course: a diagonal Gaussian factorizes
+into independent coordinates; the HW5 sample-mean MLE is unbiased; and the Beta mean and
+variance — the parameters of the conjugate prior used for Bayesian inference about a probability.
+
+## 2. Learning objectives
+
+- **O1** Show a diagonal-covariance Gaussian = product of `D` univariate Gaussians. *(Correctness E1)*
+- **O2** Prove the HW5 MLE `r̂ = (Σxᵢ)/N` is unbiased. *(Correctness E2)*
+- **O3** Derive the Beta mean `α/(α+β)`. *(Correctness E3)*
+- **O4** Derive the Beta variance `αβ/((α+β)²(α+β+1))`. *(Correctness E4)*
+- **O5** Interpret `α, β` as prior strength/belief (conjugate-prior role). *(Interpretation)*
+
+## 3. The task
+
+Prove: (1) diagonal `Σ` ⇒ independence; (2) `E[r̂] = r`; (3) `E[r] = α/(α+β)`;
+(4) `var{r} = αβ/((α+β)²(α+β+1))`.
+
+## 4. Allowed approaches
+
+**Any mathematically valid route to each result earns full credit.** State the identities you
+invoke (diagonal det/inverse facts, `Γ(n+1)=nΓ(n)`, linearity of expectation, i.i.d. sampling).
+A bare final answer earns only the result step.
+
+## 5. How you'll be assessed (criteria shown up front)
+
+| Bundle | Weight | Pass when… |
+|--------|:------:|------------|
+| **Correctness** | **60%** | per-step rubric (`rubric.md` §2a) — E1 (independence), E2 (unbiasedness), E3 (Beta mean), E4 (Beta variance) each at **Proficient+**. Any sound route counts. |
+| **Interpretation** | **30%** | the required paragraph reaches **Proficient+** on every Claim/Evidence/Reasoning/Limits dimension (`rubric.md` §2b). |
+| **Process** | **10%** | identities/assumptions stated, consistent notation, legible justification (`rubric.md` §2c). |
+
+**Revision:** one revise-and-resubmit per bundle that falls short. An LLM may draft scores; a
+human confirms and is final.
+
+## 6. Submission
+
+Write up the four derivations **and** the required interpretation paragraph; submit a hard copy
+at the start of class on the due date. Record your time in the Workload section.
```

### 4c. `make_release` — ship `rubric.md` to students (TILT)

```diff
--- a/make_release
+++ b/make_release
@@
 make without_answers && cp hw.pdf release
 cp README.md release
+cp rubric.md release
```

### 4d. `rubric.md` — NEW file (full content of §2 above; shipped to students)

```diff
--- /dev/null
+++ b/rubric.md
@@
+# HW8 — Grading rubric (Gaussian / Beta derivations; written)
+
+No autograder — written derivations. Grading replaces the 1/0.5/0 gate with per-step partial
+credit. Written/derivation-HW split **60 / 30 / 10** (correctness human-verified; see the
+repo-root `rubric.md`).
+
+## §2a · Correctness (60) — per-step derivation rubric
+
+Four exercises; each scored on the **validity of the move**, not on matching this key's exact
+algebra. **Any sound route to each result earns full credit.** Tiers map to a fraction of each
+exercise's points (3→100%, 2→80%, 1→45%, 0→0%). E4 heaviest; E2 lightest.
+
+| Exercise | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
+|----------|-----|:---:|---------------|----------------|----------------|---|
+| **E1 · diagonal Σ ⇒ independence** | O1 | 16 | `\|Σ\|=∏σ_d²`, `Σ⁻¹=diag(1/σ_d²)`, expand quadratic form, exp-of-sum=product, factor into `∏` univariate Gaussians, name independence | product reached, one step asserted | substitutes det/inverse, can't factor | missing |
+| **E2 · MLE unbiased** | O2 | 12 | `E[r̂]=E[Σxᵢ/N]`, pull `1/N`, linearity, `E[xᵢ]=r`, `=r`; states definition | a step asserted | sets up, can't finish | missing |
+| **E3 · Beta mean** | O3 | 14 | `∫ r·p(r)dr`, `α→α+1`, normalization identity, `Γ(n+1)=nΓ(n)` → `α/(α+β)` | minor slip | sets up integral, can't apply identity | missing |
+| **E4 · Beta variance** | O4 | 18 | `E[r²]` (`α→α+2`, Γ identity) → `α(α+1)/((α+β)(α+β+1))`, then `E[r²]−(E[r])²` → `αβ/((α+β)²(α+β+1))` | `E[r²]` right, final slip | sets up `E[r²]`, can't finish | missing |
+
+**Load-bearing vs. independent.** E1/E2/E3 are mutually independent — grade in isolation. E4
+depends on E3's `E[r]`; grade E4 on the student's own `E[r]` (an E3 error caps E4's value, not
+its method). Load-bearing insights: E1 = exp-of-sum→product factorization; E3/E4 = recognizing
+the unnormalized-Beta integral and applying the normalization identity.
+
+## §2b · Interpretation (30) — Claim / Evidence / Reasoning / Limits (0–3 each)
+
+The required paragraph. PASS = ≥2 every dimension.
+
+| Dim | 3 | 2 | 1 | 0 |
+|-----|---|---|---|---|
+| **Claim** | `α/(α+β)` is the prior mean; variance shrinks as `α+β` grows | mostly | direction confused | missing |
+| **Evidence** | the two derived formulas — `α=β`⇒mean `1/2`; large `α+β`⇒small variance | some | vague | none |
+| **Reasoning** | `α+β` as prior sample size (`α`/`β` pseudo successes/failures); Beta = conjugate prior for the Bernoulli rate | thin | superficial | absent |
+| **Limits** | `α,β>0` (proper); `α+β→∞`⇒prior dominates; `α,β→0`⇒improper/U-shaped | one weakly | minimal | none |
+
+## §2c · Process (10)
+
+| Sub-dim | Pts | Full credit when… |
+|---------|:---:|-------------------|
+| Stated identities/assumptions | 4 | diagonal det/inverse, `Γ(n+1)=nΓ(n)`, linearity, i.i.d. named |
+| Notation | 3 | `Σ`, `μ`, `r̂`, `α`, `β`, `E`, `var` defined/consistent |
+| Justification clarity | 3 | each line follows; legible |
+
+**LLM pre-grading** may draft scores + one-line reasons; a human confirms and is final.
+(LLM pre-grading is weak on derivations — humans grade E1–E4.)
```

### 4e. Autograder wiring (written-only — neutralize, don't orphan)

hw8 has **no `test_hw.py` and no `requirements.txt`** (identical to hw7/hw9). Fix is the
already-drafted **conditional `shared/classroom.yml`** (gate pytest + reporter on
`[ -f test_hw.py ]`, add a written-only branch) — cluster-wide (hw7/8/9/12/13), **not** a
per-assignment `hw8/` diff. Recorded so the written HW isn't orphaned with a red autograder.

---

## 5. Effort & budget

| Component | Change vs. current |
|-----------|--------------------|
| Four derivations | unchanged (already complete & correct; ~45–60 min) |
| Interpretation paragraph | **+~15 min** (new) |
| Net | within 5–6 hrs/week — hw8 is a moderate written HW |

The derivations are already minimal and correct, so there is **no busywork to trim**; the +15
min interpretation load is small. The optional non-Gaussian counterexample (§7) stays ungraded.

---

## 6. Judgment calls beyond the spec

1. **DERIVATION, not interpretation (STEP 0).** Four "Show/Derive" tasks → per-step Correctness
   (60). The interpretation row (30) rides on the Beta-as-conjugate-prior reading of the Ex3/Ex4
   results — genuinely Evaluate-level and forward-linking (hw11/hw12), **not** forced.
2. **Typst `#answer` is the strip boundary** (same call as hw7/hw9): all solution edits inside
   the first argument; validated by simulation, not compiled.
3. **Four exercises = four Correctness rows** (E1–E4), weighted `16/12/14/18`, E4 heaviest (builds
   on E3 + most algebra), E2 lightest (short linearity argument). Any split summing to 60 with E4
   dominant and E2 light is fine.
4. **Reference derivations left intact** — already correct; only the two framing blocks are added.
   Minimal source churn (contrast hw9, where the reference derivation itself was polished).
5. **One interpretation paragraph anchored on the Beta thread** (synthesizes two of the four
   results and links forward), rather than four scattered mini-interpretations — keeps the CERL
   paragraph coherent. The Ex1 "uncorrelated⇒independent is Gaussian-special" point is offered as
   the optional §7 extension instead of a second graded paragraph.
6. **hw5 through-line kept** in Ex2's prompt and echoed in the interpretation (Beta prior over the
   same Bernoulli rate `r`).
7. **`make_release` ships `rubric.md`**; autograder neutralization flagged at the `classroom.yml`
   level (§4e), shared with hw7/9/12/13.

---

## 7. Validation results (no PDF compile, per the format note)

Ran the proposed `hw.typ` through the **strip simulator** (`show_answers=false`: balanced-bracket
parse of `#answer(arg1, arg2)` → keep `arg2`), after confirming it reproduces a clean baseline on
the **unmodified** file.

- **Baseline (current `hw.typ`):** ✅ all four reference derivations stripped; all four exercise
  headings, Workload, Acknowledgments retained; 4 `#answer(` blocks; imports + `#show: info521`
  retained. (The two new prompts are correctly *absent* from the baseline.)
- **Strip check — solution content ABSENT from the released doc:** ✅ the E1 factorization
  conclusion, the E2 concise proof, the E3 Beta-mean integral, the E4 variance result, **and** the
  new reference-interpretation paragraph are all stripped.
- **Student framing RETAINED:** ✅ all four exercise headings, the new Allowed-approaches note, the
  new Required-interpretation prompt, Workload, Acknowledgments.
- **Structural:** ✅ exactly **5** `#answer(` blocks in source (4 original + 1 new reference
  interpretation), all stripped; imports intact; `#show: info521` retained.

(No `pytest` — written HW. No `.typ` compile — per the format note.)

---

## 8. Proposed commit message (when applied — do NOT commit now)

```
hw8 overhaul: per-step + CERL rubric for the Gaussian/Beta derivations (written)

- hw.typ: add a global Allowed-approaches note + a Required-interpretation prompt
  with a reference-interpretation #answer block (Beta as conjugate prior; alpha,beta
  as prior sample size; alpha,beta>0 limit). All four original derivations are
  unchanged. Every solution stays in an #answer first argument so
  `make without_answers` strips it.
- rubric.md (new): per-step derivation rubric (Correctness 60 — E1/E2/E3/E4 scored
  on move-validity, any valid route = full credit) + CERL interpretation (30) +
  Process (10). Shipped to students (TILT).
- README.md: 8-part framing; criteria-up-front specs table (replaces 1/0.5/0).
- make_release: ship rubric.md.

Preserves the hw5 through-line (Ex2: the HW5 MLE is unbiased; interpretation ties
the Beta prior to the same Bernoulli rate r). Written/derivation split 60/30/10 per
repo canon. Typst #answer(...) is the strip boundary (no %%% markers); strip
validated by simulation, not compiled.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
