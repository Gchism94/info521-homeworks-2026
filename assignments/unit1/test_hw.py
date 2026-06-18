"""Unit 1 autograder — merged outcome/property/floor-AND-guard suite (hw1 + hw2 + hw3).

Each test is one Correctness specification (see specs.md). Closed-form scalars keep exact
checks with rel headroom; everything else is a property/convergence check so any sound
method passes. The order-1 fit value (9.5947) is the Olympic-100m through-line: scalar,
matrix, and polynomial-order-1 must all agree.
"""

import numpy as np
from pytest import approx
from hw import (
    SimpleLinearModel,
    PolynomialRegressionModel,
    scale,
    run_K_fold_cv,
    load_data,
)

PRED_2012 = 9.594713852048779  # through-line: hw1 == hw2(order 1) == hw3(order 1)


def _xt():
    return load_data()


def _stack():
    x, t = _xt()
    return np.random.default_rng(0).permutation(np.column_stack((x, t)))


# ---------- Part A: scalar least squares ----------
def test_scalar_closed_form():
    x, t = _xt()
    m = SimpleLinearModel(); m.train(x, t)
    assert m.w0 == approx(36.41645590250286, rel=1e-3)
    assert m.w1 == approx(-0.013330885710960602, rel=1e-3)


def test_scalar_normal_equations():
    x, t = _xt()
    m = SimpleLinearModel(); m.train(x, t)
    r = t - m.predict(x)
    assert np.sum(r) == approx(0.0, abs=1e-6)
    assert np.dot(r, x) == approx(0.0, abs=1e-4)


def test_scalar_beats_baseline():
    """FLOOR+GUARD: the fitted line beats the constant-mean predictor by a margin."""
    x, t = _xt()
    m = SimpleLinearModel(); m.train(x, t)
    assert np.mean((t - m.predict(x)) ** 2) <= 0.5 * np.mean((t - t.mean()) ** 2)


# ---------- Part B: matrix normal equation (order-1 polynomial == scalar) ----------
def test_matrix_order1_matches_scalar():
    """The matrix fit (PolynomialRegressionModel order 1) reproduces the scalar fit."""
    x, t = _xt()
    s = SimpleLinearModel(); s.train(x, t)
    m = PolynomialRegressionModel(1); m.train(x, t)
    xq = np.array([1900.0, 2012.0])
    assert m.predict(xq) == approx(s.predict(xq), rel=1e-6)
    assert m.predict(np.array([2012.0]))[0] == approx(PRED_2012, rel=1e-3)


def test_matrix_normal_equations():
    """Residuals orthogonal to every column of the design matrix."""
    x, t = _xt()
    m = PolynomialRegressionModel(1); m.train(x, t)
    X = m.create_design_matrix(x)
    assert np.allclose(X.T @ (t - m.predict(x)), 0.0, atol=1e-4)


# ---------- Part C: polynomial features, scaling, cross-validation ----------
def test_scale_is_unit_range():
    a = np.random.default_rng(0).random(50)
    scaled, lo, span = scale(a)
    assert scaled.min() == approx(0.0) and scaled.max() == approx(1.0)
    assert lo == approx(a.min()) and span == approx(a.max() - a.min())


def test_scale_is_affine_recoverable():
    a = np.array([3.0, 7.0, 1.0, 9.0])
    scaled, lo, span = scale(a)
    assert scaled * span + lo == approx(a)


def test_design_matrix_shape_and_intercept():
    x, _ = _xt()
    m = PolynomialRegressionModel(3)
    assert m.get_design_matrix_shape(x) == (len(x), 4)
    X = m.create_design_matrix(x)
    assert X.shape == (len(x), 4)
    assert np.allclose(X[:, 0], 1.0)


def test_fit_quality_floor_scaled():
    """Capability floor: a fitted order-3 model actually fits (scaled), any method."""
    x, t = _xt()
    xs, _, _ = scale(x); ts, _, _ = scale(t)
    m = PolynomialRegressionModel(3); m.train(xs, ts)
    rmse = float(np.sqrt(np.mean((m.predict(xs) - ts) ** 2)))
    assert rmse <= 0.3


def test_cv_returns_per_order_losses():
    losses = np.asarray(run_K_fold_cv(5, 8, _stack()), dtype=float)
    assert losses.shape == (8,)
    assert np.all(np.isfinite(losses)) and np.all(losses >= 0)


def test_loocv_runs():
    x, _ = _xt()
    losses = np.asarray(run_K_fold_cv(len(x), 8, _stack()), dtype=float)
    assert losses.shape == (8,) and np.all(np.isfinite(losses))


def test_cv_penalizes_overfitting():
    """FLOOR+GUARD: CV does not pick the most complex order; the highest order scores worse."""
    losses = np.asarray(run_K_fold_cv(5, 8, _stack()), dtype=float)
    assert np.argmin(losses) < 7
    assert losses[-1] > losses[np.argmin(losses)]
