# HW3 — Regression & Model Selection

> Overhauled (Scope-A pilot). Grading is **specifications-based**: three weighted spec
> bundles, each earned **pass / revise** rather than by fractional points. The shared
> interpretation rubric is in `rubric.md`.

## 1. Context & purpose

Flexible models can fit training data arbitrarily well and still generalize badly. Here
you'll cause that failure directly and use **cross-validation** to choose model complexity —
the workhorse you'll reuse all term.

## 2. Learning objectives

- **O1** Build polynomial features and fit by least squares. *(apply — Correctness)*
- **O2** Scale features to a known range **without leaking** validation information.
  *(apply/analyze — Correctness + Interpretation)*
- **O3** Use cross-validation to select a model order. *(analyze — Correctness + Interpretation)*
- **O4** Explain the bias–variance trade-off from your own results. *(evaluate — Interpretation)*

## 3. The task (outcome, not recipe)

Fit polynomial models of orders 1–8 to the Olympic 100m data, with features scaled to
`[0, 1]`. Use cross-validation to select an order and produce the CV-error-vs-order curve.

## 4. What you may and may not use

- Fit by **any correct method** — normal equations, `np.linalg.lstsq`, `np.polyfit`.
- Use **any CV implementation** — manual K-fold, LOOCV, `sklearn.model_selection.KFold`.
- **You may not** compute the scaling statistics on the validation fold (no leakage): fit
  the scaler on training data only.

## 5. How you'll be assessed (criteria shown up front)

| Bundle | Weight | Pass when… |
|--------|:------:|------------|
| **Correctness** | **55%** | the autograder is green — see the specs in `test_hw.py` (scaling is a proper `[0,1]` map; design matrix shape + intercept; order-1/2 predictions match the closed-form fit to `rel=1e-3`; a model fits; CV returns finite non-negative per-order losses; LOOCV uses N folds; CV penalizes over-complex models). |
| **Interpretation** | **35%** | prompts I1–I3 (§6) each reach **Proficient+** on every dimension of `rubric.md`. |
| **Process** | **10%** | seeded (`np.random.default_rng` is provided), the notebook runs top-to-bottom, the CV plot is labeled, code is readable. |

**Revision:** Correctness re-runs on every push (iterate to green). Interpretation gets one
revision in the posted window.

## 6. Required interpretation (answer in the markdown cells of `hw.py`)

- **I1** Which order did CV select, and **why** — in bias–variance terms?
- **I2** What do the CV curve and the train-vs-CV gap show about overfitting?
- **I3** Name one situation where CV here could mislead you (e.g., tiny N, leakage,
  non-i.i.d. data).

## 7. Going further (optional, ungraded)

Repeat with a different CV scheme (5-fold vs LOOCV) and comment on the **variance** of the
estimate.

## 8. Submission & reproducibility (the autograder's contract)

Commit and push `hw.py` (code + the I1–I3 markdown answers), `hw.tex`/`hw.pdf` (plots +
captions). Keep the provided seed. The autograder imports these from `hw.py`, so the
**function/return contract must hold**:

- `PolynomialRegressionModel(order)` with `get_design_matrix_shape`, `create_design_matrix`,
  `train`, `predict` as given.
- `scale(array)` → `(scaled_array, array_min, array_range)`.
- **`run_K_fold_cv(K, P, data)` must return a length-`P` 1-D NumPy array** whose element
  `p-1` is the mean validation loss (over the K folds) for polynomial order `p`. *(This is
  an output contract; you may still implement the CV however you like.)*

Run the tests locally before submitting: `pytest test_hw.py`.
