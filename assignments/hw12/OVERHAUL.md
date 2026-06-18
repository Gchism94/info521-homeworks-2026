# hw12 — Overhaul draft (written-derivation pattern · Typst · Inverse-Gamma conjugacy)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw12 ("Prior on noise variance σ²" — Inverse-Gamma
conjugacy). Matches the **hw5 / hw9 written-derivation pilots**. **Draft only — no hw12 files are
modified; the diffs below are proposed, not applied.**

**Split: written/derivation → 60 / 30 / 10** (repo canon; correctness human-verified).
**No pytest** — the "Correctness" layer is a per-step derivation rubric.

> **STEP 0 — classification.** A single *"Derive the parameters for the posterior…"* task →
> **DERIVATION** (multi-step → result), so Correctness is a **per-step rubric**, not CERL. The
> interpretation layer is *not* forced (the hw11 lesson): the result is a **conjugate update**,
> and reading `α', β'` as prior pseudo-data incremented by the data's sufficient statistics is
> the canonical Evaluate-level interpretation of exactly this result — and it ties back to the
> Beta–Bernoulli conjugacy in hw8. So a CERL Interpretation row (30) is legitimate.

> **Marker reconciliation (Typst, same as hw7/8/9).** hw12 is **Typst** (`hw.typ`). Strip = the
> `#answer([sol], [blank])` macro toggled by `make without_answers` (`--input show_answers=false`),
> which renders only the *second* argument. The **`#answer(...)` first argument is the answer
> marker**. All solution edits stay inside it; the strip was validated by simulation (§7), not
> compiled (format note).

> **Reference-key bug fixed (judgment call, flagged).** The existing solution has a **sign typo**:
> the intermediate line currently reads `(σ²)^(−(α − D/2) − 1)`, but the surrounding lines and the
> boxed result correctly have `α + D/2`. Since this is the grading key, the one intermediate `− D/2`
> is corrected to `+ D/2` (inside `#answer`, so stripped from the release but right for grading).

---

## 1. Prompt rewritten into the 8-part template (markdown)

> Authored here and mirrored into `README.md` (§4b). In `hw.typ` only two student-facing blocks
> (an Allowed-approaches note + the Required-interpretation prompt) are added outside `#answer`.

**1. Context & purpose.** In the Olympics regression you treated the noise variance `σ²` as
known. Here you do the Bayesian thing instead: put an Inverse-Gamma prior on `σ²` and update it
with data. Because the Inverse-Gamma is **conjugate** to the Gaussian likelihood (with `w` known),
the posterior stays Inverse-Gamma — you only have to find its two parameters. This is the same
conjugate-update logic as the Beta prior on a probability (hw8), now for a variance.

**2. Learning objectives** (Bloom verb + the rubric row each is measured by):
- **O1** *Set up* posterior ∝ likelihood × prior and recognize the Inverse-Gamma conjugacy.
  *(Understand/Apply — Correctness A)*
- **O2** *Form* the product and isolate the `σ²`-dependent factors (drop constants).
  *(Apply — Correctness B)*
- **O3** *Derive* the shape `α' = α + D/2` via the determinant/power bookkeeping.
  *(Analyze — Correctness C)*
- **O4** *Derive* the scale `β' = β + ½(t−Xw)ᵀ(t−Xw)` by combining the exponentials.
  *(Analyze — Correctness D)*
- **O5** *Interpret* the update — sufficient statistics, prior-as-pseudo-data, the conjugacy
  pattern. *(Evaluate — Interpretation)*

**3. The task (outcome, not recipe).** Derive the posterior parameters: the posterior is
`IG(α', β')` with `α' = α + D/2` and `β' = β + ½(t−Xw)ᵀ(t−Xw)`.

**4. Allowed approaches.** **Any mathematically valid route earns full credit** — kernel-matching
(collect the `σ²`-dependent factors and read off the Inverse-Gamma form) or direct normalizing-
constant integration. State your assumptions (`w` known, noise covariance `σ²I`, `D` = number of
data points) and which factors you drop as constants in `σ²`. A bare final answer earns only the
result step.

**5. How you'll be assessed (criteria shown up front).**
- *Correctness (60%)* — the per-step rubric in §2a (A setup → B product/constants → C `α'` → D
  `β'`), each scored on the **validity of the move**, full credit for any sound route.
- *Interpretation (30%)* — the §6 paragraph, scored Claim/Evidence/Reasoning/Limits.
- *Process (10%)* — assumptions stated, notation/dimensions tracked, justification legible.
- *Specs bundle:* "Derivation = PASS" needs A–D each ≥ Proficient; "Interpretation = PASS" needs
  ≥2 on every CERL dimension; else one revise-and-resubmit.

**6. Required interpretation** (one short paragraph, no new algebra): what do `α' = α + D/2` and
`β' = β + ½(t−Xw)ᵀ(t−Xw)` say about how the data revises the prior belief in the noise variance?
**Identify the data quantities that enter (the sufficient statistics)**, explain **in what sense
`α` and `β` act like "prior data,"** and name **one assumption/limiting case** the result relies on.

**7. Going further (optional, ungraded).** Write the posterior mean of `σ²` as `β'/(α'−1)` and
show how it interpolates between the prior guess and the data's `SSE/D` — i.e. how the estimate
shifts toward the data as `D` grows.

**8. Submission contract.** Written derivation, hard copy as today (the written cluster keeps its
medium; only the *grading* changes). Keep Workload + Acknowledgments. The only build contract is
that the solution stays inside the `#answer([…], [])` first argument so `make without_answers`
strips it.

---

## 2. `hw12/rubric.md` — per-step derivation rubric (NO pytest)

### 2a. Correctness (60) — per-step derivation rubric

One derivation, four major logical steps; **each scored on the validity of the move, not on
matching the reference's exact algebra.** Any sound alternative route (e.g. direct integration of
the normalizing constant) earns full credit. Each step gets a 0–3 tier mapping to a fraction of
its points (3→100%, 2→80%, 1→45%, 0→0%). Weights sum to 60; **C and D heaviest** (they produce the
two posterior parameters).

| Step | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
|------|-----|:---:|---------------|----------------|----------------|---|
| **A · Setup / conjugacy** | O1 | 12 | writes posterior ∝ Gaussian likelihood × IG prior; states that conjugacy ⇒ posterior is `IG(α',β')`; goal = match the kernel | right with a minor gap | posterior ∝ lik×prior only, conjugacy not named | missing/wrong |
| **B · Product & constants** | O2 | 12 | forms the product, identifies factors **not** depending on `σ²` (`1/(2π)^{D/2}`, `βᵃ/Γ(α)`) as constants, keeps the `σ²`-kernel | right, one constant misclassified | forms product but doesn't separate constants | missing/wrong |
| **C · Shape `α'`** | O3 | 18 | `\|σ²I\| = σ^{2D}` ⇒ `σ^{−D}`; combines `σ^{−D}·(σ²)^{−α−1} = (σ²)^{−(α+D/2)−1}` ⇒ `α' = α + D/2` | result right, a power-bookkeeping slip | gets `σ^{−D}` but can't combine | missing/wrong |
| **D · Scale `β'`** | O4 | 18 | combines `exp{−½(t−Xw)ᵀ(t−Xw)/σ²}·exp{−β/σ²}` ⇒ `β' = β + ½(t−Xw)ᵀ(t−Xw)`, reads off `IG(α',β')` | result right, minor slip | combines exps but can't read off `β'` | missing/wrong |

**Load-bearing vs. independent:**
- **A is load-bearing** — a wrong likelihood/prior pairing or mis-stated conjugacy caps the whole
  result — but the *route* is free (kernel-match or integrate).
- **C and D are the two independent payoff moves** (shape from the power bookkeeping, scale from
  the exponent combine): grade each on the student's *own* line-B kernel. An error in B caps the
  final values, **not** C's and D's method credit, and C and D are gradeable in isolation.
- **Within C the load-bearing sub-step is the determinant fact** `\|σ²I\| = σ^{2D}`; award it even
  if the subsequent `+D/2` bookkeeping slips.

### 2b. Interpretation (30) — Claim / Evidence / Reasoning / Limits (0–3 each)

The §6 paragraph (12 raw → 30%). PASS = ≥2 every dimension.

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | the data **increments** the prior: shape `+D/2`, scale `+½·SSE`; posterior stays Inverse-Gamma | mostly right, minor gap | direction/role confused | missing |
| **Evidence** | names the sufficient statistics — the **count `D`** and the **residual SSE `(t−Xw)ᵀ(t−Xw)`**; optionally the posterior mean `β'/(α'−1)` | one of them | vague | none |
| **Reasoning** | reads `α, β` as **prior pseudo-data** (pseudo-count / pseudo-SSE); connects to conjugacy as a pattern (prior family in → same family out; cf. Beta–Bernoulli, hw8) | sound but thin | superficial | absent/wrong |
| **Limits** | names a real condition: `α,β>0` (proper IG); `w` assumed known; i.i.d. Gaussian noise `σ²I`; behavior as `D→∞` | one weakly | minimal | none |

### 2c. Process (10) — assumptions, notation/dimensions, clarity

| Sub-dim | Pts | Full credit when… |
|---------|:---:|-------------------|
| **Stated assumptions** | 4 | `w` known, noise covariance `σ²I`, `D` = number of data points, `α,β>0` made explicit |
| **Notation / dimensions** | 3 | `σ²`, `α'`, `β'`, `t`, `X`, `w`, `I` defined; dimensions tracked (the `\|σ²I\|=σ^{2D}` step) |
| **Justification clarity** | 3 | each line follows from the previous; legible |

---

## 3. Objective → rubric-row map (alignment contract)

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| **O1** setup / conjugacy | Understand/Apply | Correctness **A** | ✅ |
| **O2** product & constants | Apply | Correctness **B** | ✅ |
| **O3** shape `α'` | Analyze | Correctness **C** | ✅ |
| **O4** scale `β'` | Analyze | Correctness **D** | ✅ |
| **O5** interpret the update | Evaluate | **Interpretation** rubric (CERL) | ✅ |
| *(communication)* | — | **Process** rubric (2c) | ✅ (cross-cutting, not an O#) |

**Every objective maps to a rubric row; none unmeasurable.** Process is the standard
objective-free communication layer (dimension-tracking folds in here — central to this derivation).

---

## 4. Proposed unified diffs (per file — NOT applied)

### 4a. `hw.typ` — add framing (outside `#answer`); fix the reference-key sign typo (inside `#answer`)

The derivation is otherwise complete and is **not rewritten**. Two student-facing blocks are added
outside any `#answer` (Allowed-approaches note + Required-interpretation prompt with a reference
`#answer` block), and one intermediate sign typo is corrected inside the existing `#answer`. No
imports, headings, or the original `#answer` boundary are disturbed.

```diff
--- a/hw.typ
+++ b/hw.typ
@@
 then the posterior over $sigma^2$ will also be Inverse Gamma. Derive the
 parameters for the posterior belief in the variance.
+
+#strong[Allowed approaches.] Any mathematically valid route to the posterior
+parameters earns full credit — kernel-matching (collect the $sigma^2$-dependent
+factors and read off the Inverse-Gamma form, as sketched) or a direct
+normalizing-constant integration. State the assumptions you use (here
+$upright(bold(w))$ is known, the noise covariance is $sigma^2 upright(bold(I))$,
+and $D$ is the number of data points) and which factors you drop as constants in
+$sigma^2$. A bare final answer earns only the result step. Grading criteria are in
+#emph[rubric.md].

 #answer(
   [
 #strong[Solution.] ⋯ (derivation unchanged except the one fix below) ⋯
@@  (intermediate line — reference-key sign typo)  @@
- & prop & (sigma^2)^(- (alpha - D \/ 2) - 1) exp {- frac((1 / 2 (...))+ beta, sigma^2)} .
+ & prop & (sigma^2)^(- (alpha + D \/ 2) - 1) exp {- frac((1 / 2 (...))+ beta, sigma^2)} .
   ],
   []
 )
@@  (after the solution #answer block, before "= Workload")  @@
+= Interpretation
+<interpretation>
+#strong[Required interpretation.] After deriving $alpha'$ and $beta'$, add
+#emph[one short paragraph] (no new algebra): what do the updates
+$alpha' = alpha + D slash 2$ and
+$beta' = beta + 1/2 (bold(t) - bold(X) bold(w))^tack.b (bold(t) - bold(X) bold(w))$
+say about how the data revises the prior belief in the noise variance? Identify
+the data quantities that enter (the sufficient statistics), explain in what sense
+$alpha$ and $beta$ act like "prior data," and name one assumption or limiting case
+the result relies on.
+
+#answer(
+  [
+    #strong[Reference interpretation.] Conjugacy means the posterior is again
+    Inverse-Gamma, with the parameters simply incremented by the data's sufficient
+    statistics: the shape gains $D slash 2$ (half a unit per observation) and the
+    scale gains half the residual sum of squares
+    $1/2 (bold(t) - bold(X) bold(w))^tack.b (bold(t) - bold(X) bold(w))$. So
+    $alpha$ and $beta$ act like #emph[prior pseudo-data] — a prior count and a
+    prior sum-of-squared-errors — and observing $D$ residuals adds the real count
+    and the real SSE on top. The posterior mean of the variance,
+    $beta' slash (alpha' - 1)$, therefore sits between the prior guess and the
+    data's $"SSE" slash D$, shifting toward the data as $D$ grows. This is the same
+    conjugate-update pattern as the Beta--Bernoulli prior (HW8): prior family in,
+    same family out, parameters moved by sufficient statistics. It relies on
+    $alpha, beta > 0$ (a proper Inverse-Gamma) and on the exercise's setup that
+    $upright(bold(w))$ is known and the noise is i.i.d. Gaussian with covariance
+    $sigma^2 upright(bold(I))$; if $upright(bold(w))$ were also unknown the simple
+    one-parameter conjugacy would no longer apply.
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
+# HW12 — Prior on the noise variance σ² (Inverse-Gamma conjugacy)
+
+> Overhauled (written-derivation pattern). Grading is **per-step + specifications-based**, not
+> the old complete/incomplete gate. The full rubric ships in `rubric.md`.
+
+## 1. Context & purpose
+
+Instead of treating the noise variance `σ²` as known, put an Inverse-Gamma prior on it and update
+with data. The Inverse-Gamma is conjugate to the Gaussian likelihood (with `w` known), so the
+posterior stays Inverse-Gamma — you only find its two parameters. Same conjugate-update logic as
+the Beta prior on a probability (hw8), now for a variance.
+
+## 2. Learning objectives
+
+- **O1** Set up posterior ∝ likelihood × prior; recognize the Inverse-Gamma conjugacy. *(Correctness A)*
+- **O2** Form the product and isolate the `σ²`-dependent factors. *(Correctness B)*
+- **O3** Derive the shape `α' = α + D/2`. *(Correctness C)*
+- **O4** Derive the scale `β' = β + ½(t−Xw)ᵀ(t−Xw)`. *(Correctness D)*
+- **O5** Interpret the update (sufficient statistics, prior-as-pseudo-data, conjugacy). *(Interpretation)*
+
+## 3. The task
+
+Derive the posterior parameters: `IG(α', β')` with `α' = α + D/2`, `β' = β + ½(t−Xw)ᵀ(t−Xw)`.
+
+## 4. Allowed approaches
+
+**Any mathematically valid route earns full credit** — kernel-matching or direct normalizing-
+constant integration. State your assumptions (`w` known, noise covariance `σ²I`, `D` = data count)
+and which factors you drop as constants in `σ²`. A bare final answer earns only the result step.
+
+## 5. How you'll be assessed (criteria shown up front)
+
+| Bundle | Weight | Pass when… |
+|--------|:------:|------------|
+| **Correctness** | **60%** | per-step rubric (`rubric.md` §2a) — A (setup/conjugacy), B (product/constants), C (shape `α'`), D (scale `β'`) each at **Proficient+**. Any sound route counts. |
+| **Interpretation** | **30%** | the required paragraph reaches **Proficient+** on every Claim/Evidence/Reasoning/Limits dimension (`rubric.md` §2b). |
+| **Process** | **10%** | assumptions stated, dimensions tracked, legible justification (`rubric.md` §2c). |
+
+**Revision:** one revise-and-resubmit per bundle that falls short. An LLM may draft scores; a
+human confirms and is final.
+
+## 6. Submission
+
+Write up the derivation **and** the required interpretation paragraph; submit a hard copy at the
+start of class on the due date. Record your time in the Workload section.
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
+# HW12 — Grading rubric (Inverse-Gamma conjugacy; written derivation)
+
+No autograder — a written derivation. Grading replaces the 1/0.5/0 gate with per-step partial
+credit. Written/derivation-HW split **60 / 30 / 10** (correctness human-verified; see the
+repo-root `rubric.md`).
+
+## §2a · Correctness (60) — per-step derivation rubric
+
+One derivation, four major moves; each scored on the **validity of the move**, not on matching
+this key's exact algebra. **Any sound route earns full credit** (kernel-match or direct
+integration). Tiers map to a fraction of each step's points (3→100%, 2→80%, 1→45%, 0→0%). C and D
+heaviest (they produce the two parameters).
+
+| Step | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
+|------|-----|:---:|---------------|----------------|----------------|---|
+| **A · Setup / conjugacy** | O1 | 12 | posterior ∝ Gaussian lik × IG prior; conjugacy ⇒ posterior `IG(α',β')`; goal = match kernel | minor gap | lik×prior only, conjugacy unnamed | missing |
+| **B · Product & constants** | O2 | 12 | forms product; drops `σ²`-free factors (`1/(2π)^{D/2}`, `βᵃ/Γ(α)`); keeps `σ²`-kernel | one constant misclassified | doesn't separate constants | missing |
+| **C · Shape `α'`** | O3 | 18 | `\|σ²I\|=σ^{2D}` ⇒ `σ^{−D}`; combine to `(σ²)^{−(α+D/2)−1}` ⇒ `α'=α+D/2` | power-bookkeeping slip | gets `σ^{−D}`, can't combine | missing |
+| **D · Scale `β'`** | O4 | 18 | combine exponentials ⇒ `β'=β+½(t−Xw)ᵀ(t−Xw)`; read off `IG(α',β')` | minor slip | combines exps, can't read off `β'` | missing |
+
+**Load-bearing vs. independent.** A is load-bearing (wrong lik/prior pairing or conjugacy caps the
+result) but route-free. C and D are two independent payoff moves graded on the student's own
+line-B kernel — a B error caps the values, not C/D method credit. Within C the load-bearing
+sub-step is the determinant fact `\|σ²I\|=σ^{2D}`.
+
+## §2b · Interpretation (30) — Claim / Evidence / Reasoning / Limits (0–3 each)
+
+The required paragraph. PASS = ≥2 every dimension.
+
+| Dim | 3 | 2 | 1 | 0 |
+|-----|---|---|---|---|
+| **Claim** | data increments the prior: shape `+D/2`, scale `+½·SSE`; posterior stays IG | mostly | role confused | missing |
+| **Evidence** | the sufficient statistics — count `D` and residual SSE `(t−Xw)ᵀ(t−Xw)`; opt. mean `β'/(α'−1)` | one | vague | none |
+| **Reasoning** | `α,β` as prior pseudo-data; conjugacy pattern (prior family in → same out; cf. Beta–Bernoulli hw8) | thin | superficial | absent |
+| **Limits** | `α,β>0` (proper IG); `w` known; i.i.d. `σ²I` noise; `D→∞` behavior | one weakly | minimal | none |
+
+## §2c · Process (10)
+
+| Sub-dim | Pts | Full credit when… |
+|---------|:---:|-------------------|
+| Stated assumptions | 4 | `w` known, noise `σ²I`, `D` = data count, `α,β>0` explicit |
+| Notation / dimensions | 3 | symbols defined; dimensions tracked (`\|σ²I\|=σ^{2D}`) |
+| Justification clarity | 3 | each line follows; legible |
+
+**LLM pre-grading** may draft scores + one-line reasons; a human confirms and is final.
+(LLM pre-grading is weak on derivations — humans grade A–D.)
```

### 4e. Autograder wiring (written-only — neutralize, don't orphan)

hw12 has **no `test_hw.py` and no `requirements.txt`** (identical to hw7/8/9). Fix is the
already-drafted **conditional `shared/classroom.yml`** (gate pytest + reporter on
`[ -f test_hw.py ]`, add a written-only branch) — cluster-wide (hw7/8/9/12/13), **not** a
per-assignment `hw12/` diff. Recorded so the written HW isn't orphaned with a red autograder.

---

## 5. Effort & budget

| Component | Change vs. current |
|-----------|--------------------|
| Derivation | unchanged (~30–45 min; one multi-step derivation) |
| Interpretation paragraph | **+~15 min** (new) |
| Net | within 5–6 hrs/week — hw12 is a moderate written HW |

The derivation is already complete (only a one-character key fix), so there is **no busywork to
trim**; the +15 min interpretation load is small. The optional posterior-mean extension (§7) stays
ungraded.

---

## 6. Judgment calls beyond the spec

1. **DERIVATION, not interpretation (STEP 0).** A single multi-step "Derive the parameters" task →
   per-step Correctness (60). The interpretation row (30) rides on the conjugate-update reading
   (sufficient statistics, prior-as-pseudo-data) — genuinely Evaluate-level and tied back to hw8,
   **not** forced.
2. **Reference-key sign typo fixed.** The intermediate `(σ²)^(−(α − D/2) − 1)` is corrected to
   `+ D/2` to match the surrounding lines and the boxed result. One-character fix inside `#answer`;
   stripped from the release but correct for grading. **Flagged for your confirmation.**
3. **Typst `#answer` is the strip boundary** (same call as hw7/8/9): all edits inside the first
   argument; validated by simulation, not compiled.
4. **Four steps for one derivation**, weighted `12/12/18/18` with C and D heaviest (they produce
   `α'` and `β'`). Any split summing to 60 with C/D dominant is fine.
5. **Reference derivation left intact** apart from the typo — only the two framing blocks are added.
   Minimal source churn.
6. **Through-line to hw8 (and forward to the Bayesian-inference HWs)** made explicit in the
   interpretation: the Beta–Bernoulli conjugate update is the same pattern as this Inverse-Gamma
   update.
7. **`make_release` ships `rubric.md`**; autograder neutralization flagged at the `classroom.yml`
   level (§4e), shared with hw7/8/9/13.

---

## 7. Validation results (no PDF compile, per the format note)

Ran the proposed `hw.typ` through the **strip simulator** (`show_answers=false`: balanced-bracket
parse of `#answer(arg1, arg2)` → keep `arg2`), after confirming it reproduces a clean baseline on
the **unmodified** file.

- **Baseline (current `hw.typ`):** ✅ the reference derivation (conjugacy framing, the `α'` result,
  the determinant fact) stripped; title, problem statement, Workload, Acknowledgments retained; 1
  `#answer(` block; imports + `#show: info521` retained. (The two new prompts are correctly *absent*
  from the baseline.)
- **Strip check — solution content ABSENT from the released doc:** ✅ the conjugacy framing, the
  `α' = α + D/2` result line, the determinant fact `\|σ²I\| = σ^{2D}`, **and** the new
  reference-interpretation paragraph are all stripped.
- **Student framing RETAINED:** ✅ title, problem statement (with the IG prior), the new
  Allowed-approaches note, the new Required-interpretation prompt (verified by a second probe
  after a needle-wrap artifact), Workload, Acknowledgments.
- **Structural:** ✅ exactly **2** `#answer(` blocks in source (1 original + 1 new reference
  interpretation), all stripped; the sign-typo fix confirmed present; imports intact;
  `#show: info521` retained.

(No `pytest` — written HW. No `.typ` compile — per the format note.)

---

## 8. Proposed commit message (when applied — do NOT commit now)

```
hw12 overhaul: per-step + CERL rubric for Inverse-Gamma conjugacy (written)

- hw.typ: rewrite the prompt to the 8-part template — add an Allowed-approaches
  note (any valid route: kernel-match or integrate) and a Required-interpretation
  prompt, both outside #answer; replaces the 1/0.5/0 gate. Fix a reference-key
  sign typo (intermediate (sigma^2)^(-(alpha - D/2) - 1) -> (alpha + D/2), matching
  the boxed result).
- rubric.md (new): written-derivation split 60/30/10. Correctness 60 = per-step
  A/B/C/D = 12/12/18/18 (C shape alpha', D scale beta' the two heavy independent
  payoffs; A load-bearing for the values, route-free; determinant fact |sigma^2 I|
  = sigma^(2D) the load-bearing sub-step in C). Interpretation 30 = CERL; Process 10.
- source churn: only the two framing blocks added + the one-character typo fix;
  the derivation is otherwise intact. All solution/answer edits stay inside the
  #answer first argument (Typst strip boundary), so `make without_answers` strips
  them; the two prompts sit outside and are retained.
- through-line: interpretation ties this Inverse-Gamma update to the Beta-Bernoulli
  conjugate update (HW8) — prior family in, same family out, parameters moved by
  sufficient statistics.
- make_release: also copies rubric.md into release (TILT). Autograder: written-only
  (no test_hw.py) — skip pytest via the shared conditional classroom.yml; nothing
  to time.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
