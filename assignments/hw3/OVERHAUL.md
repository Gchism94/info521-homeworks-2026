# hw3 — Overhaul draft (Scope A pilot · gold-standard instance)

Instantiates `OVERHAUL_FRAMEWORK.md` on hw3 (Polynomial regression, cross-validation,
scaling, seeding). **Draft only — no hw3 files are modified.** Apply behind the review
gate, then run `test_hw.py` against the reference `hw.py` before moving on.

Real API confirmed in `hw3/hw.py`:
`PolynomialRegressionModel(order)` with `get_design_matrix_shape(x)`,
`initialize_design_matrix(shape)`, `fill_design_matrix(X, x)`, `create_design_matrix(x)`,
`compute_mse_loss(x, t)`, `train(x, t)`, `predict(x)`; `scale(array) -> (scaled, min, range)`;
`run_K_fold_cv(K, P, data)` (currently returns `None`, only plots); `rng = np.random.default_rng(0)`
and `stack_shuffled` already exist. **There is no `num_folds`/`design_matrix`/`cv_mean_loss`
helper** — the tests below use the real names, and the one required contract change is
called out in §4.

---

## 1. Prompt rewritten into the 8-part template

> Replaces the body of `hw3/README.md` and the lead markdown cells of `hw3/hw.py`. The two
> ungraded free-text questions (`### YOUR ANSWER HERE ###` at `hw.py:186` and `:416`) are
> promoted into the rubric-scored Required Interpretation block.

**1. Context & purpose.** Flexible models can fit training data arbitrarily well and still
generalize badly. Here you'll see that failure directly and use cross-validation to choose
model complexity — the workhorse you'll reuse all term.

**2. Learning objectives.** By the end you can:
- **O1** Build polynomial features and fit by least squares. *(Bloom: Apply — autograded)*
- **O2** Scale features to a known range without leaking validation information.
  *(Apply/Analyze — autograded + rubric)*
- **O3** Use cross-validation to select a model order. *(Analyze — autograded + rubric)*
- **O4** Explain the bias–variance trade-off from your own CV results. *(Evaluate — rubric)*

**3. The task (outcome, not recipe).** Fit polynomial models of orders 1–8 to the Olympic
100m data; scale features to `[0, 1]`. Use cross-validation to select an order and produce
the CV-error-vs-order curve.

**4. What you may and may not use.** Fit by **any correct method** — normal equations,
`np.linalg.lstsq`, `np.polyfit`. Use **any CV implementation** — manual K-fold, LOOCV, or
`sklearn.model_selection.KFold`. **You may not** compute the scaling statistics on the
validation fold (no leakage): the scaler is fit on training data only.

**5. How you'll be assessed (shown up front).**
- *Correctness (autograded, 55%)* — the checks in §2, with thresholds visible in
  `test_hw.py`: scaling is a proper `[0,1]` map; design-matrix shape + intercept column;
  order-1 & order-2 predictions match the closed-form fit to `rel=1e-3`; CV runs and
  returns finite, non-negative per-order losses; CV penalizes over-complex models.
- *Interpretation (rubric, 35%)* — the three prompts in §6, scored on the shared
  Claim/Evidence/Reasoning/Limits rubric (`hw3/rubric.md`).
- *Process (10%)* — seeded (`np.random.default_rng(0)` already provided), runs clean, CV
  plot labeled.

**6. Required interpretation** (markdown cells in `hw.py`, submitted with the code):
- **(i)** Which order did CV select, and *why* — in bias–variance terms?
- **(ii)** What do the CV curve and the train-vs-CV gap show about overfitting?
- **(iii)** Name one situation where CV here could mislead you (e.g., tiny N, leakage,
  non-i.i.d. data).

**7. Going further (optional, ungraded).** Repeat with a different CV scheme (5-fold vs
LOOCV) and comment on the *variance* of the estimate.

**8. Submission & reproducibility.** Keep the provided seed. Implement the function
contract the autograder imports (signatures unchanged except `run_K_fold_cv` now returns
the per-order mean validation losses — see §4 below). Run `pytest test_hw.py` locally
before submitting.

---

## 2. Rewritten `test_hw.py` (outcome/property/convergence; independent partial-credit)

Each test is independent (one bug can't zero the set) and carries an actionable message.
Exact match is kept **only** for the closed-form order-1/2 predictions, with `rel=1e-3`.

```python
"""Tests for hw3 — capability/property checks, not pinned coefficients."""
import numpy as np
from pytest import approx
from hw import PolynomialRegressionModel, scale, run_K_fold_cv

DATA = "data100m.csv"
def _xt():
    return np.loadtxt(DATA, delimiter=",", skiprows=1, unpack=True)

# --- O2: scaling is a proper [0,1] map (property, replaces the one hardcoded case) ---
def test_scale_is_unit_range():
    rng = np.random.default_rng(0)
    a = rng.random(50)
    scaled, lo, span = scale(a)
    assert scaled.min() == approx(0.0) and scaled.max() == approx(1.0), \
        f"scaled range should be [0,1], got [{scaled.min():.3f},{scaled.max():.3f}]"
    assert lo == approx(a.min()), f"min should be {a.min():.4f}, got {lo:.4f}"
    assert span == approx(a.max() - a.min()), f"range should be {a.max()-a.min():.4f}, got {span:.4f}"

def test_scale_is_affine_recoverable():            # invariant: unscale(scale(a)) == a
    a = np.array([3.0, 7.0, 1.0, 9.0])
    scaled, lo, span = scale(a)
    assert scaled * span + lo == approx(a), "scaling must be invertible (affine map)"

# --- O1: design matrix structure (shape + intercept), order-independent on the feature ---
def test_design_matrix_shape_and_intercept():
    x, _ = _xt()
    m = PolynomialRegressionModel(3)
    assert m.get_design_matrix_shape(x) == (len(x), 4), \
        f"order-3 design matrix should be ({len(x)}, 4)"
    X = m.create_design_matrix(x)
    assert X.shape == (len(x), 4)
    assert np.allclose(X[:, 0], 1.0), "first column must be the intercept (all ones)"

# --- O1: closed-form fits are deterministic ⇒ keep exact, with headroom (rel=1e-3) ---
def test_order1_prediction_matches_closed_form():
    x, t = _xt()
    m = PolynomialRegressionModel(1); m.train(x, t)
    assert m.predict(np.array([2012]))[0] == approx(9.594713852048779, rel=1e-3)

def test_order2_prediction_matches_closed_form():
    x, t = _xt()
    m = PolynomialRegressionModel(2); m.train(x, t)
    assert m.predict(np.array([2012]))[0] == approx(9.868303074326368, rel=1e-3)

# --- O1: capability floor — a fitted model actually fits (any method passes) ---
def test_fit_quality_floor():
    x, t = _xt()
    m = PolynomialRegressionModel(3); m.train(x, t)
    rmse = np.sqrt(np.mean((m.predict(x) - t) ** 2))
    assert rmse <= 0.5, f"train RMSE {rmse:.3f}s exceeds 0.5s floor — model isn't fitting"

# --- O3: cross-validation runs and is sane (REQUIRES the §4 return-value change) ---
def test_cv_runs_and_returns_sane_losses():
    losses = run_K_fold_cv(K=5, P=8, data=_stack())
    losses = np.asarray(losses, dtype=float)
    assert losses.shape == (8,), f"expected one mean loss per order 1..8, got shape {losses.shape}"
    assert np.all(np.isfinite(losses)), "CV losses must be finite"
    assert np.all(losses >= 0), "CV (squared-error) losses must be non-negative"

def test_loocv_runs():
    x, _ = _xt()
    losses = np.asarray(run_K_fold_cv(K=len(x), P=8, data=_stack()), dtype=float)
    assert losses.shape == (8,) and np.all(np.isfinite(losses)), "LOOCV (K=N) must run and return finite losses"

# --- O3: CV penalizes over-complex models (the concept, not a specific order/loss) ---
def test_cv_penalizes_overfitting():
    losses = np.asarray(run_K_fold_cv(K=5, P=8, data=_stack()), dtype=float)
    assert np.argmin(losses) < 7, "CV should not select the most complex order (8)"
    assert losses[-1] > losses[np.argmin(losses)], "highest order should be worse under CV"

def _stack():
    x, t = _xt()
    rng = np.random.default_rng(0)
    return rng.permutation(np.column_stack((x, t)))
```

**Coverage honesty (framework §5):** "scaling happens *inside* each fold (no leakage)" and
"this is genuinely K-fold" are partly inspection/rubric items — the autograder checks the
CV *outputs* are sane and that complexity is penalized, not the internal fold mechanics.
That gap is exactly what interpretation prompt (iii) and the leakage rule in §4 cover.

---

## 3. `hw3/rubric.md` (interpretation layer; shared analytic rubric)

Score each of prompts (i)–(iii) on four dimensions, 0–3 (12 max/prompt → normalized to the
35% interpretation weight; specs bundle: "Interpretation = PASS" requires ≥2 on every
dimension of every prompt, else one revise-and-resubmit).

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | names the selected order / the overfitting signal correctly | mostly right, minor gap | partial | missing/wrong |
| **Evidence** | cites the CV-curve minimum and the train-vs-CV gap from *their* plot | cites some numbers | vague | none |
| **Reasoning** | ties it to variance rising with complexity (bias–variance) | sound | superficial | absent/wrong |
| **Limits** | names a real failure mode (tiny N, leakage, non-i.i.d.) | states one weakly | minimal | none |

*Exemplar for (ii):* cites the curve's minimum and the widening train-vs-CV gap (Evidence),
explains it as variance growing with model order (Reasoning), notes the conclusion is
specific to this dataset/sample size (Limits).

---

## 4. Proposed `hw.py` edits (marker-preserving) — the one required contract change

`run_K_fold_cv` must **return** the per-order mean validation losses so O3 is testable
(today it returns `None` and only plots). Minimal change, inside the existing solution
markers; plotting is preserved.

```diff
 def run_K_fold_cv(K: int, P: int, data):
     ...
+    ### SOLUTION START ###
+    mean_val_losses = []           # index p-1 -> mean validation loss for order p
     for p in range(1, P + 1):
         ...
-        # (currently: accumulate losses, plot, return None)
+        mean_val_losses.append(np.mean(fold_val_losses))
     ...
     # (keep the existing plotting of the CV curve)
+    return np.asarray(mean_val_losses)
+    ### SOLUTION END ###
```

No signature change; callers `run_K_fold_cv(5, 8, stack_shuffled)` and
`run_K_fold_cv(x.shape[0], 8, stack_shuffled)` still work. Solution markers and the
`make_release` strip are preserved. (Exact diff finalized against the real loop body when
applied.)

---

## 5. Alignment & effort

| Objective | Assessed by | Type |
|-----------|-------------|------|
| O1 fit polynomial features | `test_order1/2_*`, `test_fit_quality_floor`, design-matrix test | autograded |
| O2 scale without leakage | `test_scale_*` (property) + rubric (iii) for leakage | autograded + rubric |
| O3 select order via CV | `test_cv_*` (sane, penalizes overfitting) + rubric (i) | autograded + rubric |
| O4 explain bias–variance | rubric (i),(ii) | rubric |

**Unmeasurable-by-autograder, flagged:** no-leakage and "is it truly K-fold" → covered by
the §4 rule + rubric (iii). **Effort:** roughly unchanged (~6–8h); the new work is writing
three short paragraphs, offset by deleting the two vague ungraded questions. Stays within
5–6 hrs/week.
