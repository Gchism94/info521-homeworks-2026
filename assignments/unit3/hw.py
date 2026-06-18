"""Unit 3 — Monte Carlo & estimators.

Estimating expectations and constants by sampling: E[f(X)] for X~U(-1,9) (analytic vs
Monte Carlo), and pi by rejection sampling in 2-D / 3-D / n-D (the curse of dimensionality).
All stochastic functions take a seeded RNG; `import hw` is cheap.
"""
import math
import numpy as np

RNG = np.random.default_rng(521)


# ===== Part A — Monte Carlo expectation (X ~ U(-1, 9)) =====
def f(x):
    """f(x) = 35 + 3x - 3x^2 + 0.2x^3 + 0.01x^4."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return 35 + 3 * x - 3 * x ** 2 + 0.2 * x ** 3 + 0.01 * x ** 4
    ### SOLUTION END ###
    ...  # placeholder


def monte_carlo_expectation(n_samples, rng=None):
    """Monte Carlo estimate of E[f(X)] for X ~ Uniform(-1, 9): mean of f over n samples."""
    rng = rng or RNG
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return float(np.mean(f(rng.uniform(-1, 9, n_samples))))
    ### SOLUTION END ###
    ...  # placeholder


def running_expectation(n_samples, rng=None):
    """Running-mean sequence of the estimate as samples accumulate (for the convergence plot)."""
    rng = rng or RNG
    vals = f(rng.uniform(-1, 9, n_samples))
    return np.cumsum(vals) / np.arange(1, n_samples + 1)


# ===== Part B — Estimating pi by rejection sampling =====
def estimate_pi_using_circle(n_samples, rng=None):
    """2-D: pi ~ 4 * (fraction of [0,1]^2 points inside the unit circle)."""
    rng = rng or RNG
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    s = rng.uniform(0, 1, (2, n_samples))
    return 4 * (np.sum(s[0] ** 2 + s[1] ** 2 < 1) / n_samples)
    ### SOLUTION END ###
    ...  # placeholder


def estimate_pi_using_sphere(n_samples, rng=None):
    """3-D: pi ~ 6 * (fraction of [0,1]^3 points inside the unit sphere)."""
    rng = rng or RNG
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    s = rng.uniform(0, 1, (3, n_samples))
    return 6 * (np.sum(np.sum(s ** 2, axis=0) < 1) / n_samples)
    ### SOLUTION END ###
    ...  # placeholder


def number_of_orthants(n):
    """Number of orthants of an n-ball = 2^n."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return 2 ** n
    ### SOLUTION END ###
    ...  # placeholder


def estimate_pi_using_n_ball(n, n_samples, rng=None):
    """n-D: running pi estimates from V_o; pi = (2^n * V_o * Gamma(n/2+1))^(2/n).
    Returns a length n_samples-1 list (estimate after each successive sample)."""
    rng = rng or RNG
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    samples = rng.uniform(0, 1, (n, n_samples))
    out = []
    for k in range(1, n_samples):
        ss = samples[:, :k]
        V_o = np.sum(np.sum(ss ** 2, axis=0) < 1) / k
        out.append((number_of_orthants(n) * V_o * math.gamma(n * 0.5 + 1)) ** (2 / n))
    return out
    ### SOLUTION END ###
    ...  # placeholder
