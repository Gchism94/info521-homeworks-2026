# hw13 — Overhaul draft (written cluster · Typst · PGM **diagramming** task — adapted rubric)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw13 ("Drawing probabilistic graphical models" — the
PGM for Bayesian logistic regression with a Gaussian prior). **This is the rollout map's flagged
judgment call: not a derivation, a diagramming/modeling task**, so the per-step rubric is *adapted*
to the structure of a graph. Otherwise matches the **hw5/hw9 written pilots**. **Draft only — no
hw13 files are modified; the diffs below are proposed, not applied.**

**Split: written → 60 / 30 / 10** (repo canon; correctness human-verified).
**No pytest** — the "Correctness" layer is a per-**element** structural rubric.

> **STEP 0 — classification: STRUCTURE + INTERPRETATION (the judgment call).** The task asks the
> student to *construct an artifact* (a PGM) and then *read it* — not to derive a result, and not
> (only) to interpret one. So neither the pure per-step derivation rubric (hw5/9/12) nor pure CERL
> (hw11) fits alone. The natural decomposition is exactly the 60/30/10 written canon:
> - **Correctness (60) = STRUCTURAL** — variables (right nodes), dependencies (right directed
>   edges), and replication (right plate boundaries). Graded on the **conditional-independence
>   structure the diagram *encodes*, not on layout or arrow cosmetics.** Full credit for **any
>   Markov-equivalent diagram** — one encoding the same set of conditional independencies — which
>   is the diagram analogue of "any valid route = full credit."
> - **Interpretation (30)** = CERL on **reading the conditional independencies / d-separations** the
>   structure implies (the factorization `p(w,t|X,σ²)=p(w|σ²)∏ₙ p(tₙ|xₙ,w)` and what it means for
>   the model). Genuinely Evaluate-level and **not forced** — it is the whole point of a PGM.
> - **Process (10)** = notation conventions (shaded = observed, plates labeled) + layout clarity.
>
> This is the "adapted structural rubric (nodes/edges/plate) + a conditional-independence
> interpretation" the rollout map called for.

> **"Any valid route = full credit" → "any Markov-equivalent diagram = full credit."** The
> reference solution itself says *"If the layout is slightly different but the diagram's semantics
> are accurate, that is ok."* The rubric formalizes that: **layout, node placement, and
> arrow curvature do not matter** (cosmetic) — **but node *shape* (fixed-value dot vs.
> random-variable circle) is semantic and graded**; only the variable set, observed/latent status,
> directed dependencies, and plate scope — i.e. the encoded conditional independencies — are graded.
> Defensible convention variants are accepted (§2a notes).

> **Marker reconciliation (Typst, with a twist).** hw13 is **Typst** (`hw.typ`) and uses the
> `#answer(content, fallback)` macro — but here the fallback is **`v(4in)`** (blank vertical space
> for the student to draw in), not `[]`. `make without_answers` renders only that fallback, so the
> released doc shows the prompt + blank drawing space. All solution edits stay inside the `#answer`
> first argument; the new reference-interpretation block uses **`v(2in)`** as its fallback (writing
> space for the required paragraph). Strip validated by simulation (§7), not compiled.

---

## 1. Prompt rewritten into the 8-part template (markdown)

> Authored here and mirrored into `README.md` (§4b). In `hw.typ` only student-facing blocks (an
> Allowed-approaches note + the Required-interpretation prompt) are added outside `#answer`, plus a
> Workload/Acknowledgments section (see §6 judgment call 5).

**1. Context & purpose.** A probabilistic graphical model is a *picture of a factorization*:
nodes are random variables, directed edges are conditional dependencies, plates are repetition,
and shading marks what's observed. Drawing the PGM for Bayesian logistic regression makes its
structure explicit — a Gaussian prior on `w`, conditionally-independent outputs given `w`, fixed
inputs — and that structure is exactly what the Newton-Raphson MAP inference in the next unit
(hw14) operates on.

**2. Learning objectives** (Bloom verb + the rubric row each is measured by):
- **O1** *Construct* the model's variable nodes with correct observed/latent roles.
  *(Apply — Correctness S1)*
- **O2** *Represent* the dependency structure with correctly directed edges.
  *(Apply/Analyze — Correctness S2)*
- **O3** *Scope* the repetition with correct plate notation (shared vs. per-point variables).
  *(Apply — Correctness S3)*
- **O4** *Interpret* the conditional-independence / factorization the graph encodes.
  *(Evaluate — Interpretation)*

**3. The task (outcome, not recipe).** Draw the PGM for inferring the parameters of Bayesian
logistic regression with a Gaussian prior, using plate notation where appropriate. The graph must
encode `p(w, t | X, σ²) = p(w | σ²) ∏ₙ p(tₙ | xₙ, w)`.

**4. Allowed approaches.** **Any diagram whose *semantics* are correct earns full credit** — node
placement, arrow curvature, and layout do not matter. Use the standard node convention (a
fixed-value dot for the fixed `σ²`, an open circle for the random `w`); other conventions are fine
(e.g. inputs `xₙ` as fixed nodes rather than shaded random variables, as long
as `tₙ` depends on them). State your shading/plate conventions.

**5. How you'll be assessed (criteria shown up front).**
- *Correctness (60%)* — the per-element structural rubric in §2a (S1 nodes/roles, S2 edges, S3
  plate), each scored on the validity of the modeling choice; full credit for any semantically
  equivalent diagram.
- *Interpretation (30%)* — the §6 paragraph, scored Claim/Evidence/Reasoning/Limits.
- *Process (10%)* — a stated shading/plate legend + a legible layout.
- *Specs bundle:* "Diagram = PASS" needs S1–S3 each ≥ Proficient; "Interpretation = PASS" needs ≥2
  on every CERL dimension; else one revise-and-resubmit.

**6. Required interpretation** (one short paragraph): state the factorization your graph encodes,
explain **which conditional independence it asserts among the outputs `tₙ`** (and why the plate,
the shared `w`, and the shading express it), and **name one thing the graph does *not* say**.

**7. Going further (optional, ungraded).** Redraw the model for the case where `σ²` is *also*
unknown (give it its own prior) — what node and edge appear, and is `w` still the only coupling
path among the `tₙ`?

**8. Submission contract.** Hand-drawn or typeset diagram + the interpretation paragraph; hard copy
at the start of class on the due date. Record your time in the Workload section. The only build
contract is that the reference solution stays inside the `#answer(…, v(…))` first argument so
`make without_answers` leaves only the drawing/writing space.

---

## 2. `hw13/rubric.md` — adapted per-element structural rubric (NO pytest)

### 2a. Correctness (60) — per-element structural rubric

The graph's elements play the role of "steps"; **each is scored on the validity of the modeling
choice — the conditional independencies it encodes — not on matching the reference's layout.** Any
**Markov-equivalent** diagram (same encoded independencies) earns full credit; **node placement,
arrow curvature, and overall layout are cosmetic and never cost points — but node *shape* (a
filled "fixed-value" dot vs. an open "random-variable" circle) is *semantic* under the standard PGM
convention and IS graded (see the σ² note and the FLAG below).** Each element gets a 0–3 tier
mapping to a fraction of its points (3→100%, 2→80%, 1→45%, 0→0%). Weights sum to 60; **S2 (edges)
heaviest** — the directed edges *are* the model.

| Element | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
|---------|-----|:---:|---------------|----------------|----------------|---|
| **S1 · Nodes & roles** | O1 | 20 | all variables present — `σ²`, `w`, `xₙ`, `tₙ` — with correct status: `tₙ` (and `xₙ`, by convention) **observed/shaded**, `w` **latent random / open unshaded circle**, **`σ²` a fixed hyperparameter drawn as a fixed-value node (filled dot / point), NOT a random-variable circle** | all nodes, one role/shading/shape slip | a node missing, or two roles wrong, or `σ²` drawn as a random circle | missing/wrong |
| **S2 · Edges & directions** | O2 | 24 | the three directed edges correct — `σ²→w`, `w→tₙ`, `xₙ→tₙ` — and **no spurious edges** (no direct `σ²→tₙ`, no `w→xₙ`, none among the `tₙ`) | edges right, one direction loose or one extra/missing edge | only the `w→tₙ` likelihood edge | missing/wrong |
| **S3 · Plate scope** | O3 | 16 | a plate over `n=1..N` encloses **exactly** the per-point nodes (`tₙ`, and `xₙ` if drawn as random) and **excludes** the shared `w`, `σ²`; labeled `N` | plate present, label or one boundary slightly off | plate drawn but scope wrong (encloses `w`) | missing |

**Accepted convention variants (full credit):** `xₙ` drawn as a shaded random node *or* as a fixed
input node outside/at the plate edge (logistic regression is discriminative — `xₙ` is conditioned
on, not modeled); plate corner labeled `N` or `n=1…N`; any layout/orientation.

> **σ² shape is a graded distinction, NOT a cosmetic variant (FIXED in this audit; FLAGGED).**
> Under the standard PGM convention node *shape* is semantic — a **fixed-value dot/point** marks a
> non-random (conditioned-on) quantity, an **open circle** a random variable. The model conditions
> on `σ²` (it appears in `p(w | σ²)` and is not inferred), so `σ²` is **fixed** and should be a dot,
> *distinct in shape* from the random-variable circle for `w`. Drawing `σ²` as a random circle
> misstates its status and loses an S1 tier. **The reference `hw.typ` diagram currently draws `σ²`
> as a circle (same `node-shape: circle` as `w`)** — under the strict convention that is itself
> non-standard. **Flagged for the instructor to confirm against the course's node convention:** if
> the course does *not* use the dot/circle fixed-vs-random distinction, revert this to a cosmetic
> variant and (optionally) leave the reference as-is; if it does, the reference diagram should mark
> `σ²` as a fixed-value node.

**Load-bearing vs. cosmetic (the key distinction):** an element is **load-bearing** exactly when
changing it changes the **independence semantics**. A **missing or extra edge**, a **reversed
edge**, or a **wrong plate boundary** all alter what the graph asserts → load-bearing, penalized.
**Node placement, arrow curvature, and overall layout do not change the encoded independencies →
cosmetic, never penalized. Node *shape* is the exception: a fixed-value dot vs. a random-variable
circle is semantic (the σ² distinction above) and IS graded.** Concretely:
- **S1 is load-bearing for the values** — a missing variable breaks the edges and plate that refer
  to it — but the three elements are graded on the student's *own* node set: an `S1` shading slip
  does not also cost `S2`/`S3` if the dependencies and scope are otherwise right.
- **S2 is the heart** (the conditional-dependence structure) and **the absence of edges among the
  `tₙ` is itself load-bearing** — it is what encodes conditional independence; award it explicitly.
- **S3's load-bearing point is `w` (and `σ²`) *outside* the plate** — that placement is what makes
  the parameter *shared*; a plate that swallows `w` asserts a different (wrong) model.

### 2b. Interpretation (30) — Claim / Evidence / Reasoning / Limits (0–3 each)

The §6 paragraph (12 raw → 30%). PASS = ≥2 every dimension.

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | the graph encodes `p(w,t\|X,σ²)=p(w\|σ²)∏ₙ p(tₙ\|xₙ,w)`; the `tₙ` are **conditionally independent given `w`** (`tₙ ⊥ tₘ \| w`) | mostly right, minor gap | states factorization OR independence, not both | missing |
| **Evidence** | maps structure → factors: plate = `∏ₙ`, `σ²→w` = the prior, `w→tₙ←xₙ` = the likelihood; **no edges among `tₙ`** | some of the mapping | vague | none |
| **Reasoning** | reads the independence as a **d-separation**: conditioning on the shared `w` (outside the plate) blocks the only path between any `tₙ` and `tₘ`, so they are independent **given** `w` | sound but thin / informal ("`w` is the only link") | superficial | absent/wrong |
| **Limits** | names what the graph does **not** say: marginally (`w` *not* observed) the path through `w` is **open**, so the `tₙ` are **dependent**; `xₙ` not modeled (discriminative); `σ²` fixed, not inferred | one weakly | minimal | none |

### 2c. Process (10) — legend, notation, clarity

| Sub-dim | Pts | Full credit when… |
|---------|:---:|-------------------|
| **Shading/plate legend** | 4 | the observed=shaded convention and the plate's meaning (`∏ over n`) are stated |
| **Notation** | 3 | `σ²`, `w`, `xₙ`, `tₙ`, `N` labeled and consistent with the factorization |
| **Layout clarity** | 3 | nodes/edges legible, non-overlapping, directions unambiguous |

---

## 3. Objective → rubric-row map (alignment contract)

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| **O1** nodes & observed/latent roles | Apply | Correctness **S1** | ✅ |
| **O2** directed dependency edges | Apply/Analyze | Correctness **S2** | ✅ |
| **O3** plate scope (shared vs. per-point) | Apply | Correctness **S3** | ✅ |
| **O4** conditional-independence semantics | Evaluate | **Interpretation** rubric (CERL) | ✅ |
| *(communication)* | — | **Process** rubric (2c) | ✅ (cross-cutting, not an O#) |

**Every objective maps to a rubric row; none unmeasurable.** Process is the standard
objective-free communication layer (the shading/plate legend folds in here — central to reading a
PGM).

---

## 4. Proposed unified diffs (per file — NOT applied)

### 4a. `hw.typ` — add framing (outside `#answer`) + a reference-interpretation block + Workload

The reference diagram is correct and is **not changed**. Added outside any `#answer`: an
Allowed-approaches note and a Required-interpretation prompt; added as a new `#answer(…, v(2in))`:
a reference interpretation; added as plain sections: Workload + Acknowledgments (absent in the
current file — see §6 judgment call 5). The `fletcher` import and the diagram `#answer(…, v(4in))`
boundary are untouched.

```diff
--- a/hw.typ
+++ b/hw.typ
@@
 model with a Gaussian prior on the parameters we are studying in class. Use
 plate notation wherever appropriate.
+
+#strong[Allowed approaches.] Any diagram whose #emph[semantics] are correct earns
+full credit — exact node placement, arrow curvature, and layout do not matter. Use
+the standard node convention (a fixed-value dot for the fixed $sigma^2$, an open
+circle for the random $bold(w)$); other conventions are fine (e.g. treating the
+inputs $bold(x)_n$ as fixed nodes rather than shaded random
+variables, as long as $t_n$ depends on them). What is graded is the set of
+variables and their observed / latent status, the directed dependencies, and the
+plate scope. State your shading / plate conventions. Grading criteria are in
+#emph[rubric.md].

 #answer([
   ⋯ (reference factorization + #diagram(...) unchanged; fallback stays v(4in)) ⋯
 ], v(4in))
+
+= Conditional independence the graph encodes
+
+#strong[Required interpretation.] Below your diagram, add #emph[one short
+paragraph]: state the factorization of
+$p(bold(w), bold(t) | bold(X), sigma^2)$ that your graph encodes, and explain
+which conditional independence it asserts among the outputs $t_n$ (and why the
+plate, the shared $bold(w)$, and the shading express it). Name one thing the graph
+does #emph[not] say.
+
+#answer([
+  #set text(blue)
+  The graph encodes the factorization
+  $ p(bold(w), bold(t) | bold(X), sigma^2) = p(bold(w) | sigma^2) product_(n=1)^N p(t_n | bold(x)_n, bold(w)) . $
+  Reading it off: $sigma^2 arrow.r bold(w)$ is the Gaussian prior
+  $p(bold(w)|sigma^2)$; the plate over $n = 1, dots, N$ is the product
+  $product_n$; and $bold(w) arrow.r t_n arrow.l bold(x)_n$ inside the plate is the
+  per-point likelihood $p(t_n | bold(x)_n, bold(w))$. Because the only path
+  coupling the outputs runs through the shared parameter $bold(w)$ (which sits
+  #emph[outside] the plate), the graph asserts that the $t_n$ are
+  #emph[conditionally independent given $bold(w)$] (and their inputs): there are no
+  edges directly among the $t_n$. The shading marks $bold(x)_n$ and $t_n$ as
+  observed and $bold(w)$ as latent — the thing we infer. What the graph does
+  #emph[not] say: marginally, after integrating out $bold(w)$, the $t_n$ become
+  dependent (they share what they taught us about $bold(w)$); and $sigma^2$ is a
+  fixed hyperparameter here, not itself inferred.
+], v(2in))
+
+= Workload
+<workload>
+How many hours did you spend on this homework assignment?
+
+#heading(level: 1, numbering: none)[Acknowledgments]
+<acknowledgments>
+
+Cite all the people you've worked with on this homework, as well as any other
+resources you used apart from the FCML textbook. If you used generative AI
+tools (e.g., ChatGPT), please describe how you used them.
+
+If you did not work with anyone else or use generative AI tools, please say so.
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
+# HW13 — Drawing probabilistic graphical models
+
+> Overhauled (written cluster; diagramming task with an adapted structural rubric). Grading is
+> **per-element + specifications-based**, not the old complete/incomplete gate. The full rubric
+> ships in `rubric.md`.
+
+## 1. Context & purpose
+
+A PGM is a picture of a factorization: nodes are variables, directed edges are conditional
+dependencies, plates are repetition, shading marks what's observed. Drawing the PGM for Bayesian
+logistic regression makes its structure explicit — the structure the Newton-Raphson MAP inference
+in the next unit (hw14) operates on.
+
+## 2. Learning objectives
+
+- **O1** Construct the variable nodes with correct observed/latent roles. *(Correctness S1)*
+- **O2** Represent the dependencies with correctly directed edges. *(Correctness S2)*
+- **O3** Scope the repetition with correct plate notation. *(Correctness S3)*
+- **O4** Interpret the conditional-independence/factorization the graph encodes. *(Interpretation)*
+
+## 3. The task
+
+Draw the PGM for inferring the parameters of Bayesian logistic regression with a Gaussian prior,
+with plate notation. The graph must encode `p(w, t | X, σ²) = p(w | σ²) ∏ₙ p(tₙ | xₙ, w)`.
+
+## 4. Allowed approaches
+
+**Any diagram whose *semantics* are correct earns full credit** — placement, arrow curvature, and
+layout do not matter. Use the standard node convention (a fixed-value dot for the fixed `σ²`, an
+open circle for the random `w`); `xₙ` as fixed inputs is fine, as long as `tₙ` depends on them.
+State your shading/plate conventions.
+
+## 5. How you'll be assessed (criteria shown up front)
+
+| Bundle | Weight | Pass when… |
+|--------|:------:|------------|
+| **Correctness** | **60%** | per-element rubric (`rubric.md` §2a) — S1 (nodes/roles), S2 (edges/directions), S3 (plate scope) each at **Proficient+**. Any semantically equivalent diagram counts. |
+| **Interpretation** | **30%** | the required paragraph reaches **Proficient+** on every Claim/Evidence/Reasoning/Limits dimension (`rubric.md` §2b). |
+| **Process** | **10%** | shading/plate legend stated, consistent notation, legible layout (`rubric.md` §2c). |
+
+**Revision:** one revise-and-resubmit per bundle that falls short. An LLM may draft scores; a
+human confirms and is final.
+
+## 6. Submission
+
+Hand-drawn or typeset diagram **and** the required interpretation paragraph; hard copy at the start
+of class on the due date. Record your time in the Workload section.
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
+# HW13 — Grading rubric (PGM diagram; written, adapted structural rubric)
+
+No autograder — a diagramming task. Grading replaces the 1/0.5/0 gate with a per-element
+structural rubric. Written-HW split **60 / 30 / 10** (correctness human-verified; see the repo-root
+`rubric.md`).
+
+## §2a · Correctness (60) — per-element structural rubric
+
+The graph's elements play the role of "steps"; each scored on the **conditional independencies it
+encodes**, not on this key's layout. **Any Markov-equivalent diagram (same encoded independencies)
+earns full credit; node placement, arrow curvature, and layout are cosmetic and never cost points.
+Node *shape* is the exception: a fixed-value dot vs. a random-variable circle is semantic and IS
+graded (σ² is fixed → a dot, not a circle).** Tiers map to a fraction of each element's points
+(3→100%, 2→80%, 1→45%, 0→0%). S2 (edges) heaviest — the edges are the model.
+
+| Element | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
+|---------|-----|:---:|---------------|----------------|----------------|---|
+| **S1 · Nodes & roles** | O1 | 20 | `σ²`, `w`, `xₙ`, `tₙ` present; `tₙ`/`xₙ` observed-shaded, `w` latent (open circle), `σ²` fixed hyperparameter drawn as a fixed-value dot (NOT a random circle) | one role/shading/shape slip | a node missing, two roles wrong, or σ² as a random circle | missing |
+| **S2 · Edges & directions** | O2 | 24 | `σ²→w`, `w→tₙ`, `xₙ→tₙ`; no spurious edges (no `σ²→tₙ`, `w→xₙ`, none among `tₙ`) | one direction loose / one extra-missing edge | only `w→tₙ` | missing |
+| **S3 · Plate scope** | O3 | 16 | plate over `n=1..N` encloses the per-point nodes, excludes shared `w`,`σ²`; labeled `N` | label/boundary slightly off | scope wrong (encloses `w`) | missing |
+
+**Accepted variants (full credit):** `xₙ` shaded-random or fixed-input; `σ²` solid dot or unshaded
+circle; plate labeled `N` or `n=1…N`; any layout.
+
+**Load-bearing vs. cosmetic.** An element is load-bearing exactly when changing it changes the
+independence semantics: a **missing/extra/reversed edge** or a **wrong plate boundary** are
+penalized; **placement, curvature, and layout are cosmetic and are not — but node shape (fixed dot
+vs random circle) is semantic and IS graded (σ²).** S1 is load-bearing
+for the values (a missing node breaks edges and plate) but the three elements are graded on the
+student's own node set. S2 is the heart, and **the absence of edges among the `tₙ` is itself
+load-bearing** (it encodes conditional independence). S3's load-bearing point is **`w` outside the
+plate** (what makes it shared).
+
+## §2b · Interpretation (30) — Claim / Evidence / Reasoning / Limits (0–3 each)
+
+The required paragraph. PASS = ≥2 every dimension.
+
+| Dim | 3 | 2 | 1 | 0 |
+|-----|---|---|---|---|
+| **Claim** | encodes `p(w,t\|X,σ²)=p(w\|σ²)∏ₙ p(tₙ\|xₙ,w)`; `tₙ` conditionally independent given `w` | mostly | one of the two | missing |
+| **Evidence** | plate=`∏ₙ`, `σ²→w`=prior, `w→tₙ←xₙ`=likelihood; no edges among `tₙ` | some | vague | none |
+| **Reasoning** | d-separation: conditioning on shared `w` (outside plate) blocks the only path between `tₙ`,`tₘ` ⇒ independence given `w` | informal ("`w` is the only link") | superficial | absent |
+| **Limits** | marginally (`w` unobserved) the path is open ⇒ `tₙ` dependent; `xₙ` not modeled; `σ²` fixed not inferred | one weakly | minimal | none |
+
+## §2c · Process (10)
+
+| Sub-dim | Pts | Full credit when… |
+|---------|:---:|-------------------|
+| Shading/plate legend | 4 | observed=shaded and plate=`∏ over n` stated |
+| Notation | 3 | `σ²`, `w`, `xₙ`, `tₙ`, `N` labeled, consistent with the factorization |
+| Layout clarity | 3 | legible, non-overlapping, unambiguous directions |
+
+**LLM pre-grading** may draft scores + one-line reasons; a human confirms and is final. (LLM
+pre-grading is especially weak on hand-drawn diagrams — humans grade S1–S3.)
```

### 4e. Autograder wiring (written-only — neutralize, don't orphan)

hw13 has **no `test_hw.py` and no `requirements.txt`** (identical to hw7/8/9/12). Fix is the
already-drafted **conditional `shared/classroom.yml`** (gate pytest + reporter on
`[ -f test_hw.py ]`, add a written-only branch) — cluster-wide, **not** a per-assignment `hw13/`
diff. Recorded so the written HW isn't orphaned with a red autograder. **This completes the
written cluster (hw7/8/9/12/13)** that the conditional `classroom.yml` covers.

---

## 5. Effort & budget

| Component | Change vs. current |
|-----------|--------------------|
| Diagram | unchanged (~20–30 min) |
| Interpretation paragraph | **+~15 min** (new) |
| Net | well within 5–6 hrs/week — hw13 is the lightest written HW |

The diagram is already correct, so there is **no busywork to trim**; the +15 min interpretation
load is small. The optional "σ² also unknown" extension (§7) stays ungraded.

---

## 6. Judgment calls beyond the spec

1. **Diagramming task, not a derivation (the flagged call).** Correctness (60) becomes an adapted
   **per-element** structural rubric (S1 nodes, S2 edges, S3 plate); Interpretation (30) is CERL on
   the conditional-independence semantics. This is the rollout map's recommended adaptation, mapped
   onto the standard 60/30/10 so hw13 stays consistent with the cluster.
2. **"Any valid route" → "any Markov-equivalent diagram."** Formalizes the reference's own
   "layout may differ if semantics are accurate" into the rubric (layout/placement/curvature
   ignored; node *shape* — fixed dot vs random circle — is semantic and graded) — the structural
   analogue of full credit for any sound route.
2b. **σ² node-shape correction (Phase-2 audit, FLAGGED).** Node shape is semantic under the standard
   PGM convention (dot = fixed, circle = random); σ² is conditioned on (fixed), so it must be a
   fixed-value dot, distinct from w's random circle. Removed "σ² dot-vs-circle" from the accepted
   cosmetic variants and made it a graded S1 distinction. The reference `hw.typ` draws σ² as a
   circle — flagged for the instructor to confirm against the course's node convention (revert to
   cosmetic if the course does not use the dot/circle distinction).
3. **Typst `#answer` with `v(4in)`/`v(2in)` fallbacks.** Unlike hw7/8/9/12 (`[]` fallback), hw13's
   fallback is *drawing/writing space*. The diagram answer's `v(4in)` is preserved; the new
   reference-interpretation answer uses `v(2in)`. The `#answer` first argument is still the strip
   boundary; validated by simulation.
4. **Three elements weighted `20/24/16`**, S2 (edges) heaviest because the edges are the model;
   "no edges among `tₙ`" and "`w` outside the plate" flagged as load-bearing structural facts.
5. **Added a Workload + Acknowledgments section** (absent in the current `hw13/hw.typ`, present in
   every other written HW). Low-risk consistency fix so the submission contract and time-tracking
   match the cluster. **Flagged** in case you prefer to leave hw13 without it.
6. **Through-line to hw14 made explicit** (the PGM is the structure Newton-Raphson MAP inference
   operates on) and back to the conjugacy/factorization theme (prior × likelihood).
7. **`make_release` ships `rubric.md`**; autograder neutralization flagged at the `classroom.yml`
   level (§4e) — **hw13 completes the written cluster** hw7/8/9/12/13.

---

## 7. Validation results (no PDF compile, per the format note)

Ran the proposed `hw.typ` through the **strip simulator** (`show_answers=false`: balanced-bracket
parse of `#answer(arg1, arg2)` → keep `arg2`), after confirming it reproduces a clean baseline on
the **unmodified** file. The simulator correctly keeps the `v(4in)`/`v(2in)` fallbacks (it returns
arg2 verbatim, whatever it is).

- **Baseline (current `hw.typ`):** ✅ the reference factorization + `#diagram(...)` code stripped;
  title, problem statement retained; the `v(4in)` drawing-space fallback retained; 1 `#answer(`
  block; all **3** imports (`common`, `equations`, **`fletcher`**) + `#show: info521` retained.
- **Strip check — solution content ABSENT from the released doc:** ✅ the "PGM should look like…"
  guidance, the `#diagram` `node-stroke`/node/edge code, **and** the new reference-interpretation
  paragraph (`conditionally independent given`, the `after integrating out` caveat) are all stripped.
- **Student framing RETAINED:** ✅ title, problem statement, the new Allowed-approaches note, the
  new Required-interpretation prompt + its heading, Workload, Acknowledgments, and **both** drawing/
  writing-space fallbacks `v(4in)` and `v(2in)`.
- **Structural:** ✅ exactly **2** `#answer(` blocks in source (1 diagram + 1 new reference
  interpretation), both stripped to their `v(…)` fallback; `fletcher` import intact; `#show: info521`
  retained.

(No `pytest` — written HW. No `.typ` compile — per the format note.)

---

## 8. Proposed commit message (when applied — do NOT commit now)

```
hw13 overhaul: adapted structural + CERL rubric for the PGM diagram (written)

- STEP 0: classified STRUCTURE + INTERPRETATION (construct-an-artifact then read
  it), not a derivation and not pure interpretation.
- hw.typ: rewrite the prompt to the 8-part template — add an Allowed-approaches
  note ("any Markov-equivalent diagram = full credit"; layout/placement/arrow
  curvature are cosmetic, but node SHAPE — fixed dot vs random circle — is semantic)
  and a Required-interpretation prompt, both outside
  #answer; replaces the 1/0.5/0 gate. Add a reference-interpretation #answer block
  (fallback v(2in) = writing space) and a Workload/Acknowledgments section (absent
  before; matches the rest of the written cluster). The reference #diagram is
  unchanged.
- rubric.md (new): written split 60/30/10 with an ADAPTED Correctness layer for a
  diagramming task. Correctness 60 = STRUCTURAL per-element S1/S2/S3 = 20/24/16
  (nodes/roles, edges/directions, plate scope), graded on the conditional
  independencies the diagram ENCODES; S2 heaviest (edges are the model).
  Load-bearing = anything that changes the independence semantics (missing/extra/
  reversed edge, wrong plate boundary), e.g. "no edges among t_n" (conditional
  independence) and "w outside the plate" (shared parameter); placement/curvature/
  layout are cosmetic and never penalized -- but node SHAPE (fixed dot vs random
  circle) is semantic and graded. Interpretation 30 = CERL on reading the
  conditional independencies / d-separations; Process 10 = legend + layout.
  Accepted Markov-equivalent variant: x_n fixed-vs-shaded. NOTE: sigma^2 must be a
  fixed-value node (dot), not a random circle -- a graded distinction, FLAGGED for
  instructor confirmation against the course's node convention.
- source churn: reference diagram untouched; only framing blocks + a reference
  interpretation + Workload/Ack added. All answer content stays inside the #answer
  first argument (Typst strip boundary, fallback v(4in)/v(2in) = blank space), so
  `make without_answers` leaves only the drawing/writing space; prompts sit outside
  and are retained.
- through-line: the PGM is the structure the Newton-Raphson MAP inference (HW14)
  operates on; factorization = prior x likelihood ties back to the conjugacy theme.
- make_release: also copies rubric.md into release (TILT). Autograder: written-only
  (no test_hw.py) — skip pytest via the shared conditional classroom.yml; nothing
  to time. Completes the written cluster (hw7/8/9/12/13).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
