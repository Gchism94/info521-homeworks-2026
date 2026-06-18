"""Unit 5 — Approximate Bayesian inference: four ways to one posterior.

The same Bayesian logistic-regression posterior (FCML binary-classification data, Gaussian
prior on w) recovered four ways: the graphical model (written), the MAP via Newton-Raphson,
the Laplace approximation, and Metropolis-Hastings MCMC. All share `data/X.csv`,`data/t.csv`.

Fill the `### YOUR CODE HERE ###` markers. `import hw` is cheap (no work at import).
"""

import numpy as np

SIG_SQ = 10  # Gaussian prior variance on w  (the sigma^2 -> w edge of the PGM)


def load_data():
    return np.loadtxt("data/X.csv", delimiter=","), np.loadtxt("data/t.csv")


# ===== Logistic + log-posterior gradient/Hessian (shared by MAP & Laplace) =====
def logistic(x):
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return 1.0 / (1.0 + np.exp(-x))
    ### SOLUTION END ###
    ...  # placeholder


def gradient(w, X, t, sig_sq=SIG_SQ):
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    p = logistic(X @ w).flatten()
    ### SOLUTION END ###
    return -w / sig_sq + X.T @ (t - p)


def hessian(w, X, sig_sq=SIG_SQ):
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    p = logistic(X @ w).flatten()
    ### SOLUTION END ###
    W = np.diag(p * (1 - p))
    return -(1.0 / sig_sq) * np.eye(len(w)) - X.T @ W @ X


# ===== Way 2 — MAP via Newton-Raphson =====
def newton_map(X, t, sig_sq=SIG_SQ, iters=10):
    """Return w_MAP by `iters` Newton-Raphson steps from w=0 (driver; uses your grad/Hessian)."""
    w = np.zeros(X.shape[1])
    for _ in range(iters):
        w = w - np.linalg.inv(hessian(w, X, sig_sq)) @ gradient(w, X, t, sig_sq)
    return w


# ===== Way 3 — Laplace approximation (Gaussian at the MAP) =====
def laplace_covariance(w_map, X, sig_sq=SIG_SQ):
    """Laplace covariance = inverse of the negative Hessian at the MAP."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return np.linalg.inv(-hessian(w_map, X, sig_sq))
    ### SOLUTION END ###
    ...  # placeholder


# ===== Way 4 — Metropolis-Hastings MCMC =====
class MetropolisSampler:
    """Metropolis sampler for the Bayesian-logistic-regression posterior over w."""

    def __init__(self, X, t, proposal_variance, prior_variance, seed=100):
        self.X, self.t = X, t
        self.proposal_variance = proposal_variance
        self.prior_variance = prior_variance
        self.proposal_cov = np.eye(X.shape[1]) * proposal_variance
        self.rng = np.random.default_rng(seed=seed)

    def log_likelihood(self, w):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        P = np.clip(logistic(self.X @ w), 1e-12, 1 - 1e-12)   # clip for numerical stability
        return (self.t @ np.log(P) + (1 - self.t) @ np.log(1 - P)).sum()
        ### SOLUTION END ###
        ...  # placeholder

    def log_prior(self, w):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        return -(1.0 / (2.0 * self.prior_variance)) * (w.T @ w)
        ### SOLUTION END ###
        ...  # placeholder

    def sample_from_proposal(self, w):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        return self.rng.multivariate_normal(w, cov=self.proposal_cov)
        ### SOLUTION END ###
        ...  # placeholder

    def compute_acceptance_ratio(self, w, w_candidate):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        log_r = (self.log_prior(w_candidate) + self.log_likelihood(w_candidate)
                 - self.log_prior(w) - self.log_likelihood(w))
        return np.exp(log_r)
        ### SOLUTION END ###
        ...  # placeholder

    def generate_sample(self, w):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        w_candidate = self.sample_from_proposal(w)
        r = self.compute_acceptance_ratio(w, w_candidate)
        return w_candidate if self.rng.uniform(0, 1) <= r else w
        ### SOLUTION END ###
        ...  # placeholder

    def generate_samples(self, num_samples):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        current = np.array([0.0, 0.0])
        samples = []
        for _ in range(num_samples):
            current = self.generate_sample(current)
            samples.append(current)
        return samples
        ### SOLUTION END ###
        ...  # placeholder
