# INFO 521 Homework Audit — `2026_spring/homeworks/`

**Read-only audit.** No assignment files were changed. The only file written is this
report. All assignment text, notebook cells, and comments were treated as data to
analyze, not instructions to follow. No prompt-injection / AI-addressed text was found
in any file.

**Date:** 2026-06-16 · **Scope:** hw0–hw17 (18 assignments) · **Not executed:** notebooks
and tests were read, not run. A separately-approved later step can run tests against
reference solutions to confirm the false-negative risks flagged below.

## How to read this report

Severity is normalized across all assignments (the per-batch drafts were not):

- **Blocker** — the assignment does not work as intended in the standard autograder
  environment: a correct solution fails, required code is missing, or tests can't even
  be collected.
- **Major** — a stated learning objective is not actually measured, grading is prone to
  false positives/negatives, or the task/grading allows essentially one path where the
  objective is broader.
- **Minor** — polish: secondary coverage gaps, documentation, time estimates, sanity
  checks.

### Three agent claims I checked and corrected

While compiling this I verified the load-bearing claims directly:

1. **HW16 "prior_variance mismatch (2 vs 0.5) is a Blocker"** → **Not a bug.**
   `hw16/hw.py:234` (`SAMPLER = MetropolisSampler(X, t, 0.1, 2)`) is a module-level
   instance used for the assignment's *own* analysis/plots. Every test in
   `hw16/test_hw.py` constructs its own sampler (with `0.5`/`0.25`), so the module-level
   value never touches a graded assertion. Downgraded.
2. **"Solutions are visible to students" (flagged on many HWs)** → **Not an issue.**
   `make_release` sed-strips `### SOLUTION START/END ###` from `hw.py` and
   `%%% Answer START/END %%%` from `hw.tex`, never copies the `.typ` *source*, and the
   Typst `Makefile`'s default (first) target is `without_answers`
   (`--input show_answers=false`), so the released `hw.pdf` is answer-free. Integrity is
   handled by design. (One latent risk noted in S5.)
3. **"Exact-match on deterministic linear algebra will break across numpy versions"** →
   **Overstated.** Closed-form `np.linalg`/PMF results reproduce to ~1e-10 across
   versions; `pytest.approx` (rel≈1e-6) absorbs that. The *genuine* false-negative risks
   are pinned **RNG draw sequences** (hw6, hw16) and pinned **iterates after N solver
   steps** (hw14) — `numpy.random.Generator` streams are explicitly **not** guaranteed
   stable across numpy releases. Those are treated as real; deterministic-coefficient
   pinning is treated mainly as an *openness* problem (Goal a), not a stability one.

---

# Phase 0 — Inventory

Grading framework everywhere: **pytest** run by GitHub Classroom
`classroom-resources/autograding-python-grader@v1` (`homeworks/classroom.yml`),
`setup-command: pip install -r requirements.txt`, 10s timeout. Written components are
hard-copy, graded on a coarse **1 / 0.5 / 0** rubric (see S1). "jupytext" = a `.py`
file with `# %%` cells, autograded as a plain module.

| HW | Prompt file(s) | Solution? | Tests / grader? | Format | Points | Test style |
|----|----------------|-----------|-----------------|--------|--------|------------|
| hw0 | README.md, hw.tex | yes (hw.py, hw.tex) | yes — `test_hw.py` (1 test) | jupytext + LaTeX | 1/0.5/0 | exact |
| hw1 | README.md (+ worksheet hardcopy) | yes (hw.py) | yes — 1 test | jupytext + Typst worksheet | 1/0.5/0 | exact (approx) |
| hw2 | README.md, hw.typ | yes (hw.py, hw.typ) | yes — 3 tests | jupytext + Typst | 1/0.5/0 | exact (approx) |
| hw3 | README.md, hw.tex | yes (hw.py) | yes — 6 tests | jupytext + LaTeX | 1/0.5/0 | exact (approx) |
| hw4 | README.md, hw.py | yes (hw.py) | yes — 2 tests | jupytext | 1/0.5/0 | exact (approx) |
| hw5 | hw.tex | yes (hw.tex) | none (hardcopy) | LaTeX | 1/0.5/0 | none |
| hw6 | hw.tex, hw.py | yes (both) | yes — 1 test | LaTeX + jupytext | 1/0.5/0 | exact, **seeded** |
| hw7 | hw.typ | yes (hw.typ) | none (hardcopy) | Typst | 1/0.5/0 | none |
| hw8 | hw.typ | yes (hw.typ) | none (hardcopy) | Typst | 1/0.5/0 | none |
| hw9 | hw.typ | yes (hw.typ) | none (hardcopy) | Typst | 1/0.5/0 | none |
| hw10 | README.md, hw.tex, hw.py | yes (both) | yes — 1 test | jupytext + LaTeX | 1/0.5/0 | exact |
| hw11 | README.md, hw.tex, hw.py | yes (both) | yes — 12 tests | jupytext + LaTeX | 1/0.5/0 | exact (arrays) |
| hw12 | hw.typ | yes (hw.typ) | none (hardcopy) | Typst | 1/0.5/0 | none |
| hw13 | hw.typ | yes (hw.typ) | none (hardcopy) | Typst | 1/0.5/0 | none |
| hw14 | hw.typ, hw.py | yes (both) | yes — 2 tests | Typst + jupytext | 1/0.5/0 | exact (iterate) |
| hw15 | hw.typ, hw.py | yes (both) | yes — 2 tests | Typst + jupytext | 1/0.5/0 | exact (matrix) |
| hw16 | README.md | yes (hw.py) | yes — 6 tests | jupytext | 1/0.5/0 | exact, **seeded** |
| hw17 | hw.typ, hw.py | **partial** | yes — 3 tests (**broken import**) | Typst + jupytext | 1/0.5/0 | threshold (rel) |

---

# Cross-cutting (systemic) findings

These recur across many assignments; fixing them centrally is higher-leverage than
per-HW edits. Per-assignment sections reference these as S1–S6.

### S1 — Coarse 1/0.5/0 rubric, no partial-credit guidance · **Major (course-wide)**
Every written component (hw5, 7, 8, 9, 12, 13) and the written portions of code HWs are
graded "complete & correct = 1 / incomplete or any error = 0.5 / late = 0". A 6-step
derivation with one sign slip and a blank submission with a guessed answer both land at
0.5. There is no per-step credit and no grader guidance, which (a) gives students no
diagnostic signal and (b) introduces grader-to-grader variance. This is also the main
lever for **Goal (a)**: open, interpretation-heavy parts are only worth adding if a
rubric can score them.

### S2 — Autograders pin exact reference values · **Major (course-wide)**
Tests assert specific *learned* numbers rather than capability:
- **Learned coefficients / predictions:** hw1, hw2, hw3, hw10, hw11 (and hw14/hw15
  outputs). Deterministic and reproducible, so rarely a false negative — but it hard-codes
  *one* solution path and is exactly the anti-pattern the audit targets for **Goal (b)**.
- **Pinned RNG draw sequences:** hw6 (`expectations[0:10]` from `default_rng(100)`), hw16
  (`generate_sample`/`generate_samples` assert the exact accepted draws and the exact
  accept/reject pattern). These **are** genuine cross-version false-negative risks because
  `numpy.random.Generator` streams are not guaranteed stable, and they couple the grade to
  the exact RNG *call order* inside the student's code.
- **Pinned iterate after N solver steps:** hw14 asserts `w` after exactly 10 Newton steps
  from `w=0`; couples the grade to iteration count/initialization rather than convergence.

### S3 — Constrained openness · **Major (course-wide) — this is Goal (a)**
Code HWs prescribe *how* ("use `np.column_stack`", "use `np.linalg.inv`", "use the `@`
operator") and then grade by matching the resulting numbers, so exactly one path passes.
There is very little rubric-scored written reasoning (interpretation, trade-offs,
limitations) anywhere in the code HWs. The per-assignment **(a)** proposals below convert
representative checks to outcome-based wording ("achieve property X, justify in 3–5
sentences").

### S4 — jupytext module-level execution & import-time side effects · **Major / Minor**
Tests import module-level names (`from hw import w, ...`), so a student whose notebook
runs top-to-bottom is fine, but any cell left unrun yields `ImportError`/`NameError`
that *looks* like a logic failure. Worse, some modules do real work at import:
`hw16/hw.py` builds a sampler and (per the file) drives sampling/plotting at module
scope; `hw17/hw.py` calls `plot_samples_needed()` at module scope. That runs during test
*collection* — slow, and fragile under the 10s CI timeout. Recommendation: guard
side-effecting/plotting code with `if __name__ == "__main__":`.

### S5 — Integrity is handled, with one latent risk · **Minor**
Solution stripping works (see corrected claim #2). The latent risk: `make_release` for
Typst HWs just runs `make`, which relies on `without_answers` remaining the **first**
target in each `Makefile`. If a `Makefile` is ever reordered (or a stray default `all:`
added that points at `with_answers`), the released `hw.pdf` would leak answers silently.
Consider an explicit `release:` target or having `make_release` call
`make without_answers` by name.

### S6 — Seeding is inconsistent · **Major**
The course both over-pins seeds (S2: hw6, hw16 assert exact draws) and under-seeds
(hw17 `RNG = np.random.default_rng()` with no seed → nondeterministic tests; the
4-D/1000-sample case is statistically marginal and will flake). Pick one discipline:
seed for reproducibility **and** assert *distributional/convergence* properties, not exact
draws.

---

# Phase 1 & 2 — Per-assignment

Each section: objectives → concepts (week) → quality → issues → revision proposals
(a: openness, b: thresholds) → prioritized edit plan.

---

## `hw0` — Intro to GitHub Classroom, Pytest, LaTeX
- **Objectives:** *explicit* — submit via GitHub Classroom (PR workflow), typeset a basic
  LaTeX doc, run pytest; *inferred* — git basics, read integrity policy.
- **Concepts (Week 0):** course infrastructure, not ML.
- **Quality:** Clear and appropriately scaffolded (~1–2h). The single test
  `test_add()` asserts `add(1,1)==2` — a hardcoded `return 2` would pass (false positive).
  Exact match is correct here (closed-form), so the fix is coverage, not tolerance.
- **Issues:** **Minor** — single input allows a constant-return false positive.
- **(a) Openness:** fine as an onboarding task; optionally add an ungraded one-line
  reflection ("what was the bug?"). No change needed for grading.
- **(b) Thresholds:** keep exact (addition is exact); add inputs to close the loophole:
  `assert add(2,3)==5; assert add(-1,1)==0; assert add(0,0)==0`.
- **Edit plan:** *Minor* — add 3 assertions to `hw0/test_hw.py`.

## `hw1` — Simple linear model + scalar normal equations
- **Objectives:** *explicit* — implement a single-variable least-squares model, predict;
  derive normal equations on the (hardcopy) worksheet. *inferred* — load CSV, numpy.
- **Concepts (Week 1):** scalar linear regression, closed-form least squares.
- **Quality:** Clear, ~3–4h with the worksheet. Test asserts `w0`/`w1` to reference
  values; **no test exercises `predict()`** — a student with correct fit and a broken
  `predict` still passes. Coefficient pinning = S2/S3.
- **Issues:** **Major** — grade measures learned coefficients, not the capability
  ("can fit a line and predict"); `predict` uncovered. **Minor** — worksheet is hardcopy,
  no timestamped backup.
- **(a) Openness — before→after:**
  - *Before:* "Implement `w1` and `w0` using the formulas above."
  - *After:* "Fit a single-variable least-squares model to the data and implement
    `predict(year)`. Your model must reproduce the closed-form least-squares fit
    (checked: predictions match to tolerance) — you may compute it however you like
    (normal equations, `np.polyfit`, `lstsq`). In 2–3 sentences, state what `w0` and `w1`
    mean in the units of this dataset." (reasoning part is rubric-scored)
- **(b) Thresholds — test capability, not coefficients:**
  ```python
  def test_fit_quality():
      x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)
      m = SimpleLinearModel(); m.train(x, t)
      # RMSE floor instead of pinning w0/w1
      rmse = np.sqrt(np.mean((m.predict(x) - t)**2))
      assert rmse <= 0.30, f"train RMSE {rmse:.3f} exceeds 0.30s"
  def test_prediction_reasonable():
      ...
      assert m.predict(2012) == approx(9.5947138520, rel=1e-3)  # the documented target
  ```
  Keep one tolerance-relaxed prediction check (the "verify it matches last HW" goal); drop
  the exact `w0`/`w1` pins.
- **Edit plan:** *Major* — add `predict` coverage + RMSE floor, relax/replace coefficient
  pins (`hw1/test_hw.py`); reword the prompt for path-independence + add reasoning blank
  (`hw1/hw.py`). *Minor* — note worksheet backup option (`hw1/README.md`).

## `hw2` — Normal equations in matrix/vector form (+ Table 1.4 identities, written)
- **Objectives:** *explicit* — build design matrix, solve `ŵ=(XᵀX)⁻¹Xᵀt`, predict, extend
  to 2nd-order; derive FCML Table 1.4 identities (written).
- **Concepts (Week 2):** matrix least squares, design matrices, polynomial features.
- **Quality:** Clear, ~4–5h. Three tests pin `w`, the 2012 prediction, and
  `w_second_order`. Tests import module-level `w, winning_time_for_2012, w_second_order`
  (S4) — a cell left unrun reads as a logic failure. No 2nd-order *prediction* check.
- **Issues:** **Major** — module-level import coupling (S4) + coefficient pinning (S2/S3).
  **Minor** — 2nd-order prediction uncovered; design-matrix shape only implicitly checked.
- **(a) Openness — before→after:**
  - *Before:* prescriptive "use `column_stack`/`linalg.inv`/`@`".
  - *After:* "Construct a design matrix and fit a degree-1 and degree-2 polynomial by
    least squares (any correct method). Predictions must match the closed-form fit to
    tolerance. Add one sentence: what does adding the `x²` column change about the fit?"
- **(b) Thresholds / structure (order-independent where possible):**
  ```python
  def test_design_matrix_structure():
      X = build_design_matrix(x, order=1)
      assert X.shape == (len(x), 2)
      assert np.allclose(X[:, 0], 1.0)          # intercept column present
      assert set(np.round(X[:,1],6)) == set(np.round(x,6))  # feature column = x (any order check as appropriate)
  def test_predictions_match_fit():
      assert model.predict(2012) == approx(9.5947138520, rel=1e-3)
      assert model_2.predict(2012) == approx(9.8683030743, rel=1e-3)
  ```
  Keep exact only for genuinely closed-form scalars, with `rel=1e-3` headroom.
- **Edit plan:** *Major* — load data inside tests / assert on functions instead of pinned
  module globals (S4); add structural checks; relax coefficient pins (`hw2/test_hw.py`).
  *Minor* — add 2nd-order prediction test; reasoning blank (`hw2/hw.py`).

## `hw3` — Polynomial regression, cross-validation, scaling, seeding
- **Objectives:** *explicit* — `PolynomialRegressionModel` class, scale to [0,1], visualize
  overfitting, implement K-fold CV and LOOCV (K=N), set a seed; answer 2 short questions.
- **Concepts (Week 3):** polynomial features, overfitting, K-fold/LOOCV, scaling, seeding.
- **Quality:** The richest early HW (~6–8h). Tests (6) cover design-matrix shape,
  `initialize_design_matrix`, params (orders 1–2), predictions (orders 1–2), and `scale`
  (one hardcoded 10-element case). **Cross-validation — the central new topic — is never
  called by any test** (confirmed in `hw3/test_hw.py`): a student can ship a broken
  `run_K_fold_cv` (off-by-one folds, leaking scaling, wrong mean) and pass everything
  (false positive). The two open questions (Q1 "at which order does the fit worsen?",
  Q2 "dimensions of `stack`?") have no rubric.
- **Issues:** **Major** — CV objective untested (false positives on the headline skill).
  **Major** — open questions ungraded/no rubric (S1). **Minor** — `scale` tested on one
  hardcoded case only; seeding/reproducibility not enforced; orders 3–8 uncovered.
- **(a) Openness — before→after:**
  - *Before:* Q1/Q2 as free text, ungraded; "implement K-fold CV" with prescribed loops.
  - *After:* "Use cross-validation to select a polynomial order. Report the selected order
    and the CV curve, and justify the choice in 3–5 sentences (bias/variance, what the
    plots show). Any correct CV scheme is fine as long as scaling happens *inside* each
    fold (no leakage)." Rubric-score the justification + a leakage check.
- **(b) Thresholds — make the objective testable without pinning a method:**
  ```python
  def test_scale_is_unit_range():               # property, replaces single hardcoded case
      a = rng.random(50)
      s, lo, rng_ = scale(a)
      assert s.min()==approx(0.0) and s.max()==approx(1.0)
      assert lo==approx(a.min()) and rng_==approx(a.max()-a.min())
  def test_kfold_cv_runs_and_is_sane():
      losses = run_K_fold_cv(K=5, order=3, data=shuffled)   # adapt to real signature
      assert np.all(np.isfinite(losses)) and np.all(losses >= 0)
  def test_loocv_fold_count():
      assert num_folds(K=len(x)) == len(x)        # LOOCV ⇒ N folds
  def test_cv_prefers_low_order():                # overfitting signal, not exact loss
      assert np.argmin(cv_mean_loss_by_order) < 8
  ```
  Keep exact (with `rel=1e-3`) only for the closed-form order-1/2 predictions.
- **Edit plan:** *Major* — add CV smoke + sanity + LOOCV-fold tests (`hw3/test_hw.py`);
  add Q1/Q2 rubric (`hw3/README.md` or `hw.tex`). *Minor* — property-based `scale` test;
  enforce/assert seeding; reword CV section to outcome-based (`hw3/hw.py`).

## `hw4` — Poisson probabilities
- **Objectives:** *explicit* — compute `P(2≤X≤6)` and its complement for `X~Poisson(3)`.
  *inferred* — PMF, complementary counting, tail decay.
- **Concepts (Week 4/Module 2):** Poisson PMF, law of total probability.
- **Quality:** Tight, ~15–30 min. Two tests pin the two probabilities — **correctly**
  exact (closed-form). Gaps: no direct `poisson()` test, no sanity invariants.
- **Issues:** **Minor** — no property checks (`prob_a+prob_b==1`, PMF∈[0,1]); no direct
  check of the `poisson` helper (errors only surface composed).
- **(a) Openness:** appropriate to keep constrained at this level; optionally generalize
  to `pmf_range(low, high, lam)` so the same code answers any interval (small openness win).
- **(b) Thresholds:** keep the two exact values; **add invariants** (these catch the common
  "returned `prob_a` twice" bug that exact-only can miss):
  ```python
  def test_complement(): assert calc_a()+calc_b()==approx(1.0, abs=1e-10)
  def test_pmf_bounds(): assert all(0<=poisson(x,3)<=1 for x in range(20))
  ```
- **Edit plan:** *Minor* — add complement + bounds tests (`hw4/test_hw.py`); document
  `poisson` domain (`hw4/hw.py`).

## `hw5` — Derive the MLE for a Bernoulli parameter *(written)*
- **Objectives:** *explicit* — write the likelihood for N i.i.d. Bernoulli samples, show a
  unique maximum, derive `r̂ = (Σxᵢ)/N`.
- **Concepts (Module 2):** likelihood, log-likelihood, second-derivative test, MLE.
- **Quality:** Clear three-part progression, ~45–90 min. Graded only by S1's coarse rubric.
- **Issues:** **Major (S1)** — no partial-credit rubric for a 3-part derivation. **Minor**
  — no nudge toward log-likelihood (students rediscover it).
- **(a) Openness:** add an interpretation part — "Explain in 2–3 sentences why the MLE
  equals the sample mean, and one case where that estimate is misleading." (rubric-scored)
- **(b) Thresholds:** N/A (hardcopy). Replace S1 rubric with the per-part scheme in S1.
- **Edit plan:** *Major* — per-part rubric (`hw5/README.md`). *Minor* — optional hints +
  time estimate (`hw5/hw.tex`).

## `hw6` — Expectations: analytic vs. Monte-Carlo sampling
- **Objectives:** *explicit* — compute `E[f(X)]` analytically (written) and by sampling
  (code), visualize convergence to the true value.
- **Concepts (Module 2):** expectation as integral, Monte-Carlo estimation, LLN, seeding.
- **Quality:** Good scaffolding, ~60–90 min. **The one test pins `expectations[0:10]` and
  the final value to draws from `default_rng(100)`** — this asserts the exact RNG stream,
  which is the genuine cross-version false-negative risk in S2/S6, and it tests "did you
  reproduce my draws" rather than "does your estimator converge".
- **Issues:** **Major (S2/S6)** — exact pinned RNG draws; brittle and off-target. **Minor**
  — no `f(x)` spot check; convergence/bounds never asserted.
- **(a) Openness — before→after:**
  - *Before:* "match these expectation values."
  - *After:* "Estimate `E[f(X)]` by Monte-Carlo and show convergence. Your final estimate
    (≥10⁴ samples) must be within 2% of the analytic value; the running estimate must
    stabilize. Briefly explain the `O(1/√N)` error trend you observe." (any seed allowed)
- **(b) Thresholds — distributional, not draw-pinned:**
  ```python
  def test_f_values(): assert f(0)==approx(35.0); assert f(1)==approx(35.21)
  def test_converges_to_truth():
      assert expectations[-1] == approx(TRUE_EXPECTATION, rel=0.02)
  def test_running_estimate_stabilizes():
      assert np.var(expectations[-10:]) <= np.var(expectations[:10])
  ```
  If exact reproduction is still wanted, pin numpy in `requirements.txt` and *document*
  that the values assume that exact version — but prefer the distributional form.
- **Edit plan:** *Major* — replace pinned-array test with convergence/bounds + `f` check
  (`hw6/test_hw.py`); reword to outcome-based, any-seed (`hw6/hw.py`, `hw6/hw.tex`).
  *Minor* — apply S1 rubric to the written derivation.

## `hw7` — Practice with Jacobians *(written)*
- **Objectives:** *explicit* — three matrix-calculus proofs (`∂w/∂w=I`; gradient/transpose
  relation; `∂(Cw)/∂wᵀ=C`).
- **Concepts (Module 2):** Jacobians, Kronecker delta, transpose rules — feeds the logistic
  Hessian later.
- **Quality:** Clear progression, ~60–120 min. Uses "compact derivative notation" assumed
  from lecture. Graded by S1 rubric only.
- **Issues:** **Major (S1)** — no per-proof credit (3 independent proofs → ternary grade).
  **Minor** — notation not defined in the student doc; no textbook pointer.
- **(a) Openness:** these are proofs (one correct result each) — keep them, but accept any
  valid derivation route (index expansion *or* identity-based). Add: "after Proof 3, state
  in one sentence where this identity is used in logistic regression."
- **(b) Thresholds:** N/A. Use S1's per-proof rubric (1/proof).
- **Edit plan:** *Major* — per-proof rubric (`hw7/README.md`). *Minor* — define notation +
  textbook ref (`hw7/hw.typ`).

## `hw8` — Multivariate normals; MLE unbiasedness; Beta moments *(written)*
- **Objectives:** *explicit* — factor a diagonal-covariance Gaussian into independents;
  show the hw5 MLE is unbiased; compute `E[r]`, `Var(r)` for a Beta density.
- **Concepts (Module 2):** MVN independence, unbiasedness, Beta/Gamma identities.
- **Quality:** Four proofs in one assignment, ~60–90 min. Forward-references hw5 without
  restating it. S1 rubric only.
- **Issues:** **Major (S1)** — one ternary grade for four multi-step proofs. **Minor** —
  hw5 result not restated; no time estimate.
- **(a) Openness:** add interpretation — "explain *why* diagonal covariance implies
  independence for Gaussians but not in general." (rubric-scored)
- **(b) Thresholds:** N/A. Per-problem rubric (0.25 each ×4, with partial tiers).
- **Edit plan:** *Major* — per-problem rubric (`hw8/README.md`). *Minor* — restate hw5 MLE
  inline + time estimate (`hw8/hw.typ`).

## `hw9` — Fisher information of a Bernoulli parameter *(written)*
- **Objectives:** *explicit* — derive `I(r)=1/(r(1−r))` from the definition.
- **Concepts (Module 2):** Fisher information, curvature of log-likelihood.
- **Quality:** Single, well-scoped derivation, ~15–20 min. S1 rubric only.
- **Issues:** **Major (S1)** — single ternary grade can't distinguish setup vs. expectation
  vs. final-form errors.
- **(a) Openness:** add "interpret how `I(r)` behaves as `r→0` or `r→1`, and what that says
  about estimating rare events." (rubric-scored)
- **(b) Thresholds:** N/A. Sub-step rubric (setup .5 / expectation .3 / closed form .2).
- **Edit plan:** *Major* — sub-step rubric (`hw9/README.md`).

## `hw10` — Predictive variance computation
- **Objectives:** *explicit* — implement `Cov(ŵ)=σ²(XᵀX)⁻¹` and predictive variance
  `σ²·xᵀ(XᵀX)⁻¹x`; interpret why error bars widen in the data gap.
- **Concepts (Module 2, S12):** parameter covariance, predictive uncertainty.
- **Quality:** Excellent scaffolding (~45–60 min). **One test**, pinning a scalar
  predictive variance and the four entries of a 2×2 covariance on a 3-point toy set. The
  headline learning objective — *variance grows where there's no data* — is never tested;
  no symmetry/PSD checks; no vectorization check.
- **Issues:** **Major** — coefficient/matrix pinning (S2/S3) + the core "gap" objective
  untested; written caption rubric undocumented (S1). **Minor** — N=3 toy data; RNG state
  threaded across calls.
- **(a) Openness — before→after:**
  - *Before:* "implement these two formulas exactly."
  - *After:* "Quantify prediction uncertainty for this model. Implement parameter
    covariance and predictive variance, then explain (with your plot) why variance grows
    in the gap `2.5≤x≤4.5`. Compare orders 1, 3, 5, 9." (explanation rubric-scored)
- **(b) Thresholds — properties + behavior:**
  ```python
  def test_cov_is_symmetric_psd():
      assert np.allclose(C, C.T)
      assert np.all(np.linalg.eigvalsh(C) > 0)
  def test_predictive_variance_vectorized_nonneg():
      v = m.predictive_variance(np.array([0.5, 1.5, 2.5]))
      assert v.shape == (3,) and np.all(v >= 0)
  def test_variance_larger_in_gap():
      assert m.predictive_variance([3.5])[0] > m.predictive_variance([1.5])[0]
  ```
- **Edit plan:** *Major* — replace pinned values with PSD/symmetry/vectorization/gap tests
  (`hw10/test_hw.py`); document caption rubric (`hw10/README.md`). *Minor* — larger test
  data; outcome-based wording (`hw10/hw.py`).

## `hw11` — Exact Bayesian inference for the coin game
- **Objectives:** *explicit* — implement `B(a,b)`, `Beta(r,a,b)`, conjugate `posterior`,
  log-space marginal likelihood, and `P(win)` across three priors.
- **Concepts (Module 3, S17):** Beta-Bernoulli conjugacy, evidence, predictive prob.
- **Quality:** Strong narrative + scaffolding (~90–120 min). 12 tests, but they assert
  **100-element posterior/prior arrays** and high-precision scalars, and run through a
  per-scenario fixture: if `B()` is wrong, the fixture throws and *every* downstream test
  fails with a confusing setup error (cascade) — there are **no isolated unit tests** for
  `B`/`Beta`/`posterior`. Some references are genuinely closed-form (marginal likelihood
  `≈1/21`) and fine to keep.
- **Issues:** **Major** — no per-function unit tests → cascading false negatives;
  array-pinning (S2). **Major** — written caption rubric undocumented (S1). **Minor** —
  no edge cases (`r∈{0,1}`, extreme priors); log-space stability not directly checked.
- **(a) Openness:** add interpretation — "compare the three priors: how does prior strength
  move the posterior and `P(win)`? Which prior would you choose and why?" (rubric-scored).
  Keep the math functions exact (they have right answers).
- **(b) Thresholds — unit-test against references, add properties:**
  ```python
  def test_B_matches_gamma(): assert B(2,3)==approx(gamma(2)*gamma(3)/gamma(5), rel=1e-10)
  def test_Beta_matches_scipy(): assert Beta(r,5,3)==approx(scipy_beta.pdf(r,5,3), rel=1e-8)
  def test_posterior_is_conjugate():
      assert posterior(r,N,yN,a,b)==approx(Beta(r,a+yN,b+N-yN), rel=1e-8)
  def test_pwin_in_unit_interval(): assert 0<=calc_pwin(N,yN,a,b)<=1
  ```
  These isolate failures and stop the cascade; drop the 100-element array pins.
- **Edit plan:** *Major* — add isolated unit tests for `B`/`Beta`/`posterior`, replace
  array pins with property/conjugacy/bounds checks (`hw11/test_hw.py`); document caption
  rubric (`hw11/README.md`). *Minor* — edge cases; note log-space in docstring (`hw11/hw.py`).

## `hw14` — MAP via Newton-Raphson (code) + NR update for Poisson regression (written)
- **Objectives:** *explicit* — implement `logistic`, `gradient`, `hessian`; run Newton-
  Raphson to the MAP; derive the NR update for Poisson likelihood + Gaussian prior.
- **Concepts (Module 4, S22):** MAP, Newton-Raphson, gradient/Hessian.
- **Quality:** Good scaffolding (~1.5–2.5h code + 1–2h written). `test_gradient_function`
  runs **exactly 10** NR steps from `w=0` and asserts the resulting `w` — coupling the
  grade to iteration count/initialization (S2), not convergence. `hessian` is only tested
  indirectly; the written derivation is S1-graded.
- **Issues:** **Major** — exact-iterate pin (S2); `hessian` not directly tested; written
  derivation no rubric (S1). **Minor** — no numerical-stability edge cases (logistic
  saturating to 0/1).
- **(a) Openness — before→after:**
  - *Before:* "run 10 iterations and match this `w`."
  - *After:* "Find the MAP by Newton-Raphson. Iterate until `‖gradient‖<1e-4` (report your
    iteration count). Implement the gradient and Hessian. Briefly: why is Newton-Raphson
    well-suited here, and what does the Hessian represent?" (reasoning rubric-scored)
- **(b) Thresholds — converged properties, not the iterate:**
  ```python
  def test_converges_to_stationary_point():
      w = newton_raphson(...)               # student's loop or a tolerance loop
      assert np.linalg.norm(gradient(w, X, t, sig_sq)) < 1e-3
      assert np.all(np.isfinite(w))
      assert w == approx([1.63985881, 1.99983755], rel=1e-2, abs=5e-2)  # location, loose
  def test_hessian_negative_definite():
      H = hessian(w_star, X, sig_sq)
      assert np.all(np.linalg.eigvalsh(H) < 0)
  ```
- **Edit plan:** *Major* — convergence-property + direct Hessian tests, relaxed location
  check (`hw14/test_hw.py`); per-step written rubric (`hw14/README.md`). *Minor* —
  stability note + outcome-based wording (`hw14/hw.py`, `hw14/hw.typ`).

## `hw15` — Laplace approximation (code) + Laplace for Beta/Binomial (written)
- **Objectives:** *explicit* — Laplace posterior for Bayesian logistic regression
  (`w_MAP` + `cov = (−H)⁻¹`), sample from it; derive the Beta/Binomial Laplace case.
- **Concepts (Module 4, S23):** Laplace approximation, inverse-Hessian covariance.
- **Quality:** Excellent scaffolding, reuses hw14 (~1h code + 1.5–2h written). Two tests
  pin `w_MAP` (the **same exact iterate as hw14** → inherits hw14's brittleness) and all
  four `g_cov` entries. No PSD/symmetry check (which would actually catch a wrong Hessian).
  Written part S1-graded.
- **Issues:** **Major** — exact `w_MAP`/`g_cov` pinning, cascading from hw14 (S2); no
  PSD/symmetry/conditioning check; written no rubric (S1). **Minor** — no
  near-singular-Hessian edge case.
- **(a) Openness:** "Approximate the posterior with a Gaussian and justify when Laplace is
  reasonable here; compare your sampled covariance to the analytic `(−H)⁻¹`." (rubric)
- **(b) Thresholds:**
  ```python
  def test_cov_symmetric_psd_well_conditioned():
      assert np.allclose(g_cov, g_cov.T)
      assert np.all(np.linalg.eigvalsh(g_cov) > 0)
      assert np.linalg.cond(g_cov) < 100
  def test_cov_close_to_reference():
      assert g_cov == approx(REF, rel=2e-2, abs=1e-1)   # location, not exact
  def test_samples_recover_cov():
      assert np.cov(samples_1000.T) == approx(g_cov, rel=0.2)  # 1000-draw sanity
  ```
- **Edit plan:** *Major* — PSD/symmetry/conditioning + relaxed location + sample-recovery
  tests (`hw15/test_hw.py`); written rubric (`hw15/README.md`). *Minor* — outcome-based
  wording (`hw15/hw.py`, `hw15/hw.typ`).

## `hw16` — Metropolis-Hastings MCMC for Bayesian logistic regression
- **Objectives:** *explicit* — implement `MetropolisSampler` (`log_likelihood`,
  `log_prior`, `sample_from_proposal`, `compute_acceptance_ratio`, `generate_sample(s)`)
  and run a chain.
- **Concepts (Module 4, S25):** MH-MCMC, proposals, log-scale acceptance.
- **Quality:** Good method-by-method scaffolding (~2–3h). `log_likelihood`/`log_prior`/
  `compute_acceptance_ratio` tests assert hardcoded values (reasonable: deterministic given
  data). **`test_generate_sample`/`test_generate_samples` assert the exact accepted draws
  *and* the exact accept/reject pattern under `seed=100`** — this couples the grade to the
  precise RNG call order inside the student's code (a correct sampler that draws the
  proposal and the uniform in a different order fails) and to RNG-stream stability (S2/S6).
  Module-level sampling/plotting runs at import (S4). *(The "prior_variance 2 vs 0.5"
  inconsistency reported elsewhere is not a bug — see corrected claim #1.)*
- **Issues:** **Major** — exact pinned draws + accept/reject pattern (S2/S6). **Minor** —
  import-time side effects (S4); no convergence/posterior-recovery checks.
- **(a) Openness:** "Implement an MH sampler whose stationary distribution is the posterior.
  Demonstrate it by recovering the Laplace posterior mean/covariance from hw15 within
  tolerance, and comment on mixing / acceptance rate." (any internal RNG order allowed)
- **(b) Thresholds — formula checks + distributional recovery, not pinned draws:**
  ```python
  def test_log_likelihood_formula():
      P = 1/(1+np.exp(-X@w)); exp = (t*np.log(P)+(1-t)*np.log(1-P)).sum()
      assert sampler.log_likelihood(w)==approx(exp)
  def test_acceptance_ratio_formula():
      logr = (s.log_prior(c)+s.log_likelihood(c))-(s.log_prior(w)+s.log_likelihood(w))
      assert s.compute_acceptance_ratio(w,c)==approx(np.exp(logr))
  def test_proposal_shape_and_reproducible():   # keep seed check, drop value pin
      assert cand.shape==(2,)
  def test_chain_recovers_posterior():
      chain = s.generate_samples(20000)[5000:]   # burn-in
      assert chain.mean(0)==approx(W_MAP, rel=0.1, abs=0.1)
  ```
- **Edit plan:** *Major* — replace pinned-draw tests with formula + posterior-recovery
  tests (`hw16/test_hw.py`). *Minor* — guard plotting/sampling with `__main__` (S4),
  `hw16/hw.py`; add a written component or note its absence.

## `hw17_under_construction` — Estimating π by sampling (2-D, 3-D, n-D)
- **Objectives:** *explicit* — rejection-sample π via the circle, sphere, and n-ball;
  observe the curse of dimensionality.
- **Concepts (Module 4, S25):** Monte-Carlo integration, n-ball volume, acceptance rates.
- **Quality / status:** **Under construction and currently broken.** `test_hw.py` imports
  `estimate_pi_using_sphere` (line 8), but `hw17/hw.py` defines only
  `estimate_pi_using_circle`, `estimate_pi_using_n_ball`, `estimate_pi_n_ball_running`
  (confirmed by grep). The import fails at **collection**, so *all three* hw17 tests error
  before running. Separately, `RNG = np.random.default_rng()` is unseeded → tests are
  nondeterministic, and the `(dim=4, samples=1000)` case is statistically marginal
  (acceptance ≈ 6%) → it will flake even when correct. `plot_samples_needed()` runs at
  import (S4). Notably, hw17's tests are the one place already using **threshold** style
  (`approx(pi, rel=...)`) — the right direction, just under-seeded.
- **Issues:** **Blocker** — missing `estimate_pi_using_sphere` ⇒ import error fails the
  suite; assignment incomplete. **Major (S6)** — unseeded RNG + marginal 4-D tolerance ⇒
  flaky. **Minor** — import-time plotting (S4); no test for `number_of_orthants`/running
  estimates.
- **(a) Openness:** already outcome-based (converge to π within tolerance). Keep that;
  add "explain, with your log-log plot, why the n-ball acceptance rate collapses as n
  grows." (rubric-scored)
- **(b) Thresholds — seed + widen marginal cases:**
  ```python
  # seed once for determinism, keep the convergence (threshold) style
  def test_circle(): assert estimate_pi_using_circle(100_000)==approx(pi, rel=0.02)
  def test_sphere(): assert estimate_pi_using_sphere(100_000)==approx(pi, rel=0.02)
  def test_nball():
      for dim, n, tol in [(2,100_000,0.02),(3,100_000,0.03),(4,200_000,0.05)]:
          assert estimate_pi_using_n_ball(dim, n)[-1]==approx(pi, rel=tol)
  ```
- **Edit plan:** *Blocker* — implement `estimate_pi_using_sphere` (`hw17/hw.py`) so the
  suite imports and runs. *Major* — seed the RNG (configurable) and raise sample counts /
  tolerances on marginal dims (`hw17/hw.py`, `hw17/test_hw.py`). *Minor* — guard plotting
  with `__main__`; add helper tests. Mark "ready" only once the suite passes.

---

# Phase 3 — Summary & approval gate

**No assignment files have been modified.** Counts use the normalized severities above;
"systemic" items (S1/S2/etc.) are counted once in the assignment where they bite, not
multiplied across the course.

| HW | Blk | Maj | Min | Headline recommendation |
|----|:--:|:--:|:--:|---|
| hw0 | 0 | 0 | 1 | Add 3 assertions to close the constant-return loophole. |
| hw1 | 0 | 1 | 2 | Test `predict` + an RMSE floor; stop pinning `w0/w1`; add reasoning blank. |
| hw2 | 0 | 1 | 2 | Load data inside tests (kill module-global coupling); add structural checks. |
| hw3 | 0 | 2 | 3 | **Test cross-validation** (currently untested) + rubric the open questions. |
| hw4 | 0 | 0 | 3 | Keep exact values; add complement/bounds invariants. |
| hw5 | 0 | 1 | 1 | Per-part derivation rubric (S1). |
| hw6 | 0 | 1 | 1 | Replace pinned RNG draws with convergence/bounds tests (S2/S6). |
| hw7 | 0 | 1 | 1 | Per-proof rubric (S1); define notation. |
| hw8 | 0 | 1 | 1 | Per-problem rubric (S1); restate hw5 result inline. |
| hw9 | 0 | 1 | 0 | Sub-step rubric (S1). |
| hw10 | 0 | 1 | 1 | Replace pinned cov/var with PSD/symmetry/gap-behavior tests. |
| hw11 | 0 | 2 | 1 | Add isolated unit tests (stop the fixture cascade); rubric captions. |
| hw14 | 0 | 1 | 1 | Test convergence + Hessian directly, not the 10th iterate. |
| hw15 | 0 | 1 | 1 | PSD/symmetry/conditioning + relaxed location; de-couple from hw14. |
| hw16 | 0 | 1 | 1 | Replace pinned draws with formula + posterior-recovery tests. |
| hw17 | **1** | 1 | 1 | **Implement `estimate_pi_using_sphere` (suite is broken); seed the RNG.** |
| **Total** | **1** | **17** | **23** | |

**Course-wide priorities (do these once, benefit everywhere):**
1. **S2/S6 — stop pinning learned/stochastic values.** Convert autograders to capability
   tests: performance floors (RMSE/accuracy), structural/property checks (shape, column
   set, dtype, symmetry, PSD, bounds, monotonicity, conjugacy), and convergence/
   distributional checks for anything random. Keep exact match only for genuinely
   closed-form scalars, with a little `rel` headroom.
2. **S1 — replace the 1/0.5/0 rubric** with per-part rubrics for the written HWs (and the
   written portions of code HWs). This is the prerequisite for adding the open,
   interpretation-style parts in every **(a)** proposal.
3. **S3 — open up the wording.** Specify *what* to achieve and require a short rubric-scored
   justification, instead of prescribing the exact numpy calls and grading the numbers.
4. **S4 — guard import-time side effects** (`if __name__ == "__main__":`) and load data
   inside tests rather than importing module globals.

**The one true Blocker:** `hw17` (`estimate_pi_using_sphere` missing → whole suite errors
on import).

---

## Awaiting your approval

Per the plan, I've stopped here and changed nothing. Tell me which to apply and I'll do
them **one assignment at a time, showing a diff for each before saving.** Some ways to
scope it:

- **"Fix the Blocker"** — just `hw17` (implement the missing function + seed the RNG).
- **"Do the systemic fixes"** — S1 (rubrics) and/or S2 (threshold tests) across the board.
- **"Start with hw3"** (or any single HW) — apply its full edit plan as a worked example,
  then decide whether to roll the pattern out.
- **"All Majors"**, **"everything"**, or your own selection.

I'd also suggest the separately-approved step of **running each `test_hw.py` against its
reference `hw.py`** before/after edits, to confirm the false-negative risks (esp. hw6/hw16
RNG pinning) empirically rather than by inspection.
