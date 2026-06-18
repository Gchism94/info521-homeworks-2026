# %% [markdown]
"""
# Unit 1 — Linear models & model selection (Olympic 100m)

Importable reference module for the Unit 1 autograder. Three ways to fit the same
Olympic-100m data, deepening: scalar least squares (Part A) -> matrix normal equation
(Part B) -> polynomial features + cross-validation (Part C).

All drivers are guarded / factored into functions, so `import hw` is cheap and writes
nothing. Fill the `### YOUR CODE HERE ###` markers.
"""

import numpy as np

DATA = "data100m.csv"


def load_data(path: str = DATA):
    """Load the Olympic 100m data as (x, t) = (year, winning time)."""
    return np.loadtxt(path, delimiter=",", skiprows=1, unpack=True)


# ===== Part A — scalar least squares (the 1-D normal equations) =====
class SimpleLinearModel:
    """1-D least squares with two parameters, by the closed-form normal equations."""

    def __init__(self):
        self.w0: float = None
        self.w1: float = None

    def train(self, x, t):
        xbar = x.mean()
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        tbar = t.mean()
        xxbar = np.multiply(x, x).mean()
        xtbar = np.multiply(x, t).mean()
        self.w1 = (xtbar - xbar * tbar) / (xxbar - xbar ** 2)
        self.w0 = tbar - self.w1 * xbar
        ### SOLUTION END ###

    def predict(self, x):
        return self.w0 + self.w1 * x


# ===== Part C — polynomial regression (matrix normal equation, any order) =====
# PolynomialRegressionModel(1) IS Part B's matrix linear fit (order-1 design matrix
# [1, x]); higher orders add columns x**k. The matrix normal equation it solves is
# w = (X^T X)^{-1} X^T t, obtained by setting the gradient of the squared-error loss to
# zero using the matrix-calculus identities APPLIED here and DERIVED GENERALLY in U2b (hw7).
class PolynomialRegressionModel:
    """Polynomial regression by the matrix normal equation."""

    def __init__(self, order: int):
        self.order = order
        self.w = None

    def get_design_matrix_shape(self, x):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        return (x.shape[0], self.order + 1)
        ### SOLUTION END ###
        ...  # placeholder: keeps the stripped student template valid

    @staticmethod
    def initialize_design_matrix(shape):
        return np.zeros(shape)

    def fill_design_matrix(self, X, x):
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        for k in range(self.order + 1):
            X[:, k] = x ** k
        ### SOLUTION END ###
        ...  # placeholder: keeps the stripped student template valid

    def create_design_matrix(self, x):
        X = self.initialize_design_matrix(self.get_design_matrix_shape(x))
        self.fill_design_matrix(X, x)
        return X

    def compute_mse_loss(self, x, t):
        error = self.predict(x) - t
        return (error.T @ error) / error.shape[0]

    def train(self, x, t):
        X = self.create_design_matrix(x)
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        self.w = np.linalg.solve(X.T @ X, X.T @ t)   # solve, not inv (stable; cf. U2b)
        ### SOLUTION END ###

    def predict(self, x):
        if self.w is None:
            raise ValueError("Model not trained yet.")
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        return self.create_design_matrix(x) @ self.w
        ### SOLUTION END ###


def scale(array):
    """Linearly scale `array` to [0, 1]; return (scaled, min, range) for inversion."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    array_min = np.min(array)
    array_range = np.max(array) - array_min
    scaled_array = (array - array_min) / array_range
    ### SOLUTION END ###
    return scaled_array, array_min, array_range


def run_K_fold_cv(K: int, P: int, data):
    """K-fold CV over polynomial orders 1..P. Returns a length-P array; element p-1 is
    the mean validation MSE for order p. (Scales each fold AFTER splitting -- no leakage.)
    Pure: returns losses, writes/plots nothing (the notebook plots separately)."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    folds = np.array_split(data, K)
    mean_validation_losses = np.zeros(P)
    for p in range(1, P + 1):
        model = PolynomialRegressionModel(p)
        order_losses = np.zeros(K)
        for k in range(K):
            train = np.concatenate([folds[i] for i in range(K) if i != k])
            val = folds[k]
            xs, xmin, xrng = scale(train[:, 0])
            ts, tmin, trng = scale(train[:, 1])
            model.train(xs, ts)
            xvs = (val[:, 0] - xmin) / xrng
            tvs = (val[:, 1] - tmin) / trng
            order_losses[k] = model.compute_mse_loss(xvs, tvs)
        mean_validation_losses[p - 1] = order_losses.mean()
    return mean_validation_losses
    ### SOLUTION END ###
    ...  # placeholder: keeps the stripped student template valid
