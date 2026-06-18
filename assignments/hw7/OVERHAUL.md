# hw7 — Overhaul draft (written-derivation pattern · Typst · matrix-calculus identities)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw7 ("Practice with Jacobians"). Matches the
**hw5 / hw9 written-derivation pilots**. **Draft only — no hw7 files are modified; the diffs
below are proposed, not applied.**

**Split: written/derivation → 60 / 30 / 10** (repo canon; correctness human-verified).
**No pytest** — the "Correctness" layer is a per-step derivation rubric.

> **STEP 0 — classification.** All three exercises are *"Show that …"* prove-an-identity tasks
> → **DERIVATION** (steps → result), so Correctness is a **per-step rubric**, not CERL. The
> interpretation layer is *not* forced onto a mechanical task (the hw11 lesson): the document
> itself (lines 114–117) raises a genuine conceptual point — the numerator/denominator **layout
> convention**, the transpose bookkeeping that reconciles "gradient as a column" with "Jacobian
> as a row," and the **downstream uses** (Newton-Raphson update for Bayesian logistic
> regression; Hessian of the linear-Gaussian log-likelihood). That is a real Evaluate-level
> question, so a *light* CERL Interpretation row (30) is legitimate, not manufactured.

> **Marker reconciliation (Typst, same as hw9).** hw7 is **Typst** (`hw.typ`), not LaTeX. Its
> strip mechanism is the `#answer([solution], [blank])` macro toggled by `make without_answers`
> (`typst compile … --input show_answers=false`), which renders only the *second* argument. So
> the **`#answer(...)` first argument is the answer marker** — the faithful analogue of
> `%%% Answer START/END %%%`. All solution edits stay inside it. Per the format note I did
> **not** compile the `.typ`; the strip was validated by simulation (§7).

---

## 1. Prompt rewritten into the 8-part template (markdown)

> Authored here and mirrored into `README.md` (§4b). In `hw.typ` only the student-facing lines
> (Allowed approaches + Required-interpretation prompt) are added outside `#answer`; the rest of
> the framing lives in `README.md` because the document format is changing.

**1. Context & purpose.** These three Jacobian identities are the matrix-calculus primitives
behind almost every gradient/Hessian you will compute later in the course. They are the matrix
analogues of `dx/dx = 1` and `d(cx)/dx = c`; getting the **layout conventions** straight here
is what later lets you derive the Newton-Raphson update for Bayesian logistic regression and
the Hessian of the linear-Gaussian log-likelihood without sign or shape errors.

**2. Learning objectives** (Bloom verb + the rubric row each is measured by):
- **O1** *Compute* the Jacobian of a vector with respect to itself and show it equals `I`.
  *(Apply — Correctness exercise E1)*
- **O2** *Establish* the transpose relation `∂/∂wᵀ f = (∂f/∂w)ᵀ` for a scalar `f`.
  *(Apply/Analyze — Correctness E2)*
- **O3** *Derive* `∂/∂wᵀ (Cw) = C` via entrywise expansion and the Kronecker delta.
  *(Analyze — Correctness E3)*
- **O4** *Connect* the identities to the layout conventions and downstream uses (Newton-Raphson,
  the linear-Gaussian Hessian) and name an assumption they rest on. *(Evaluate — Interpretation)*

**3. The task (outcome, not recipe).** Prove the three identities: (1) `∂w/∂w = I`;
(2) for scalar `f(w)`, `∂/∂wᵀ f = (∂f/∂w)ᵀ`; (3) `∂/∂wᵀ (Cw) = C`.

**4. Allowed approaches.** **Any mathematically valid route to each identity earns full credit
— no canonical path is privileged.** Entrywise expansion with the Kronecker delta, differential
calculus (`d(Aw) = A dw`), or a stated-and-justified matrix-calculus rule are all fine. **State
your layout convention (numerator / denominator) and stay consistent.** A bare final answer
earns only the result step.

**5. How you'll be assessed (criteria shown up front).**
- *Correctness (60%)* — the per-step derivation rubric in §2a (E1 + E2 + E3), each step scored
  on the **validity of the move**, full credit for any sound alternative route.
- *Interpretation (30%)* — the §6 paragraph, scored Claim/Evidence/Reasoning/Limits.
- *Process (10%)* — layout convention stated, Kronecker delta defined, notation consistent,
  justification legible.
- *Specs bundle:* "Derivation = PASS" needs E1–E3 each ≥ Proficient; "Interpretation = PASS"
  needs ≥2 on every CERL dimension; else one revise-and-resubmit.

**6. Required interpretation** (one short paragraph, no new algebra): what role do the layout
and transpose conventions play, and **why does the part-2 transpose relation matter** when
differentiating a scalar objective? Name **where at least one identity is used downstream**
(Newton-Raphson update for Bayesian logistic regression, or the linear-Gaussian Hessian), and
state **one assumption** the part-3 result relies on.

**7. Going further (optional, ungraded).** Redo part 3 in the *denominator* layout and confirm
you get `Cᵀ` instead of `C` — i.e. show explicitly that the result is convention-dependent.

**8. Submission contract.** Written derivation, hard copy as today (the written cluster keeps
its medium; only the *grading* changes). Keep the Workload + Acknowledgments sections. The only
build contract is that every solution stays inside an `#answer([…], [])` first argument so
`make without_answers` strips it.

---

## 2. `hw7/rubric.md` — per-step derivation rubric (NO pytest)

### 2a. Correctness (60) — per-step derivation rubric

Three independent exercises; **each scored on the validity of the move, not on matching the
reference's exact algebra.** Any sound alternative route earns full credit. Each exercise gets a
0–3 tier mapping to a fraction of its points (3→100%, 2→80%, 1→45%, 0→0%). Weights sum to 60;
**E3 is heaviest** (it is the only multi-step derivation).

| Exercise | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
|----------|-----|:---:|---------------|----------------|----------------|---|
| **E1 · `∂w/∂w = I`** | O1 | 12 | writes the Jacobian as the matrix of `∂wᵢ/∂wⱼ`, evaluates to `δᵢⱼ`, concludes `I` | right with a small gap (e.g. `δ` used implicitly) | states entries are 0/1 without the `δᵢⱼ` argument | missing/wrong |
| **E2 · transpose relation** | O2 | 16 | writes `∂/∂wᵀ f` as a **row** of partials, identifies `∂f/∂w` as the **column**, concludes one is the transpose of the other | right but layout/orientation argued loosely | asserts the transpose without showing row vs. column | missing/wrong |
| **E3 · `∂/∂wᵀ(Cw) = C`** | O3 | 32 | expands `(Cw)ᵢ = Σ_d C_{id} w_d`, differentiates entrywise, collapses `Σ_d C_{id} δ_{dj} = C_{ij}`, concludes `C` | result reached, one minor slip (an index, a missing `δ` step) | sets up `Σ_d C_{id} w_d` but cannot carry the `δ` collapse | missing/wrong |

**Load-bearing vs. independent:**
- **E1, E2, E3 are mutually independent** — no exercise uses another's result, so grade each in
  isolation. A wrong E1 does **not** cap E2 or E3.
- **Within E3 the moves chain** (expand → differentiate → Kronecker-collapse → assemble), but
  each move is gradeable on the student's *own* previous line: an upstream index error caps the
  final value, **not** the method credit for the downstream collapse.
- **The Kronecker-delta step is the load-bearing insight of E3** (it is what turns the double
  sum into `C_{ij}`); award it explicitly even if the final assembly slips.

### 2b. Interpretation (30) — Claim / Evidence / Reasoning / Limits (0–3 each)

The §6 paragraph (12 raw → 30%). PASS = ≥2 every dimension.

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | states the identities are matrix analogues of `dx/dx=1`, `d(cx)/dx=c`, and that the part-2 transpose reconciles **gradient-as-column** with **Jacobian-as-row** | mostly right, minor gap | vague "they're useful" | missing |
| **Evidence** | names a concrete downstream use — **Newton-Raphson** update (gradient + Hessian) for Bayesian logistic regression, or the **linear-Gaussian Hessian** | one use, loosely | gestures at "later" | none |
| **Reasoning** | explains *why* the transpose bookkeeping prevents shape/sign errors when differentiating a scalar objective | sound but thin | superficial | absent/wrong |
| **Limits** | names a real condition: **`C` constant in `w`** (part 3 fails otherwise), `f` scalar (part 2), or **result is layout-convention-dependent** | one weakly | minimal | none |

### 2c. Process (10) — conventions, notation, clarity

| Sub-dim | Pts | Full credit when… |
|---------|:---:|-------------------|
| **Layout convention** | 4 | numerator vs. denominator layout **stated** and used consistently across all three parts |
| **Definitions** | 3 | Kronecker delta defined; `C` dimensions (`N×D`) and `w` (`D×1`) given |
| **Justification clarity** | 3 | each line follows from the previous; legible |

---

## 3. Objective → rubric-row map (alignment contract)

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| **O1** `∂w/∂w = I` | Apply | Correctness **E1** | ✅ |
| **O2** transpose relation | Apply/Analyze | Correctness **E2** | ✅ |
| **O3** `∂/∂wᵀ(Cw) = C` | Analyze | Correctness **E3** | ✅ |
| **O4** conventions + downstream use | Evaluate | **Interpretation** rubric (CERL) | ✅ |
| *(communication / conventions)* | — | **Process** rubric (2c) | ✅ (cross-cutting, not an O#) |

**Every objective maps to a rubric row; none unmeasurable.** Process is the standard
objective-free communication layer (layout convention folds in here because it is cross-cutting
across all three exercises). Nothing here is unmeasurable.

---

## 4. Proposed unified diffs (per file — NOT applied)

### 4a. `hw.typ` — add framing (outside `#answer`) + light solution polish (inside `#answer`)

All solution edits stay inside an `#answer([…], [])` first argument (stripped by
`make without_answers`); the prompt lines go outside (always shown). No imports, headings, or
the three original `#answer` strip boundaries are disturbed. The three reference derivations are
already correct — they are **not** rewritten; only an assumptions/notation note is prepended to
E1 and a new reference-interpretation `#answer` block is added.

```diff
--- a/hw.typ
+++ b/hw.typ
@@
 = Practice with Jacobians
+
+#strong[Allowed approaches.] Any mathematically valid route to each requested
+identity earns full credit — entrywise expansion with the Kronecker delta,
+differential calculus ($dif(bold(A) bold(w)) = bold(A) dif bold(w)$), or a known
+matrix-calculus rule you state and justify. State your layout convention
+(numerator / denominator) and stay consistent; show the steps that justify each
+move — a bare final answer earns only the result step. Grading criteria are in
+#emph[rubric.md].

 + Show that $ #jacobian([$bold(w)$], [w]) = bold(I)$, where $bold(I)$ is the
   identity matrix.

 #answer(
   [
-    In this homework solution, I use the compact derivative notation $dvcp(f,x)
-    = dvp(f,x)$ in some places.
+    #strong[Assumptions and notation.] I use the numerator-layout convention
+    (the Jacobian of $bold(w)$ w.r.t. $bold(w)$ has $(i,j)$ entry
+    $partial w_i slash partial w_j$), the Kronecker delta
+    $kdelta(i,j) = 1$ if $i = j$ else $0$, and the compact derivative notation
+    $dvcp(f,x) = dvp(f,x)$ in some places.
     ⋯ (existing E1 derivation unchanged) ⋯
   ],
   []
 )
@@  (E2 and E3 #answer blocks unchanged)  @@
@@
 We will use the first two relations when we derive the Newton-Raphson update
 rule for Bayesian logistic regression with a Gaussian prior (#fcml $section$ 4).
 The third relation was used in class when we computed the Hessian of the
 log-likelihood for the linear model with Gaussian additive noise.
+
+#strong[Required interpretation.] After deriving the three identities, add
+#emph[one short paragraph] (no new algebra): what role do these layout and
+transpose conventions play, and why does the transpose relation in part 2 matter
+when we differentiate a scalar objective? Name where at least one identity is
+used downstream (e.g. the Newton-Raphson update for Bayesian logistic regression,
+or the Hessian of the linear-Gaussian log-likelihood), and state one assumption
+the part-3 result relies on.
+
+#answer(
+  [
+    #strong[Reference interpretation.] These three identities are the matrix
+    analogues of the scalar facts $dif x slash dif x = 1$ and
+    $dif (c x) slash dif x = c$ — part 1 is the vector "derivative of a variable
+    with respect to itself," and part 3 is the linear-map version (a constant
+    $bold(C)$ comes straight out, exactly the #emph[scalar identity] generalized).
+    The part-2 transpose relation matters because two conventions collide: the
+    #emph[gradient] of a scalar objective is naturally a column vector, while the
+    Jacobian $partial slash partial bold(w)^T$ is naturally a row. The identity
+    $partial slash partial bold(w)^T f = (partial f slash partial bold(w))^T$ is
+    exactly the bookkeeping that lets us move between "gradient as a column" and
+    "Jacobian as a row" without sign or shape errors. Downstream, parts 1–2 give
+    the gradient and Hessian terms in the Newton-Raphson update for Bayesian
+    logistic regression with a Gaussian prior (#fcml $section$ 4), and part 3 is
+    the step that produces the Hessian of the linear-Gaussian log-likelihood. The
+    part-3 result $partial slash partial bold(w)^T (bold(C) bold(w)) = bold(C)$
+    relies on $bold(C)$ being #strong[constant] in $bold(w)$ (it fails if
+    $bold(C)$ itself depends on $bold(w)$) and on a fixed layout convention.
+  ],
+  []
+)
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
+# HW7 — Practice with Jacobians
+
+> Overhauled (written-derivation pattern). Grading is **per-step + specifications-based**, not
+> the old complete/incomplete gate. The full rubric ships in `rubric.md`.
+
+## 1. Context & purpose
+
+These three Jacobian identities are the matrix-calculus primitives behind the gradients and
+Hessians used later in the course — the matrix analogues of `dx/dx = 1` and `d(cx)/dx = c`.
+Getting the layout conventions straight here is what later lets you derive the Newton-Raphson
+update for Bayesian logistic regression and the Hessian of the linear-Gaussian log-likelihood.
+
+## 2. Learning objectives
+
+- **O1** Compute `∂w/∂w` and show it equals `I`. *(Correctness E1)*
+- **O2** Establish the transpose relation `∂/∂wᵀ f = (∂f/∂w)ᵀ` for scalar `f`. *(Correctness E2)*
+- **O3** Derive `∂/∂wᵀ (Cw) = C` via the Kronecker delta. *(Correctness E3)*
+- **O4** Connect the identities to the layout conventions and their downstream use. *(Interpretation)*
+
+## 3. The task
+
+Prove: (1) `∂w/∂w = I`; (2) for scalar `f`, `∂/∂wᵀ f = (∂f/∂w)ᵀ`; (3) `∂/∂wᵀ (Cw) = C`.
+
+## 4. Allowed approaches
+
+**Any mathematically valid route to each identity earns full credit** — entrywise expansion
+with the Kronecker delta, differential calculus (`d(Aw) = A dw`), or a stated-and-justified
+matrix-calculus rule. **State your layout convention (numerator/denominator) and stay
+consistent.** A bare final answer earns only the result step.
+
+## 5. How you'll be assessed (criteria shown up front)
+
+| Bundle | Weight | Pass when… |
+|--------|:------:|------------|
+| **Correctness** | **60%** | per-step rubric (`rubric.md` §2a) — exercises E1 (`∂w/∂w=I`), E2 (transpose relation), E3 (`∂/∂wᵀ(Cw)=C`) each at **Proficient+**. Any sound route counts. |
+| **Interpretation** | **30%** | the required paragraph reaches **Proficient+** on every Claim/Evidence/Reasoning/Limits dimension (`rubric.md` §2b). |
+| **Process** | **10%** | layout convention stated, Kronecker delta defined, legible justification (`rubric.md` §2c). |
+
+**Revision:** one revise-and-resubmit per bundle that falls short. An LLM may draft scores; a
+human confirms and is final.
+
+## 6. Submission
+
+Write up the three derivations **and** the required interpretation paragraph; submit a hard copy
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
+# HW7 — Grading rubric (Jacobian identities; written derivation)
+
+No autograder — this is a written derivation. Grading replaces the 1/0.5/0 gate with per-step
+partial credit. Written/derivation-HW split **60 / 30 / 10** (correctness human-verified; see
+the repo-root `rubric.md`).
+
+## §2a · Correctness (60) — per-step derivation rubric
+
+Three independent exercises; each scored on the **validity of the move**, not on matching this
+key's exact algebra. **Any sound route to each identity earns full credit.** Tiers map to a
+fraction of each exercise's points (3→100%, 2→80%, 1→45%, 0→0%). E3 is heaviest.
+
+| Exercise | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
+|----------|-----|:---:|---------------|----------------|----------------|---|
+| **E1 · `∂w/∂w = I`** | O1 | 12 | Jacobian of `∂wᵢ/∂wⱼ` → `δᵢⱼ` → `I` | minor gap (`δ` implicit) | "entries 0/1" without `δ` argument | missing |
+| **E2 · transpose relation** | O2 | 16 | `∂/∂wᵀ f` as a **row**, `∂f/∂w` as the **column**, one is the other's transpose | orientation argued loosely | asserts transpose without row-vs-column | missing |
+| **E3 · `∂/∂wᵀ(Cw) = C`** | O3 | 32 | expand `(Cw)ᵢ=Σ_d C_{id}w_d` → differentiate → `Σ_d C_{id}δ_{dj}=C_{ij}` → `C` | result reached, one index/`δ` slip | sets up sum, can't carry `δ` collapse | missing |
+
+**Load-bearing vs. independent.** E1/E2/E3 are mutually independent — grade each in isolation; a
+wrong E1 does not cap E2 or E3. Within E3 the moves chain, but each is gradeable on the
+student's own previous line; the **Kronecker-delta collapse is the load-bearing insight** —
+award it explicitly even if the final assembly slips.
+
+## §2b · Interpretation (30) — Claim / Evidence / Reasoning / Limits (0–3 each)
+
+The required paragraph. PASS = ≥2 every dimension.
+
+| Dim | 3 | 2 | 1 | 0 |
+|-----|---|---|---|---|
+| **Claim** | analogues of `dx/dx=1`, `d(cx)/dx=c`; transpose reconciles gradient-column ↔ Jacobian-row | mostly | vague "useful" | missing |
+| **Evidence** | a concrete downstream use: Newton-Raphson update, or the linear-Gaussian Hessian | one, loosely | "later" | none |
+| **Reasoning** | *why* the transpose bookkeeping prevents shape/sign errors | thin | superficial | absent |
+| **Limits** | `C` constant in `w` / `f` scalar / result is layout-convention-dependent | one weakly | minimal | none |
+
+## §2c · Process (10)
+
+| Sub-dim | Pts | Full credit when… |
+|---------|:---:|-------------------|
+| Layout convention | 4 | numerator/denominator stated and consistent across all parts |
+| Definitions | 3 | Kronecker delta defined; `C` (`N×D`), `w` (`D×1`) dimensions given |
+| Justification clarity | 3 | each line follows; legible |
+
+**LLM pre-grading** may draft scores + one-line reasons; a human confirms and is final.
+(LLM pre-grading is weak on derivations — humans grade E1–E3.)
```

### 4e. Autograder wiring (written-only — neutralize, don't orphan)

hw7 has **no `test_hw.py` and no `requirements.txt`** (identical to hw9). The shared
`shared/classroom.yml` would run `autograding-python-grader` (pytest) + `pip install -r
requirements.txt` and **fail red** on a written-only repo. The fix is the **already-drafted
conditional `classroom.yml`** (gate the pytest + reporter steps on `[ -f test_hw.py ]`, add a
written-only "submission received" branch) — an infra-level change shared across the whole
written cluster (hw7/8/9/12/13), **not** a per-assignment `hw7/` diff. Recorded here so the
written HW isn't orphaned with a perpetually-red autograder.

---

## 5. Effort & budget

| Component | Change vs. current |
|-----------|--------------------|
| Three derivations | unchanged (already complete & correct; ~30–40 min) |
| Interpretation paragraph | **+~15 min** (new) |
| Net | well within 5–6 hrs/week — hw7 is a short written HW |

The derivations are already minimal and correct, so there is **no busywork to trim**; the +15
min interpretation load is small. The optional denominator-layout extension (§7) stays ungraded.

---

## 6. Judgment calls beyond the spec

1. **DERIVATION, not interpretation (STEP 0).** Three "Show that…" identities → per-step
   Correctness (60). The interpretation row (30) is justified by the document's own
   layout-convention / downstream-use content (lines 114–117), **not** forced onto a mechanical
   task — the hw11 category-error is avoided.
2. **Typst `#answer` is the strip boundary** (same call as hw9): all solution edits inside the
   first argument; validated by simulation, not compiled (format note).
3. **Three exercises = three Correctness rows** (E1/E2/E3), weighted `12/16/32` with E3 heaviest
   (the only multi-step derivation). Any split summing to 60 with E3 dominant is fine.
4. **Reference derivations left intact.** The existing E1–E3 solutions are already correct; I
   only prepend an assumptions/notation note to E1 and add a new reference-interpretation
   `#answer` block — minimal source churn.
5. **8-part prompt authored in `README.md` markdown**, with only the Allowed-approaches and
   Required-interpretation lines added to `hw.typ` (document format changing; rendering deferred).
6. **Target identities shown in the prompt** (they always were — the exercises state them).
   Layout convention surfaced in the prompt (TILT); the *derivations* stay stripped.
7. **`make_release` ships `rubric.md`**; autograder neutralization for the written cluster
   flagged at the `classroom.yml` level (§4e), shared with hw8/9/12/13.

---

## 7. Validation results (no PDF compile, per the format note)

Ran the proposed `hw.typ` through a **strip simulator** that emulates `show_answers=false`
(balanced-bracket parse of `#answer(arg1, arg2)` → keep `arg2`), after confirming the simulator
reproduces a clean baseline on the **unmodified** file.

- **Baseline (current `hw.typ`):** ✅ all three reference derivations stripped; title, exercise
  statements, context note, Workload, Acknowledgments retained; 3 `#answer(` blocks; imports +
  `#show: info521` retained.
- **Strip check — solution content ABSENT from the released doc:** ✅ the E1 compact-notation
  note and partials matrix, the E2 transpose result `(∂f/∂w)ᵀ`, the E3 Kronecker collapse and
  `= C` result, **and** the new in-answer assumptions note + reference-interpretation paragraph
  are all stripped.
- **Student framing RETAINED:** ✅ title, all three exercise statements, the new
  Allowed-approaches prompt, the context note, the new Required-interpretation prompt, Workload,
  Acknowledgments.
- **Structural:** ✅ exactly **4** `#answer(` blocks in source (3 original + 1 new reference
  interpretation), all stripped; imports intact (`common.typ`/`equations.typ`); `#show: info521`
  retained; `#fcml` already used in the original so it resolves.

(No `pytest` — written HW. No `.typ` compile — per the format note.)

---

## 8. Proposed commit message (when applied — do NOT commit now)

```
hw7 overhaul: per-step + CERL rubric for the Jacobian identities (written)

- hw.typ: add Allowed-approaches + Required-interpretation prompts (outside the
  #answer markers); inside #answer, prepend an assumptions/notation note to E1
  and add a reference-interpretation block (layout conventions; Newton-Raphson
  and linear-Gaussian-Hessian downstream uses; C-constant assumption). The three
  original derivations are unchanged. All solution edits stay in an #answer first
  argument so `make without_answers` strips them.
- rubric.md (new): per-step derivation rubric (Correctness 60 — E1/E2/E3 scored
  on move-validity, any valid route = full credit) + CERL interpretation (30) +
  Process (10). Shipped to students (TILT).
- README.md: 8-part framing; criteria-up-front specs table (replaces 1/0.5/0).
- make_release: ship rubric.md.

Written/derivation split 60/30/10 per repo canon. Typst #answer(...) is the
strip boundary (no %%% markers); strip validated by simulation, not compiled.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
