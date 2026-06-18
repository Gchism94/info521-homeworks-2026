"""Unit 4 — Bayesian inference, exact & conjugate.

Predictive variance / error bars (hw10), the exact Beta-Binomial coin-game posterior (hw11,
conjugacy), and the Inverse-Gamma conjugate prior on the regression noise variance (hw12,
written). `import hw` is cheap.
"""
import numpy as np
from scipy.special import gamma, loggamma, binom


# ===== Part A — Predictive variance (error bars) =====
def true_function(x):
    return 0.5 * x ** 3 - 3 * x ** 2 - 2 * x + 5


def sample_dataset(x, noise_variance, rng):
    return true_function(x) + rng.normal(0, np.sqrt(noise_variance), x.shape)


def generate_synthetic_data(rng, N, x_min, x_max, noise_variance, gap_min, gap_max):
    x = np.sort(rng.uniform(x_min, x_max, N))
    t = sample_dataset(x, noise_variance, rng)
    pos = ((x > gap_min) * (x < gap_max)).nonzero()[0]
    return np.delete(x, pos)[:, None], np.delete(t, pos)[:, None]


class PolynomialRegressionModel:
    """Polynomial regression with the MLE noise variance + predictive variance."""

    def __init__(self, order, x, t):
        self.order = order
        x = x.squeeze(); t = t.squeeze()
        self.X_train = self.get_design_matrix(x)
        self.w, self.sigma_sq = self.train(t)

    def get_design_matrix(self, x):
        X = np.zeros((x.shape[0], self.order + 1))
        x = x.reshape((x.shape[0], 1))
        for k in range(self.order + 1):
            X[:, k:k + 1] = x ** k
        return X

    def compute_cov_w(self):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        return self.sigma_sq * np.linalg.inv(self.X_train.T @ self.X_train)
        ### SOLUTION END ###
        ...  # placeholder

    def train(self, t):
        X = self.X_train
        w = np.linalg.inv(X.T @ X) @ X.T @ t
        sigma_sq = (1 / X.shape[0]) * (t.T @ t - t.T @ X @ w)   # MLE: divide by n_train
        return w, sigma_sq

    def predict(self, x):
        return self.get_design_matrix(x) @ self.w

    def predictive_variance(self, x_new):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        X_test = self.get_design_matrix(x_new); X = self.X_train
        n = X_test.shape[0]; variance = np.zeros(n)
        for k in range(n):
            variance[k] = self.sigma_sq * (X_test[k].T @ np.linalg.inv(X.T @ X) @ X_test[k])
        return variance
        ### SOLUTION END ###
        ...  # placeholder


# ===== Part B — Exact Beta-Binomial inference (the coin game) =====
def B(a, b):
    """Beta function  B(a,b) = Gamma(a)Gamma(b)/Gamma(a+b)."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return (gamma(a) * gamma(b)) / gamma(a + b)
    ### SOLUTION END ###
    ...  # placeholder


def Beta(r, a, b):
    """Beta(r | a, b) density."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return (1 / B(a, b)) * np.power(r, a - 1) * np.power(1 - r, b - 1)
    ### SOLUTION END ###
    ...  # placeholder


def posterior(r, N, y_N, a, b):
    """Posterior over r: conjugacy ⇒ Beta(r | a + y_N, b + N - y_N)."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return Beta(r, a + y_N, b + N - y_N)
    ### SOLUTION END ###
    ...  # placeholder


def calculate_marginal_likelihood(N, y_N, a, b):
    """Marginal likelihood (computed in log-space for stability)."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    log_ml = (np.log(binom(N, y_N)) + loggamma(a + b) - loggamma(a) - loggamma(b)
              + loggamma(a + y_N) + loggamma(b + N - y_N) - loggamma(a + b + N))
    return np.exp(log_ml)
    ### SOLUTION END ###
    ...  # placeholder


def calculate_probability_of_winning(N, y_N, a, b):
    """P(win) = P(<= 6 heads in the next 10) under the posterior predictive."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    ap, bp = a + y_N, b + N - y_N
    def pp(y_new):
        log_e = (np.log(binom(10, y_new)) + loggamma(ap + bp) - loggamma(ap) - loggamma(bp)
                 + loggamma(ap + y_new) + loggamma(bp + 10 - y_new) - loggamma(ap + bp + 10))
        return np.exp(log_e)
    return 1 - sum(pp(y) for y in range(7, 11))
    ### SOLUTION END ###
    ...  # placeholder
