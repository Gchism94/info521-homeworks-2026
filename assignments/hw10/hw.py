# %% [markdown]
# # Predictive variance
#
# _(Adapted from materials developed by Simon Rogers and Clay Morrison)_
#
# In this example, we study properties of predictive variance using a synthetic data example. Recall that, for maximum likelihood estimators
#
# $$
# \widehat{\mathbf{w}} = \left(\mathbf{X}^\intercal\mathbf{X}\right)^{-1}\mathbf{X}^\intercal\mathbf{t}$$
#
# $$\widehat{\sigma^2} = \frac{1}{N}\left(\mathbf{t} - \mathbf{X}\widehat{\mathbf{w}}\right)^\intercal\left(\mathbf{t} - \mathbf{X}\widehat{\mathbf{w}}\right)
# $$
#
# we have mean prediction:
#
# $$ t_\text{new} = \widehat{\mathbf{w}}^\intercal\mathbf{x}_\text{new}$$
#
# and variance:
#
# $$ \mbox{var}\{t_\text{new}\} = \widehat{\sigma^2}\mathbf{x}_\text{new}^\intercal\left(\mathbf{X}^\intercal\mathbf{X}\right)^{-1}\mathbf{x}_\text{new}$$
#
# We'll start by generating some synthetic data from a third order polynomial, and then removing a portion of the data to see how that affects predictive variance.
#
# The function we'll use is the one below:
#
# $$f(x) = 0.5x^3 - 3x^2 - 2x + 5$$
#
# And we will set the true noise variance ($\sigma^2$) to 6.
#
# Fill in the missing pieces of code at the markers that say 
#
# `### YOUR CODE HERE ###`

# %%
import numpy as np


def true_function(x):
    return 0.5 * (x**3) - 3 * (x**2) - 2 * x + 5


def sample_dataset(x, noise_variance, rng):
    """
    Sample a set of outputs for a function a given a set of inputs,
    noise_variance, and a random number generator.

    Args:
        x: Vector of inputs
        noise_variance: Noise variance for data generation
        rng: NumPy random Generator instance

    Returns:
        Vector of outputs
    """
    # Add Gaussian noise using numpy.random.Generator.normal
    # https://numpy.org/doc/2.2/reference/random/generated/numpy.random.Generator.normal.html
    epsilon = rng.normal(0, np.sqrt(noise_variance), x.shape)
    t = true_function(x) + epsilon
    return t


def generate_synthetic_data(
    rng, N, x_min, x_max, noise_variance, gap_min, gap_max
):
    """Generate synthetic data, excluding points in a given range.

    Args:
        rng: Instance of NumPy random.Generator (https://numpy.org/doc/stable/reference/random/generator.html)
        N: Number of initial datapoints to generate (prior to excluding data points in a given range)
        x_min: Minimum value of x
        x_max: Maximum value of x
        noise_variance: Noise variance for our data generation process (polynomial model with Gaussian additive noise.
        gap_min: Lower bound of region of x values to exclude
        gap_max: Upper bound of region of x values to exclude

    Returns:
        x: Vector of inputs uniformly sampled between x_min and x_max, excluding points between gap_min and gap_max.
        t: Vector of outputs sampled using the inputs `x`
    """
    # Sample N values of x from U(x_min, x_max)
    x = np.sort(rng.uniform(x_min, x_max, N))

    # Compute values of t using the array of x values.
    t = sample_dataset(x, noise_variance, rng)

    # Remove data points with x values lying within a certain range
    pos = ((x > gap_min) * (x < gap_max)).nonzero()[0]
    x = np.delete(x, pos)[:, None]
    t = np.delete(t, pos)[:, None]

    return x, t


# Initialize a random number generator
# https://numpy.org/doc/2.2/reference/random/generator.html
rng = np.random.default_rng(seed=100)

# Set the number of samples to generate
N = 40

# Setting the range of inputs
x_min, x_max = -2, 7

# Set the value of the noise variance
noise_variance = 6

# We will remove data points with gap_min <= x <= gap_max
gap_min, gap_max = 2.5, 4.5

x, t = generate_synthetic_data(
    rng, N, x_min, x_max, noise_variance, gap_min, gap_max
)

# %% [markdown]
# Let us first plot the data:

# %%
# Plotting-related imports
from matplotlib import pyplot as plt

# %matplotlib inline
# %config InlineBackend.figure_format = "retina"

# %% jupyter={"outputs_hidden": false}
# Plot the data
fig, ax = plt.subplots(figsize=(4, 3))
ax.scatter(x, t, s=3, facecolor="k")
ax.set_xlabel("$x$")
ax.set_ylabel("$f(x)$")
plt.tight_layout()

# %% [markdown]
# We now fit the models and plot predictive mean and variances (as error bars) based on the equations above.

# %% jupyter={"outputs_hidden": false}
# Select the polynomial orders we want to examine
orders = (1, 3, 5, 9)


class PolynomialRegressionModel:
    """Polynomial regression model"""

    def __init__(self, order: int, x, t):
        """
        Class constructor.

        Args:
            order: The order of the polynomial to fit
            x: Training data inputs
            t: Training data outputs
        """
        self.order = order
        x = x.squeeze()
        t = t.squeeze()
        self.X_train = self.get_design_matrix(x)
        self.w, self.sigma_sq = self.train(t)

    def get_design_matrix(self, x):
        """Create design matrix for polynomial regression from a vector of inputs.

        Args:
            x: Vector of inputs.

        Returns:
            Design matrix
        """

        # Get design matrix shape
        X_shape = (x.shape[0], self.order + 1)

        # Initialize design matrix
        X = np.zeros(X_shape)

        # Fill design matrix
        x = x.reshape((x.shape[0], 1))
        for k in range(self.order + 1):
            X[:, k : k + 1] = x**k
        return X

    def compute_cov_w(self):
        """Returns the covariance of the maximum likelihood estimator
        of the model parameters w."""
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        return self.sigma_sq * np.linalg.inv(self.X_train.T @ self.X_train)
        ### SOLUTION END ###

    def train(self, t):
        """
        Train the model using the normal equation, given training data.
        That is, find the best-fit parameters using the matrix normal equation.

        Args:
            t: Vector of outputs

        Returns:
            A 2-tuple (w, sigma_sq), where:
            - w is the MLE for the model parameters
            - sigma_sq is the MLE for the noise variance.
        """
        X = self.X_train
        w = np.linalg.inv(X.T @ X) @ X.T @ t
        sigma_sq = ((1 / N) * (t.T @ t - t.T @ X @ w))
        return w, sigma_sq

    def predict(self, x):
        """Returns a prediction made by the model.

        Args:
            x: Vector of inputs for which to get predictions

        Returns
            Vector of output predictions
        """
        X = self.get_design_matrix(x)
        return X @ self.w

    def predictive_variance(self, x_new):
        """Calculates variance for prediction at x_new.

        This should be a vectorized implementation, that is, it should assume
        that x_new is a vector of inputs, and it should return a vector of the
        same size as x_new, where the elements of the vector are the variances
        corresponding to the values of x_new in the vector.

        Args:
            x_new: Vector of inputs

        Returns:
            Vector of predictive variances, one for each element of x_new.
        """
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        X_test = self.get_design_matrix(x_new)
        X = self.X_train
        N = X_test.shape[0]
        variance = np.zeros(N)
        for k in range(N):
            variance[k] = self.sigma_sq * (
                X_test[k].T @ np.linalg.inv(X.T @ X) @ X_test[k]
            )
        return variance
        ### SOLUTION END ###


# %%
x_new = np.linspace(-2, 7, 50)[:, None]
for order in orders:
    m = PolynomialRegressionModel(order, x, t)
    t_new = m.predict(x_new)
    variances = m.predictive_variance(x_new)
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.scatter(x, t, s=5, facecolor="k")
    ax.errorbar(
        x_new.flatten(), t_new.flatten(), yerr=variances.flatten(), alpha=0.5
    )
    ax.set_title(f"Order {order}")
    plt.tight_layout()
    fig.savefig(f"images/predictive_variance_order_{order}.pdf")

# %% [markdown]
# We notice that the variance decreases but then starts increasing again as the
# model order increases. This is due to the increased flexibility of the higher
# order models, particularly in regions where there is no data. The following
# plots show possible models - as the order increases it's clear that the models
# exhibit greater variability within the areas lacking data.

# %% jupyter={"outputs_hidden": false}
x_new = np.linspace(-2, 7, 50)[:, None]
rng = np.random.default_rng(seed=100)
for i in orders:
    m = PolynomialRegressionModel(i, x, t)
    cov_w = m.compute_cov_w()
    test_mean = m.predict(x_new)
    sampled_ws = rng.multivariate_normal(m.w.flatten(), cov_w, 10)
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.scatter(x, t, s=5, facecolor="k")
    ax.plot(x_new, m.get_design_matrix(x_new) @ sampled_ws.T, "k", alpha=0.1)
    ax.set_title("Order " + str(i))
    plt.tight_layout()
    fig.savefig(f"images/sampled_functions_order_{i}.pdf")

# %% [markdown]
# Let us now see how best fit lines vary with sampled datasets

# %%
num_sample_sets = 20
sample_size = 25

rng = np.random.default_rng(seed=100)

# Sample a new set of inputs
x_new = np.sort(rng.uniform(x_min, x_max, sample_size))
x_test = np.linspace(-2, 7, 100)

# Loop over polynomial orders
for order in (1, 3, 5, 9):
    fig, ax = plt.subplots()
    ax.set_title(f"Order {order}")
    ax.set_ylim(-30, 30)

    # Sample `num_sample_sets` sets of outputs t corresponding to the same set of inputs `x_new`.
    for _ in range(num_sample_sets):

        # Sample outputs given inputs `x_new`
        t = sample_dataset(x_new, noise_variance, rng)

        # Initialize a polynomial regression model of order `order`, with training data (x_new, t).
        m = PolynomialRegressionModel(order, x_new, t)

        # Plot the best-fit line computed from `x_new` and `t` (using MLE).
        ax.plot(x_test, m.get_design_matrix(x_test) @ m.w, "k", alpha=0.1)

    # Plot the mean of the true function
    ax.plot(x_test, true_function(x_test), "k", linewidth=2)
    fig.savefig(f"images/sampled_datasets_order_{order}.pdf")
