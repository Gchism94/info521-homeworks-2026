"""Capstone autograder — METHOD VALIDITY + INTERNAL CONSISTENCY + RUNNABLE (no pinned answer).

Every check passes for ANY sound Bayesian-uncertainty approach on the provided data; none
checks a specific numeric result (the task is open).
"""
import numpy as np
from hw import BayesianModel, load_data

X, T = load_data()


def _fit():
    return BayesianModel().fit(X, T)


def test_runs_and_shapes():
    """RUNNABLE: fit/predict/predictive_std run and return finite, correctly-shaped output."""
    m = _fit()
    xq = np.linspace(-3, 3, 25)
    p, s = m.predict(xq), m.predictive_std(xq)
    assert p.shape == (25,) and s.shape == (25,)
    assert np.all(np.isfinite(p)) and np.all(np.isfinite(s))

def test_model_fits_beats_baseline():
    """METHOD VALIDITY (floor): the fit beats the constant-mean predictor on the data."""
    m = _fit()
    rmse = np.sqrt(np.mean((m.predict(X) - T) ** 2))
    assert rmse <= 0.7 * np.std(T)

def test_uncertainty_nonneg_and_cov_psd():
    """METHOD VALIDITY: predictive std >= 0 and the parameter posterior covariance is symmetric PSD."""
    m = _fit()
    assert np.all(m.predictive_std(np.linspace(-3, 3, 40)) >= 0)
    cov = np.asarray(m.posterior_cov())
    assert np.allclose(cov, cov.T)
    assert np.all(np.linalg.eigvalsh(cov) >= -1e-8)

def test_uncertainty_grows_off_data():
    """INTERNAL CONSISTENCY: predictive std grows under EXTRAPOLATION vs the dense-data region --
    the robust property every valid Bayesian method that propagates parameter uncertainty shares.
    (Gap behaviour is method-dependent -- e.g. a smooth model may interpolate a narrow gap
    confidently -- so it is an Interpretation item, NOT a floor; computed here only as a diagnostic.)"""
    m = _fit()
    s_dense = m.predictive_std(np.array([-1.5]))[0]    # region with data
    s_extrap = m.predictive_std(np.array([4.5]))[0]    # beyond the data
    s_gap = m.predictive_std(np.array([1.25]))[0]      # centre of the [0.5, 2.0] gap -- DIAGNOSTIC ONLY
    print(f"[C1 diagnostic] s_dense={s_dense:.4f}  s_gap={s_gap:.4f}  s_extrap={s_extrap:.4f}")
    assert s_extrap > s_dense

def test_predictive_std_exceeds_noise_floor():
    """INTERNAL CONSISTENCY: predictive uncertainty is never below the model's own noise scale
    (predictive var = noise var + parameter var >= noise var)."""
    m = _fit()
    assert np.all(m.predictive_std(np.linspace(-3, 3, 30)) >= np.sqrt(1.0 / m.beta) - 1e-9)
