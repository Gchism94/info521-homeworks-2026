"""Unit 4 autograder — predictive-variance (hw10) + coin-game conjugacy (hw11) specs.

Closed-form/relationship checks (no brittle 100-element array pins). The Inverse-Gamma
conjugacy derivation (hw12) is a written, human-graded spec (specs.md).
"""
import numpy as np
from pytest import approx
from scipy.special import gamma as _g
from hw import (PolynomialRegressionModel, generate_synthetic_data, sample_dataset,
                B, Beta, posterior, calculate_marginal_likelihood,
                calculate_probability_of_winning)


def _model(order=2):
    rng = np.random.default_rng(0)
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]); t = sample_dataset(x, 6, rng)
    return PolynomialRegressionModel(order, x, t)


# Reference values for the order-2 `_model()` on its seeded data, computed at authoring time
# from the reference solution (deterministic under the numpy 2.1.x RNG/ABI pin). Pinned as
# VALUES so the autograder checks correctness WITHOUT spelling out the expressions students
# derive:  cov_w = sigma^2 (XtX)^-1   and   predictive_variance = diag(X cov_w X^T).
COV_W_REF = np.array([[16.06301404, -9.78839918,  1.25492297],
                      [-9.78839918,  6.87518514, -0.94119223],
                      [ 1.25492297, -0.94119223,  0.13445603]])
PRED_VAR_REF = np.array([8.39397807, 2.14177255, 1.86445699])   # predictive var at x = [0.5, 1.5, 4.0]


# ---------- Part A: predictive variance ----------
def test_cov_w_definition_psd():
    """A1: parameter covariance has the correct VALUE (pinned reference) and is symmetric PSD
    -- checks the value, not the sigma^2 (XtX)^-1 expression."""
    cov = _model().compute_cov_w()
    assert cov == approx(COV_W_REF, rel=1e-6)
    assert cov == approx(cov.T) and np.all(np.linalg.eigvalsh(cov) >= -1e-10)

def test_predictive_variance_matches_cov_w():
    """A2: predictive variance has the correct VALUE (pinned reference) and is nonnegative
    -- checks the value, not the diag(X cov_w X^T) expression."""
    m = _model()
    assert m.predictive_variance(np.array([0.5, 1.5, 4.0])) == approx(PRED_VAR_REF, rel=1e-6)
    assert np.all(m.predictive_variance(np.linspace(-2, 7, 20)) >= 0)

def test_variance_larger_in_gap():
    """FLOOR-AND-GUARD: predictive variance is larger in the data gap than where data is dense."""
    rng = np.random.default_rng(0)
    x, t = generate_synthetic_data(rng, 40, -2, 7, 6, 2.5, 4.5)
    m = PolynomialRegressionModel(3, x, t)
    assert m.predictive_variance(np.array([3.5]))[0] > m.predictive_variance(np.array([0.0]))[0]


# ---------- Part B: Beta-Binomial conjugacy (the coin game) ----------
def test_B_function():
    assert B(2, 3) == approx(_g(2) * _g(3) / _g(5))

def test_beta_normalizes():
    r = np.linspace(0, 1, 100001)
    assert np.trapezoid(Beta(r, 2, 5), r) == approx(1.0, abs=1e-3)

def test_posterior_is_conjugate_beta():
    """The defining identity: posterior(r) == Beta(r | a+y_N, b+N-y_N) (replaces the array pins)."""
    r = np.linspace(0.01, 0.99, 50)
    assert posterior(r, 20, 13, 2.0, 3.0) == approx(Beta(r, 2.0 + 13, 3.0 + 20 - 13))

def test_posterior_mean_is_conjugate():
    """Beta posterior mean = (a+y_N)/(a+b+N) (pseudo-counts; ties to U2b Beta moments)."""
    r = np.linspace(0, 1, 200001)
    post = posterior(r, 20, 13, 2.0, 3.0)
    mean = np.trapezoid(r * post, r)
    assert mean == approx((2 + 13) / (2 + 3 + 20), abs=1e-3)

def test_marginal_likelihood_and_prob_win_are_probabilities():
    ml = calculate_marginal_likelihood(20, 13, 2.0, 3.0)
    pw = calculate_probability_of_winning(20, 13, 2.0, 3.0)
    assert 0.0 < ml < 1.0
    assert 0.0 <= pw <= 1.0
