# %% [markdown]
r"""
# Bayesian Logistic Regression Classifier – Estimation Methods

Adarsh Pyarelal

(Adapted from notebook originally developed by Simon Rogers and modified by Clayton Morrison)

In this notebook, you will implement a Metropolis-Hastings Markov Chain Monte Carlo (MH-MCMC) sampler to perform inference for Bayesian logistic regression.
"""

# %% [markdown]
# Import numpy, matplotlib, set up plot style:

# %%
import numpy as np
from tqdm import trange
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

# %matplotlib inline
# %config InlineBackend.figure_format = "retina"


# %% [markdown]
# Load the data (this is the same data used in the binary
# classification example in FCML Chapter 4).

# %%
X = np.loadtxt("data/X.csv", delimiter=",") # Design matrix
t = np.loadtxt("data/t.csv") # target vector

# %% [markdown]
# Plot the data. The plot should look similar to FCML Figure 4.1


# %%
def plot_data(X, t) -> tuple[Figure, Axes]:
    """Plot the binary classification dataset.

    Args:
        X: Design matrix of shape (N, 2) with input observations.
        t: Target vector of shape (N,) with binary class labels (0 or 1).

    Returns:
        Tuple of (fig, axes) for the resulting plot.
    """
    fig, axes = plt.subplots(figsize=(5, 4))

    # Plot class 0
    pos = np.where(t == 0)[0]
    axes.plot(X[pos, 0], X[pos, 1], "ko")

    # Plot class 1
    pos = np.where(t == 1)[0]
    axes.plot(X[pos, 0], X[pos, 1], "ks", markerfacecolor="none")

    axes.set_xlabel("$x_1$")
    axes.set_ylabel("$x_2$")

    axes.set_xlim([-5, 5])
    axes.set_ylim([-5, 5])
    plt.tight_layout()
    return fig, axes

plot_data(X, t)


# %%
def logistic(x):
    """The logistic function. Is automatically vectorized when you pass in a numpy array.
    Args:
        x: Input array.

    Returns:
        Array of the same shape as x with the logistic function applied element-wise.
    """
    return 1 / (1.0 + np.exp(-x))


# %% [markdown]
# ## Metropolis-Hastings
#
# We now turn to implementing an MH-MCMC sampler. Fill out the missing code in the `MetropolisSampler` class below at the markers that say `### YOUR CODE HERE`.
#
# In order to maintain numeric stability, instead of computing the acceptance ratio directly,
# first compute the logarithm of the acceptance ratio (use the `log_prior` and `log_likelihood` methods that you will implement along the way)
# and then exponentiate it. This will help you avoid underflow issues. I recommend deriving the mathematical expressions for the log likelihood and log prior before writing any code.
#
# Use a Gaussian prior with mean $\mathbf{0}$ and covariance $\sigma_\text{prior}^2\mathbf{I}$.
#
# For the proposal distribution, use a Gaussian centered at the current sample, with covariance given by $\sigma_\text{proposal}^2\mathbf{I}$.

# %%
class MetropolisSampler:
    """Metropolis sampler for the posterior for Bayesian logistic regression weights."""

    def __init__(
        self,
        X,
        t,
        proposal_variance: float,
        prior_variance: float,
        seed: int = 100,
    ) -> None:
        """Initialize the sampler.

        Args:
            X: Design matrix of observed inputs
            t: Vector of observed binary response labels
            proposal_variance: Variance $\sigma_{proposal}^2$ for the diagonal Gaussian proposal covariance matrix.
            prior_variance: Variance $\sigma_{prior}^2$ for the diagonal Gaussian prior covariance matrix.
            seed: Seed for the random number generator.
        """
        self.X = X
        self.t = t
        self.proposal_variance = proposal_variance
        self.prior_variance = prior_variance
        self.proposal_cov = np.eye(X.shape[1]) * proposal_variance
        self.rng = np.random.default_rng(seed=seed)

    def log_likelihood(self, w) -> float:
        """Calculate the log likelihood of w given the observed data.

        Args:
            w: Parameter vector

        Returns:
            The log likelihood of w given self.X and self.t.
        """
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        P = logistic(self.X @ w)
        return (self.t @ np.log(P) + (1 - self.t) @ np.log(1 - P)).sum()
        ### SOLUTION END ###

    def log_prior(self, w) -> float:
        """Calculate the log Gaussian prior (up to an additive constant).

        Only includes the term involving w; constant terms cancel in the MH
        log acceptance ratio.

        Args:
            w: Parameter vector

        Returns:
            The scalar log prior density of w
        """
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        return -(1.0 / (2.0 * self.prior_variance)) * (w.T @ w)
        ### SOLUTION END ###

    def sample_from_proposal(self, w):
        """Draw a candidate sample from the proposal distribution.

        Args:
            w: Current sample

        Returns:
            Candidate sample from proposal distribution
        """
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        candidate_sample = self.rng.multivariate_normal(w, cov=self.proposal_cov)
        return candidate_sample
        ### SOLUTION END ###


    def compute_acceptance_ratio(self, w, w_candidate) -> float:
        """Returns the acceptance ratio (FCML Equation 4.17) 

        Args:
            w: Current sample
            w_candidate: Candidate sample

        Returns:
            Acceptance ratio
        """
        # Implement the computation of the acceptance ratio here.
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        log_r = (
            self.log_prior(w_candidate)
            + self.log_likelihood(w_candidate)
            - self.log_prior(w)
            - self.log_likelihood(w)
        )
        return np.exp(log_r)
        ### SOLUTION END ###

    def generate_sample(self, w):
        """Generate a sample from the chain.

        Args:
            w: Current sample

        Returns:
            Next sample
        """
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        w_candidate = self.sample_from_proposal(w)
        r = self.compute_acceptance_ratio(w, w_candidate)
        return w_candidate if self.rng.uniform(0, 1) <= r else w
        ### SOLUTION END ###

    def generate_samples(self, num_samples: int) -> list:
        """Generate samples from the chain

        Args:
            num_samples: Number of samples to draw.

        Returns:
            List of samples
        """
        ### YOUR CODE HERE ###
        ### SOLUTION START ###
        # Initialize current sample
        current_sample = np.array([0, 0])
        samples = []
        for _ in trange(num_samples, ncols=70):
            current_sample = self.generate_sample(current_sample)
            samples.append(current_sample)
        return samples
        ### SOLUTION END ###

# %% [markdown]
# The following uses the sampler to gather 5000 samples with $\sigma_\text{proposal}^2 = 0.1$ and $\sigma_\text{prior}^2 = 0.5$.

# %%
# Create an instance of the sampler
SAMPLER = MetropolisSampler(X, t, 0.1, 2)

# Generate 5000 samples. 
W_SAMPLES = SAMPLER.generate_samples(5000)

# %% [markdown]
# Next, plot the samples themselves. Locate the initial sample point -- you will see that it looks a little out of the ordinary compared to the general shape of the posterior. This is an example of a sample that are likely part of the "burn-in" portion of the sampler. In this simple exercise, we are ignoring identification of burn-in, and instead using all of the samples. The shape of the samples should be similar to FCML Figure 4.12(a).

# %%
def plot_w_samples(w_samples: list) -> tuple[Figure, Axes]:
    """Plot posterior samples.

    Args:
        w_samples: List of samples

    Returns:
        Tuple of (fig, axes) for the resulting plot.
    """
    fig, axes = plt.subplots(figsize=(5, 4))
    axes.plot(*zip(*w_samples), "k.", alpha=0.2)
    axes.set_xlabel("$w_1$")
    axes.set_ylabel("$w_2$")
    plt.tight_layout()
    return fig, axes

# %%
plot_w_samples(W_SAMPLES)

# %% [markdown]
# If we plot again, this time, using samples starting at sample 200, then by this point the sampler has likely converged to the stationary distribution. See the difference in the shape of the samples; the main change in shape is that now we don't have those points in the lower-left of the density, including the starting point of (0,0) -- those were likely part of the burn-in phase before convergence.

# %%
plot_w_samples(W_SAMPLES[2000:])

# %% [markdown]
# The following plots the decision boundaries corresponding to 20 samples taken starting at sample 200 in the sample set. These are chosen so that chain is almost certainly burned in. Your plot should look similar to (but may not be identical to) FCML Figure 4.12(f).


# %%
def plot_w_samples_decision_boundaries(
    X,
    t,
    w_samples: list,
    sample_start: int = 0,
    sample_end: int = 10,
) -> None:
    """Plot decision boundary lines for a subset of samples.

    Args:
        X: Design matrix
        t: Target vector
        w_samples: List of samples
        sample_start: Index of the first sample to plot.
        sample_end: Index one past the last sample to plot.
    """
    _, axes = plot_data(X, t)
    for w_sample in w_samples[sample_start:sample_end]:
        # Plot the line corresponding to w.T x = 0
        x = np.array([-5, 5])
        y = (-w_sample[1] / w_sample[0]) * x
        axes.plot(x, y, color="k", linewidth=0.5)


plot_w_samples_decision_boundaries(X, t, W_SAMPLES, 200, 220)

# %% [markdown]
# The following plots the probability contours with the data. Again, we are using samples starting after sample 200, assuming the sampler has converged to the stationary distribution by this point. The resulting plot should look similar to FCML Figure 4.12(e).

# %%
def plot_w_samples_contours(
    X,
    t,
    w_samples: list,
    sample_start: int = 0,
    sample_end: int = 10,
) -> None:
    """Plot class-probability contours estimated from a subset of samples.

    Args:
        X: Design matrix
        t: Target vector
        w_samples: List of samples from posterior
        sample_start: Index of the first sample to use.
        sample_end: Index one past the last sample to use.
    """
    gridX, gridY = np.meshgrid(np.arange(-5, 5, 0.1), np.arange(-5, 5, 0.1))

    # Select the samples from w_samples to use to estimate label probability countours.
    sample_design_matrix = np.zeros((sample_end - sample_start, 2))

    for i, sample in enumerate(w_samples[sample_start:sample_end]):
        sample_design_matrix[i, :] = sample

    n_rows, n_cols = gridX.shape

    gx = np.reshape(gridX, (n_rows * n_cols, 1))
    gy = np.reshape(gridY, (n_rows * n_cols, 1))

    g = np.hstack((gx, gy))

    # Compute expected probabilities using the samples (FCML Equation 4.15)
    # Compute probability for each sample, then take the mean of the probabilities
    P = logistic(g @ sample_design_matrix.T).mean(axis=1)
    P = np.reshape(P, (n_rows, n_cols))

    _, axes = plot_data(X, t)

    CS = axes.contour(
        gridX,
        gridY,
        P,
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
        colors="k",
        linewidths=0.5,
    )
    axes.clabel(CS, list(CS.levels), inline=True)
    axes.set_xlim((-5, 5))
    axes.set_ylim((-5, 5))
# %%
plot_w_samples_contours(X, t, W_SAMPLES, 200, 5000)

# %%
