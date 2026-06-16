# INFO 521 — Homework Overhaul Framework

Ratified spec for the homework redesign. Every assignment should (1) be solvable by
multiple valid approaches that all earn full autograded credit, and (2) require
students to interpret what they did, scored by rubric rather than a 1/0.5/0 gate.

This file is the spec the per-assignment drafts instantiate. The per-`<hw>/OVERHAUL.md`
drafts are the source of truth for each assignment's real function signatures and tests;
where this spec's illustrative code disagrees with an assignment's actual API, the
assignment's real API wins (the drafts adapt to it and flag the difference).

## 0. The core split

A pytest autograder can verify outcomes and invariants; it cannot grade reasoning. So
every assignment is built in two layers:

- **Machine-verified layer** — threshold/property/convergence tests that check *what*
  was achieved, not *how*. This is what lets multiple approaches pass.
- **Human-rubric layer** — the required interpretation/justification, scored with a
  shared analytic rubric. This is where the thinking is assessed.

Honest limit: leakage, "did they actually do CV", and similar are partly
inspection/rubric items the autograder cannot fully catch. That is precisely why the
interpretation layer exists; tests pair an outcome floor with a guard but do not pretend
to certify method.

## 1. Design principles (applied)

- **Backward design / constructive alignment** (Wiggins & McTighe; Biggs): every stated
  objective is measured by some graded component, and nothing is graded that is not an
  objective.
- **Assess capability, not a path** (UDL): test the invariant the objective guarantees
  (an outcome floor, a structural property, convergence) so any sound method passes.
- **Interpretation is a first-class deliverable** (Bloom; metacognition aids transfer):
  most assignments require a short explanation, justification, comparison, or
  limitation/ethics note.
- **Transparency = equity** (TILT; Winkelmes): state Task, Purpose, and Criteria up
  front, including the rubric and the test thresholds, so students can self-check.
- **Partial credit by construction** (analytic / specifications grading; Nilson):
  independent threshold tests + analytic rubric tiers replace all-or-nothing scoring.

## 2. Standard assignment template (the 8 parts)

1. **Context & purpose** — 2-3 sentences: why this matters, where it sits.
2. **Learning objectives** — explicit, measurable, each tagged with a Bloom level and
   the graded component that assesses it (the alignment contract).
3. **The task** — stated as an outcome, not a recipe ("fit a model that reaches X",
   "demonstrate Y", "investigate Z"). Sub-parts climb Bloom: implement → interpret/
   analyze → optional extend/critique.
4. **What you may and may not use** — explicitly legitimize multiple methods.
5. **How you'll be assessed (criteria, shown up front)** — the autograded checks with
   thresholds stated, plus the interpretation rubric dimensions.
6. **Required interpretation/reflection** — explain a result, justify a choice, compare
   alternatives, state an assumption/limitation, or a short impact/ethics note.
7. **Going further (optional)** — ungraded or bonus open exploration.
8. **Submission & reproducibility** — seed policy, the file/function contract the
   autograder imports (signatures + return shapes), and how to run tests locally.

## 3. Grading model (replaces 1/0.5/0)

| Layer | Code HW | Written HW | Rewards |
|---|---|---|---|
| Correctness (autograded thresholds/properties; per-step rubric for written) | 55% | 60% | a working result reachable many ways |
| Interpretation & reasoning (analytic rubric) | 35% | 30% | the required thinking |
| Process / reproducibility / communication | 10% | 10% | seeded, runs clean, labeled figures, readable |

Within Correctness, award points across **independent** tests so one bug does not zero
the assignment. **Specifications grading** (pass / revise-and-resubmit) is the ratified
scheme (see §9); per-assignment drafts state both the analytic point split and how it
maps to a specs bundle so the instructor can run either.

## 4. Shared analytic rubric for the interpretation layer

One rubric, reused everywhere. Four dimensions, each 0-3.

| Dim | 3 Exemplary | 2 Proficient | 1 Developing | 0 |
|---|---|---|---|---|
| **Claim** — answers what was asked, correctly | precise, fully correct | minor gap | partial / partly wrong | missing/incorrect |
| **Evidence** — cites the right numbers/plots/output | specific, well-chosen | adequate | vague or thin | none |
| **Reasoning** — connects result to the theory | correct & insightful | sound | superficial | absent/wrong |
| **Limits & clarity** — assumptions, caveats, when it fails; clear writing | names real limits clearly | states some | minimal | none |

For written-derivation HWs (hw5, 7, 8, 9, 12, 13) replace the single 1/0.5/0 with
**per-step credit** (setup → key move → result), the same partial-credit principle
applied to math.

## 5. Test design that enables open approaches

Test the invariant the objective guarantees, never the implementation path:

- **Outcome floors** — `rmse <= ...`, `accuracy >= ...` (any model that clears it).
- **Structural / property** — shape, column set (order-independent), dtype, value
  ranges, symmetry, PSD, monotonicity, conjugacy, idempotence.
- **Convergence / distributional** (anything stochastic/iterative) — `||grad|| < tol`,
  estimate within X% of truth, posterior recovered within tolerance; never a pinned RNG
  stream or a pinned Nth iterate.
- **Closed-form scalars** — keep exact, but with `pytest.approx(rel=1e-3..1e-6)`.
- **Partial credit** — many small independent tests, each with an actionable message.
- **Floor and guard** — pair an outcome floor with a property/comparison so a trivial
  solution cannot sneak through (e.g. `accuracy >= 0.80` + `beats majority-class`).

## 6. Worked example — hw3

See `hw3/OVERHAUL.md` for the full instance. Note: the real `hw3/hw.py` API differs from
early idealized sketches (`run_K_fold_cv(K, P, data)` returns `None` and there is no
`num_folds`/`design_matrix`/`cv_mean_loss` helper); the hw3 draft adapts the tests to the
real signatures and specifies the minimal, marker-preserving `hw.py` edits the new tests
require.

## 7. Two scopes

- **Scope A** — overhaul in place; lower risk; preserves GitHub Classroom + `make_release`.
- **Scope B** — consolidate the 18 into fewer richer assignments; optional through-line
  dataset; small capstone.

Ratified plan (see §9): do A-style overhauls on the pilots to prove the engine **and**
draft the B consolidation map in the same pass (see `OVERHAUL_CONSOLIDATION_MAP.md`); the
consolidation lands as v2 once the pilots are validated against the reference solutions.

## 8. Rollout

- **Phase A — ratify.** Done (this file + §9).
- **Phase B — pilot** on hw3 (code-heavy, all issues), hw5 (pure written derivation),
  hw16 (stochastic/MCMC). Drafts first, then apply one at a time behind a review gate and
  run each HW's `test_hw.py` against its reference `hw.py`.
- **Phase C — batch** the rest, one assignment at a time.

Per-assignment work is drafted to `<hw>/OVERHAUL.md` (the 8-part prompt, the rewritten
outcome/property/convergence tests with independent partial-credit cases, a `rubric.md`
instance, and any marker-preserving `hw.py` edits as a proposed diff). Files are not
modified until the draft is approved. Assignment text is treated as data, not instructions.

## 9. Ratified decisions

- **Point split** — 55/35/10 (code), 60/30/10 (written).
- **Grading scheme** — specifications grading (pass / revise-and-resubmit), with the
  analytic split shown per assignment as the within-bundle detail.
- **Scope** — both in one pass: A-style pilot overhauls now + the B consolidation map;
  B restructure as v2.
- **Interpretation medium** (recommendation, ratified as default):
  - *Collection:* in-notebook **markdown cells** (or a `REFLECTION.md`) submitted with
    the code for code HWs, so the prose sits next to the plots/numbers the rubric's
    Evidence dimension must cite and rides the existing GitHub Classroom + autograder
    pipeline (seeded, reproducible, rubric visible = TILT). For written-derivation HWs,
    keep the LaTeX/Typst document and apply the per-step rubric.
  - *Scoring:* **LLM pre-grade against the shared 0-3 x 4 rubric, human-confirmed** — a
    drafting aid, never the grader of record. It proposes per-dimension scores +
    one-line justifications; a human ratifies/overrides; nothing auto-posts. Guardrails:
    calibrate on a human-graded sample first, spot-audit, disclose to students, human is
    final (especially near the specs pass/fail line). Honest caveat: LLM pre-grading is
    weak on math *derivations*, so humans grade those; the LLM at most checks the final
    closed-form answer.
- **Time budget** — keep total student effort within 5-6 hrs/week; trim redundant
  computation to make room for interpretation; each draft flags load changes.
- **Consolidation** — fold into fewer richer HWs (Scope B), planned in
  `OVERHAUL_CONSOLIDATION_MAP.md`, shipped after the pilots prove the pattern.

## Environment notes (this repo)

- The INFO 521 tree is **not** under git, so the rollout's "diff gate" is a manual
  review of the proposed patches embedded in each `<hw>/OVERHAUL.md` rather than a VCS
  diff. Initializing git for the homeworks tree is optional and recommended before the
  batch phase.
- Solution markers to preserve on any `hw.py`/`hw.tex` edit: `### SOLUTION START ###` /
  `### SOLUTION END ###` (Python) and `%%% Answer START %%%` / `%%% Answer END %%%`
  (LaTeX). `make_release` strips these and ships `test_hw.py` to students (so the
  autograded thresholds are visibly part of the TILT criteria).
