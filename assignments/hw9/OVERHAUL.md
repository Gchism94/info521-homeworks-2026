# hw9 — Overhaul draft (written-derivation pattern · cleanest written representative)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw9 (Fisher information for the Bernoulli).
Matches the **hw5 written-derivation pilot**. **Draft only — no hw9 files are modified; the
diffs below are proposed, not applied.**

**Split: written/derivation → 60 / 30 / 10** (repo canon; correctness human-verified).
**No pytest** — the "Correctness" layer is a per-step derivation rubric.

> **Marker reconciliation (judgment call, flagged).** hw9 is **Typst** (`hw.typ`), not LaTeX.
> Its strip mechanism is the `#answer([solution], [blank])` macro toggled by
> `make without_answers` (`typst compile … --input show_answers=false`), which renders only
> the *second* argument in the release. So the **`#answer(...)` first argument is the answer
> marker** — the faithful analogue of `%%% Answer START/END %%%`. All solution edits stay
> inside it. Per the format note, I did **not** compile the `.typ`; the strip was validated
> structurally (§8).

---

## 1. Prompt rewritten into the 8-part template (markdown)

> Authored here and mirrored into `README.md` (§4b). In `hw.typ` only the two student-facing
> lines (Allowed approaches + Required-interpretation prompt) are added outside `#answer`; the
> rest of the framing lives in `README.md` markdown because the document format is changing.

**1. Context & purpose.** Fisher information measures how much a single observation tells you
about a parameter — it sets the Cramér–Rao floor on any unbiased estimator's variance and the
asymptotic variance of the MLE. Deriving it once for the Bernoulli connects directly to the
MLE you found in Homework 5.

**2. Learning objectives** (Bloom verb + the rubric row each is measured by):
- **O1** *State* the Fisher information as the expected curvature (or score variance) of the
  log-likelihood. *(Understand/Apply — Correctness step A)*
- **O2** *Differentiate* the Bernoulli log-pmf to the score and the curvature.
  *(Apply — Correctness steps B, C)*
- **O3** *Evaluate* the expectation to the closed form `I(r) = 1/(r(1−r))`.
  *(Analyze — Correctness step D)*
- **O4** *Interpret* the result — how informativeness varies with `r`, and the assumptions it
  rests on. *(Evaluate — Interpretation rubric)*

**3. The task (outcome, not recipe).** Derive the Fisher information `I(r)` for the parameter
`r` of a `Bernoulli(r)` distribution. The required result is `I(r) = 1/(r(1−r))`.

**4. Allowed approaches.** **Any mathematically valid route to `I(r) = 1/(r(1−r))` earns full
credit — no canonical path is privileged.** You may use the curvature form
`I = E[−∂²log p/∂r²]` *or* the score-variance form `I = E[(∂log p/∂r)²]`; both are correct
under the standard regularity conditions. Show the steps that justify each move; a bare final
answer earns only the result step.

**5. How you'll be assessed (criteria shown up front).**
- *Correctness (60%)* — the per-step derivation rubric in §2 (setup → score → curvature →
  expectation), each step scored on the **validity of the move**, full credit for any sound
  alternative route.
- *Interpretation (30%)* — the §6 paragraph, scored Claim/Evidence/Reasoning/Limits.
- *Process (10%)* — notation, stated assumptions, justification clarity.
- *Specs bundle:* "Derivation = PASS" needs steps A–D each ≥ Proficient; "Interpretation =
  PASS" needs ≥2 on every CERL dimension; else one revise-and-resubmit.

**6. Required interpretation** (one short paragraph): what does `I(r)` say about how
informative a single observation is about `r` as `r` varies; **where is it largest / smallest,
and why**; and what assumptions / regularity conditions it relies on (or a case where it
breaks — e.g. `r` at the boundary 0 or 1).

**7. Going further (optional, ungraded).** Give the Fisher information for `N` i.i.d.
observations and connect `1/(N·I(r))` to the variance of the Homework-5 MLE `r̂ = (Σxᵢ)/N`.

**8. Submission contract.** Written derivation, hard copy as today (the written cluster keeps
its medium; only the *grading* changes). Keep the Workload + Acknowledgments sections. The
only build contract is that the solution stays inside the `#answer([…], [])` first argument so
`make without_answers` strips it.

---

## 2. `hw9/rubric.md` — per-step derivation rubric (NO pytest)

### 2a. Correctness (60) — per-step derivation rubric

Enumerate the major logical steps; **each is scored on the validity of the move, not on
matching the reference's exact algebra.** Any sound alternative route to `I(r)=1/(r(1−r))`
earns full credit (e.g. the score-variance form instead of the curvature form). Each step gets
a 0–3 tier mapping to a fraction of its points (3→100%, 2→80%, 1→45%, 0→0%). Weights sum to 60.

| Step | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
|------|-----|:---:|---------------|----------------|----------------|---|
| **A · Definition / setup** | O1 | 12 | states a correct Fisher-information definition — `I = E[−∂²log p/∂r²]` **or** `E[(∂log p/∂r)²]` — and that it is scalar for one parameter | states a definition with a minor gap | wrong/garbled definition but some intent | missing |
| **B · Log-pmf & score** | O2 | 14 | `log p = y log r + (1−y)log(1−r)`, score `∂/∂r = y/r − (1−y)/(1−r)` | right with a small slip | sets up log-pmf only / score error | missing/incorrect |
| **C · Curvature (2nd derivative)** | O2/O3 | 14 | `∂²/∂r² = −y/r² − (1−y)/(1−r)²` (correctly differentiates the student's own score) | minor slip | attempts but wrong sign/term | missing |
| **D · Expectation & result** | O3 | 20 | takes `E[·]`, uses `E[Y]=r`, simplifies `1/r + 1/(1−r) = 1/(r(1−r))` | right result, minor algebra slip | applies E but cannot simplify | missing/incorrect |

**Load-bearing vs. independent:**
- **A is load-bearing** — a wrong Fisher-information definition caps the whole result — but the
  *form* is free: the score-variance route earns full A (and B–D adapt to it).
- **B → C → D is a chain for the *values*, but each *move* is gradeable in isolation.** Grade C
  on whether it correctly differentiates the student's *own* score, and D on whether it
  correctly takes the expectation of the student's *own* curvature. An error upstream caps the
  final value but **not** the method credit downstream.
- **Within D, two independent sub-moves:** (i) the expectation step using `E[Y]=r` (the key
  insight), (ii) the algebraic simplification to `1/(r(1−r))`. Award separately.

### 2b. Interpretation (30) — Claim / Evidence / Reasoning / Limits (0–3 each)

The §6 paragraph (12 raw → 30%). PASS = ≥2 every dimension.

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | correctly states `I(r)` is **smallest at `r=1/2`** and grows as `r→0` or `1` | mostly right, minor gap | partial / direction confused | missing |
| **Evidence** | cites `I(1/2)=4`, the `1/(r(1−r))` shape, or the CRLB variance `r(1−r)/N` | some numbers | vague | none |
| **Reasoning** | links Fisher info → estimator precision (CRLB / MLE variance); explains *why* near-boundary outcomes are more informative | sound | superficial | absent/wrong |
| **Limits** | names a real condition/failure: `r∈(0,1)`, support not depending on `r`, boundary breakdown, single obs vs `N` | one weakly | minimal | none |

### 2c. Process (10) — notation, assumptions, justification clarity

| Sub-dim | Pts | Full credit when… |
|---------|:---:|-------------------|
| **Notation** | 4 | `r`, `Y`, `I`, `E`, `log` base defined/consistent |
| **Stated assumptions** | 3 | `Y∈{0,1}`, `r∈(0,1)`, `E[Y]=r`, regularity made explicit |
| **Justification clarity** | 3 | each line follows from the previous; legible |

---

## 3. Objective → rubric-row map (alignment contract)

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| **O1** state Fisher information | Understand/Apply | Correctness **step A** | ✅ |
| **O2** score & curvature | Apply | Correctness **steps B, C** | ✅ |
| **O3** expectation → closed form | Analyze | Correctness **step D** | ✅ |
| **O4** interpret | Evaluate | **Interpretation** rubric (CERL) | ✅ |
| *(communication)* | — | **Process** rubric (2c) | ✅ (cross-cutting, not an O#) |

**Every objective maps to a rubric row; none unmeasurable.** Process is the standard
objective-free communication layer (flagged per the "flag any you cannot measure" instruction;
nothing here is unmeasurable).

---

## 4. Proposed unified diffs (per file — NOT applied)

### 4a. `hw.typ` — add framing (outside `#answer`) + polish the solution (inside `#answer`)

All solution edits stay inside the `#answer([…], [])` first argument (stripped by
`make without_answers`); the two prompt lines go outside it (always shown). No imports,
headings, or the `#answer` strip boundary are disturbed.

```diff
--- a/hw.typ
+++ b/hw.typ
@@
 = Fisher Information for Bernoulli distribution
 <fisher-information-for-bernoulli-distribution>
 #emph[(FCML Exercise 2.13)]

-Compute the Fisher information for the parameter of a Bernoulli
-distribution.
+Compute the Fisher information $cal(I)(r)$ for the parameter $r$ of a Bernoulli
+distribution.
+
+#strong[Allowed approaches.] Any mathematically valid route to
+$cal(I)(r) = frac(1, r (1 - r))$ earns full credit — you may use the curvature
+form $cal(I) = bb(E){- partial^2 log p slash partial r^2}$ or the score-variance
+form $cal(I) = bb(E){(partial log p slash partial r)^2}$. Show the steps that
+justify each move; a bare final answer earns only the result step. Grading
+criteria are in #emph[rubric.md].
+
+#strong[Required interpretation.] After deriving $cal(I)(r)$, add one short
+paragraph: what does $cal(I)(r)$ say about how informative a single observation
+is about $r$ as $r$ varies; where is it largest / smallest, and why; and what
+assumptions or regularity conditions it relies on (or a case where it breaks)?

 #answer([
+  #strong[Assumptions and notation.] Let $Y tilde.op$ Bernoulli$(r)$ with
+  $Y in {0, 1}$ and $r in (0, 1)$; "$log$" is the natural logarithm. We use the
+  curvature form of the Fisher information,
+  $cal(I) = bb(E)_(p (y | r)){- partial^2 log p (y | r) slash partial r^2}$,
+  which under the usual regularity conditions (the support ${0, 1}$ does not
+  depend on $r$, and differentiation and expectation may be interchanged) equals
+  the score-variance form $bb(E){(partial log p slash partial r)^2}$.
+
   #strong[Solution] The Fisher Information Matrix (FIM) is an $M times M$
   matrix, where $M$ is the number of parameters of the distribution. Since
   the Bernoulli distribution only has one parameter, the FIM will be a
-  single number. Let $Y tilde.op$Bernoulli$(r)$; then the FIM, $cal(I)$,
-  is given by
+  single number. With $p(y | r) = r^y (1 - r)^(1 - y)$, the FIM, $cal(I)$,
+  is given by
   $ 
   cal(I) &=  bb(E)_(p (y | r)) {- frac(partial^2 log p (y | r), partial r^2)}\
   &=  bb(E)_(p (y | r)) {- frac(partial^2, partial r^2) (y log r + (1 - y) log (1 - r))}\
   &=  bb(E)_(p (y | r)) {- frac(partial, partial r) (y / r - frac(1 - y, 1 - r))}\
   &=  bb(E)_(p (y | r)) {y / r^2 + frac(1 - y, (1 - r)^2)}\
+  &=  frac(bb(E){y}, r^2) + frac(bb(E){1 - y}, (1 - r)^2)\
+  &=  frac(r, r^2) + frac(1 - r, (1 - r)^2)\
   &=  1 / r + frac(1, 1 - r)\
   &=  frac(1, r (1 - r)) , 
   $ 
-  where we have used the fact that $bb(E)_(p (y | r)) {y} = r$.
+  where we have used the facts that $bb(E)_(p (y | r)) {y} = r$ and hence
+  $bb(E){1 - y} = 1 - r$.
+
+  #strong[Interpretation.] The Fisher information $cal(I)(r) = 1 slash (r (1 - r))$
+  measures how much a single Bernoulli observation tells us about $r$. It is
+  smallest at $r = 1 slash 2$ (where $cal(I) = 4$) and grows without bound as
+  $r arrow.r 0$ or $r arrow.r 1$: near the boundary the outcome is almost
+  deterministic, so even a small change in $r$ is easy to detect, whereas a fair
+  coin is the hardest case. Equivalently, by the Cramér–Rao bound the asymptotic
+  variance of the MLE $hat(r)$ from $N$ observations is
+  $1 slash (N cal(I)(r)) = r (1 - r) slash N$ — exactly the variance of the
+  sample-mean estimator from Homework 5. This relies on $r in (0, 1)$ and the
+  regularity conditions above; at $r = 0$ or $r = 1$ the information is undefined
+  and the bound breaks down.
 ],
 []
 )
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
+# HW9 — Fisher Information for the Bernoulli
+
+> Overhauled (written-derivation pattern). Grading is **per-step + specifications-based**, not
+> the old complete/incomplete gate. The full rubric ships in `rubric.md`.
+
+## 1. Context & purpose
+
+Fisher information measures how much one observation tells you about a parameter — it sets the
+Cramér–Rao floor on an unbiased estimator's variance and the asymptotic variance of the MLE.
+Deriving it for the Bernoulli connects directly to the MLE from Homework 5.
+
+## 2. Learning objectives
+
+- **O1** State the Fisher information as expected curvature / score variance. *(Correctness A)*
+- **O2** Differentiate the Bernoulli log-pmf to the score and curvature. *(Correctness B, C)*
+- **O3** Evaluate the expectation to `I(r) = 1/(r(1−r))`. *(Correctness D)*
+- **O4** Interpret how informativeness varies with `r` and its assumptions. *(Interpretation)*
+
+## 3. The task
+
+Derive the Fisher information `I(r)` for the parameter `r` of `Bernoulli(r)`. Required result:
+`I(r) = 1/(r(1−r))`.
+
+## 4. Allowed approaches
+
+**Any mathematically valid route to `I(r) = 1/(r(1−r))` earns full credit** — curvature form
+`E[−∂²log p/∂r²]` or score-variance form `E[(∂log p/∂r)²]`. Show the steps; a bare final answer
+earns only the result step.
+
+## 5. How you'll be assessed (criteria shown up front)
+
+| Bundle | Weight | Pass when… |
+|--------|:------:|------------|
+| **Correctness** | **60%** | per-step derivation rubric (`rubric.md` §2a) — steps A (definition), B (score), C (curvature), D (expectation→result) each at **Proficient+**. Any sound route counts. |
+| **Interpretation** | **30%** | the required paragraph reaches **Proficient+** on every Claim/Evidence/Reasoning/Limits dimension (`rubric.md` §2b). |
+| **Process** | **10%** | clear notation, stated assumptions, legible justification (`rubric.md` §2c). |
+
+**Revision:** one revise-and-resubmit per bundle that falls short. An LLM may draft scores; a
+human confirms and is final.
+
+## 6. Submission
+
+Write up the derivation **and** the required interpretation paragraph; submit a hard copy at
+the start of class on the due date. Record your time in the Workload section.
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
+# HW9 — Grading rubric (Fisher information; written derivation)
+
+No autograder — this is a written derivation. Grading replaces the 1/0.5/0 gate with per-step
+partial credit. Written/derivation-HW split **60 / 30 / 10** (correctness human-verified; see
+the repo-root `rubric.md`).
+
+## §2a · Correctness (60) — per-step derivation rubric
+
+Each step is scored on the **validity of the move**, not on matching this key's exact algebra.
+**Any sound route to `I(r) = 1/(r(1−r))` earns full credit** (e.g. the score-variance form).
+Tiers map to a fraction of each step's points (3→100%, 2→80%, 1→45%, 0→0%).
+
+| Step | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
+|------|-----|:---:|---------------|----------------|----------------|---|
+| **A · Definition** | O1 | 12 | correct FI definition (`E[−∂²log p/∂r²]` or `E[(∂log p/∂r)²]`), noted scalar | minor gap | garbled but intent | missing |
+| **B · Log-pmf & score** | O2 | 14 | `log p = y log r + (1−y)log(1−r)`, score `y/r − (1−y)/(1−r)` | small slip | log-pmf only / score error | missing |
+| **C · Curvature** | O2/O3 | 14 | `−y/r² − (1−y)/(1−r)²` (differentiates own score) | minor slip | wrong sign/term | missing |
+| **D · Expectation & result** | O3 | 20 | uses `E[Y]=r`, simplifies to `1/(r(1−r))` | minor algebra slip | applies E, can't simplify | missing |
+
+**Load-bearing vs. independent.** A is load-bearing (wrong FI definition caps the result) but
+route-free. B→C→D is a value-chain, yet each move is gradeable on the student's own previous
+line — an upstream error caps the final value, not the downstream method credit. Within D,
+score the expectation move (`E[Y]=r`) and the algebraic simplification separately.
+
+## §2b · Interpretation (30) — Claim / Evidence / Reasoning / Limits (0–3 each)
+
+The required paragraph. PASS = ≥2 every dimension.
+
+| Dim | 3 | 2 | 1 | 0 |
+|-----|---|---|---|---|
+| **Claim** | `I(r)` smallest at `r=1/2`, grows as `r→0` or `1` | mostly | direction confused | missing |
+| **Evidence** | cites `I(1/2)=4` / the `1/(r(1−r))` shape / CRLB variance `r(1−r)/N` | some | vague | none |
+| **Reasoning** | links FI → estimator precision; why near-boundary is more informative | sound | superficial | absent |
+| **Limits** | `r∈(0,1)`, support independent of `r`, boundary breakdown, single obs vs `N` | one weakly | minimal | none |
+
+## §2c · Process (10)
+
+| Sub-dim | Pts | Full credit when… |
+|---------|:---:|-------------------|
+| Notation | 4 | `r`, `Y`, `I`, `E`, `log` defined/consistent |
+| Stated assumptions | 3 | `Y∈{0,1}`, `r∈(0,1)`, `E[Y]=r`, regularity explicit |
+| Justification clarity | 3 | each line follows; legible |
+
+**LLM pre-grading** may draft scores + one-line reasons; a human confirms and is final.
+(LLM pre-grading is weak on derivations — humans grade A–D.)
```

### 4e. Autograder wiring (written-only — neutralize, don't orphan)

hw9 has **no `test_hw.py` and no `requirements.txt`**, but the shared `shared/classroom.yml`
runs `autograding-python-grader` (pytest) and `pip install -r requirements.txt`. Shipped as-is
to a written-only repo it would **fail** (no requirements file, no tests). **Recommendation
(flagged, not applied here):** the template generator (`scripts/make_template_repo.sh`) should
**omit the autograder workflow for written-only HWs** (or ship a no-op "submission received"
check), so grading is hard-copy + `rubric.md`. This is an infra-level change to the generator,
out of scope for the per-assignment `hw9/` diff, but recorded so the written HW isn't orphaned
with a perpetually-red autograder.

---

## 5. Effort & budget

| Component | Change vs. current |
|-----------|--------------------|
| Derivation | unchanged (~30–45 min; single derivation) |
| Interpretation paragraph | **+~15 min** (new) |
| Net | well within 5–6 hrs/week — hw9 is the smallest written HW |

The derivation is already minimal (four short steps), so there is **no busywork to trim**; the
+15 min interpretation load is small and absorbed. The optional `N`-observation extension (§7)
stays ungraded.

---

## 6. Judgment calls beyond the spec

1. **Typst, not LaTeX markers (the big one).** The task names `%%% Answer START/END %%%`; hw9
   uses Typst's `#answer([sol], [blank])` + `make without_answers`. I kept all solution edits
   inside the `#answer` first argument (the faithful strip boundary) and validated the strip
   structurally rather than by compiling (per the format note).
2. **Target result shown in the prompt.** The Allowed-approaches line states the target
   `I(r)=1/(r(1−r))` (outcome-based + TILT, consistent with hw5 revealing `r̂`). The *solution's*
   derivation and result line are still stripped from the release; only the target is surfaced
   so students know what to derive. Flagged because it means the released doc contains the
   formula by design.
3. **Four fine-grained steps for one exercise.** "Major logical steps" = definition/score/
   curvature/expectation, mapping cleanly to O1/O2/O3. Weights `12/14/14/20` (D heaviest);
   any split summing to 60 with D heaviest is fine.
4. **8-part prompt authored in `README.md` markdown**, with only two student-facing lines added
   to `hw.typ` — because the document format is changing and rendering is deferred.
5. **hw5 through-line preserved.** The reference interpretation ties `1/(N·I(r))` to the hw5
   MLE variance `r(1−r)/N` (Unit-2 coherence).
6. **`make_release` ships `rubric.md`**; autograder neutralization for written-only HWs flagged
   at the generator level (§4e).

---

## 7. Validation results (no PDF compile, per the format note)

Ran the proposed `hw.typ` through a **strip simulator** that emulates `show_answers=false`
(balanced-bracket parse of `#answer(arg1, arg2)` → keep `arg2`), plus structural checks:

- **Strip check — solution content ABSENT from the released doc:** ✅ solution result line
  `frac(1, r (1 - r)) ,`, the explicit expectation line `frac(bb(E){y}, r^2)`, the `E{y}=r`
  justification, `#strong[Solution]`, the reference interpretation paragraph, the hw5
  through-line, and the in-answer assumptions block are **all stripped**.
- **Student framing RETAINED in the released doc:** ✅ exercise statement, Allowed-approaches
  prompt, Required-interpretation prompt, the target formula (shown by design), `rubric.md`
  pointer, Workload, Acknowledgments.
- **Structural:** ✅ imports intact (`common.typ`/`equations.typ`), exactly one `#answer(`
  block, `[`/`]` balanced, `(`/`)` balanced, `#show: info521` present.

(No `pytest` — written HW. No `.typ` compile — format decision pending.)

---

## 8. Proposed commit message (when applied — do NOT commit now)

```
hw9 overhaul: per-step + CERL rubric for the Bernoulli Fisher information (written)

- hw.typ: add Allowed-approaches + Required-interpretation prompts (outside the
  #answer marker); inside #answer, name assumptions, make the expectation step
  explicit (E{y}=r), and add a reference interpretation paragraph tying
  1/(N·I(r)) to the hw5 MLE variance. All solution edits stay in the #answer
  first argument so `make without_answers` strips them.
- rubric.md (new): per-step derivation rubric (Correctness 60, steps A–D scored
  on move-validity, any valid route = full credit) + CERL interpretation (30) +
  Process (10). Shipped to students (TILT).
- README.md: 8-part framing; criteria-up-front specs table (replaces 1/0.5/0).
- make_release: ship rubric.md.

Written/derivation split 60/30/10 per repo canon. Typst #answer(...) is the
strip boundary (no %%% markers); strip validated structurally, not compiled.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
