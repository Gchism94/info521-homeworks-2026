"""Capstone — open Bayesian modelling with uncertainty.

You choose a model and a Bayesian uncertainty method (a Unit-4/5 approach: conjugate/Laplace/
MCMC). The autograder checks METHOD VALIDITY, INTERNAL CONSISTENCY, and that your code RUNS --
there is no pinned 'right answer'. The contract below is the minimum your submission must expose;
implement it however you like.

Reference (ONE valid approach, inside the SOLUTION markers): Bayesian linear regression with
polynomial features and a Gaussian prior -- closed-form posterior + predictive variance.
"""
import numpy as np


def load_data(path="data/capstone.csv"):
    d = np.loadtxt(path, delimiter=",", skiprows=1)
    return d[:, 0], d[:, 1]


class BayesianModel:
    """Contract: fit(x,t) -> self ; predict(x) -> mean ; predictive_std(x) -> std ;
    posterior_cov() -> parameter posterior covariance (PSD)."""

    def __init__(self, order=4, prior_precision=1.0, noise_precision=25.0):
        self.order = order
        self.alpha = prior_precision      # Gaussian prior precision on the weights
        self.beta = noise_precision       # noise precision (1 / noise variance)

    def _design(self, x):
        return np.vander(np.asarray(x).ravel(), self.order + 1, increasing=True)

    def fit(self, x, t):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        X = self._design(x)
        self.cov = np.linalg.inv(self.alpha * np.eye(X.shape[1]) + self.beta * X.T @ X)
        self.mean = self.beta * self.cov @ X.T @ np.asarray(t).ravel()
        ### SOLUTION END ###
        return self

    def predict(self, x):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        return self._design(x) @ self.mean
        ### SOLUTION END ###
        ...

    def predictive_std(self, x):
        """Predictive standard deviation = sqrt(1/beta + x^T cov x)."""
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        X = self._design(x)
        var = 1.0 / self.beta + np.sum((X @ self.cov) * X, axis=1)
        return np.sqrt(var)
        ### SOLUTION END ###
        ...

    def posterior_cov(self):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        return self.cov
        ### SOLUTION END ###
        ...
