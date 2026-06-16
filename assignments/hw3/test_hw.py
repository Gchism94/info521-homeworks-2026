"""Tests for HW3 (overhauled) — capability/property checks, not pinned coefficients.

Each test is an independent Correctness spec (partial credit) with an actionable message.
Exact match is kept only for the closed-form order-1/2 predictions, with rel=1e-3 headroom.
"""

import numpy as np
from pytest import approx
from hw import PolynomialRegressionModel, scale, run_K_fold_cv

DATA = "data100m.csv"


def _xt():
    return np.loadtxt(DATA, delimiter=",", skiprows=1, unpack=True)


def _stack():
    x, t = _xt()
    return np.random.default_rng(0).permutation(np.column_stack((x, t)))


# --- O2: scaling is a proper [0, 1] map (property; replaces the single hardcoded case) ---
def test_scale_is_unit_range():
    a = np.random.default_rng(0).random(50)
    scaled, lo, span = scale(a)
    assert scaled.min() == approx(0.0) and scaled.max() == approx(1.0), (
        f"scaled range should be [0,1], got [{scaled.min():.3f}, {scaled.max():.3f}]"
    )
    assert lo == approx(a.min()), f"min should be {a.min():.4f}, got {lo:.4f}"
    assert span == approx(a.max() - a.min()), (
        f"range should be {a.max() - a.min():.4f}, got {span:.4f}"
    )


def test_scale_is_affine_recoverable():
    a = np.array([3.0, 7.0, 1.0, 9.0])
    scaled, lo, span = scale(a)
    assert scaled * span + lo == approx(a), "scaling must be invertible (affine map)"


# --- O1: design matrix has the right shape and an intercept column ---
def test_design_matrix_shape_and_intercept():
    x, _ = _xt()
    m = PolynomialRegressionModel(3)
    assert m.get_design_matrix_shape(x) == (len(x), 4), (
        f"order-3 design matrix should be ({len(x)}, 4)"
    )
    X = m.create_design_matrix(x)
    assert X.shape == (len(x), 4)
    assert np.allclose(X[:, 0], 1.0), "first column must be the intercept (all ones)"


# --- O1: closed-form fits are deterministic -> keep exact, with rel=1e-3 headroom ---
def test_order1_prediction_matches_closed_form():
    x, t = _xt()
    m = PolynomialRegressionModel(1)
    m.train(x, t)
    assert m.predict(np.array([2012]))[0] == approx(9.594713852048779, rel=1e-3)


def test_order2_prediction_matches_closed_form():
    x, t = _xt()
    m = PolynomialRegressionModel(2)
    m.train(x, t)
    assert m.predict(np.array([2012]))[0] == approx(9.868303074326368, rel=1e-3)


# --- O1: capability floor — a fitted model actually fits (scaled; any method passes) ---
def test_fit_quality_floor_scaled():
    x, t = _xt()
    xs, _, _ = scale(x)
    ts, _, _ = scale(t)
    m = PolynomialRegressionModel(3)
    m.train(xs, ts)
    rmse = float(np.sqrt(np.mean((m.predict(xs) - ts) ** 2)))
    assert rmse <= 0.3, f"scaled train RMSE {rmse:.3f} too high — model isn't fitting"


# --- O3: cross-validation output contract + sanity (uses the documented return) ---
def test_cv_returns_per_order_losses():
    losses = np.asarray(run_K_fold_cv(5, 8, _stack()), dtype=float)
    assert losses.shape == (8,), (
        f"run_K_fold_cv must return one mean loss per order 1..8; got shape {losses.shape}"
    )
    assert np.all(np.isfinite(losses)), "CV losses must be finite"
    assert np.all(losses >= 0), "squared-error CV losses must be non-negative"


def test_loocv_runs():
    x, _ = _xt()
    losses = np.asarray(run_K_fold_cv(len(x), 8, _stack()), dtype=float)
    assert losses.shape == (8,) and np.all(np.isfinite(losses)), (
        "LOOCV (K=N) must run and return finite per-order losses"
    )


# --- O3: CV penalizes over-complex models (the concept, not a specific order/loss) ---
def test_cv_penalizes_overfitting():
    losses = np.asarray(run_K_fold_cv(5, 8, _stack()), dtype=float)
    assert np.argmin(losses) < 7, (
        f"CV should not select the most complex order (8); argmin={np.argmin(losses)}"
    )
    assert losses[-1] > losses[np.argmin(losses)], (
        "the highest order should score worse under CV than the selected order"
    )
