# %% [markdown]
r"""
# Estimating $\pi$ with Monte Carlo sampling

## Overview

In this notebook you will estimate $\pi$ using sampling, and in the process get
a taste of the curse of dimensionality.

Fill in the missing pieces of code at the markers that say
`### YOUR CODE HERE ###`.
"""

# %%
import math
import numpy as np
import mplcursors
from matplotlib import pyplot as plt
from tqdm import tqdm

# Initialize a random number generator
RNG = np.random.default_rng()

# %% [markdown]
r"""
## Sampling in 2 dimensions

(Adapted from FCML Exercise 4.4)

Implement `estimate_pi_using_circle` below.
*Hint*: use
[`numpy.random.Generator.uniform`](https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.uniform.html) to draw samples, and boolean indexing to select the accepted ones.
"""

# %%
def estimate_pi_using_circle(n_samples: int) -> float:
    """Estimate pi using the expression for the area of a circle.
    Args:
        n_samples: Number of random samples to draw.

    Returns:
        An estimate of pi.
    """
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    samples = RNG.uniform(0, 1, (2, n_samples))
    accepted = samples[:, (samples[0]**2 + samples[1]**2) < 1]
    return 4 * (accepted[0].size / samples[0].size)
    ### SOLUTION END ###

# %% [markdown]
r"""
## Sampling in $n$ dimensions

The volume of the unit $n$-ball is:

$$V_n = \frac{\pi^{n/2}}{\Gamma\!\left(\frac{n}{2} + 1\right)}$$

Implement `estimate_pi_using_n_ball`, which should return the **running**
sequence of estimates as samples are added one by one (so the returned list
has length `n_samples - 1`).  Use `math.gamma` for the gamma function.
"""

def number_of_orthants(n: int) -> int:
    """
    Get the number of orthants for an n-ball.

    Args:
        n: number of dimensions of the n-ball.

    Returns:
        The number of orthants of an n-ball.
    """

    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return 2**n
    ### SOLUTION END ###


# %%
def estimate_pi_using_n_ball(n: int, n_samples: int) -> list[float]:
    """Estimate pi the expression for the volume of an n-ball,
    returning a running sequence of estimates as samples are added one by one.

    Args:
        n: Dimension of the ball.
        n_samples: Total number of random samples to draw.

    Returns:
        A list of length n_samples - 1 containing the pi estimate after
        each successive sample.
    """
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    samples = RNG.uniform(0, 1, (n, n_samples))
    estimates = []

    for n_subset in range(1, n_samples):
        samples_subset = samples[:, :n_subset]
        accepted = samples_subset[:, np.sum(samples_subset**2, axis=0) < 1]
        V_o = accepted[0].size / samples_subset[0].size
        pi_estimate = (number_of_orthants(n) * V_o * math.gamma(n * 0.5 + 1))**(2/n)
        estimates.append(pi_estimate)
    return estimates
    ### SOLUTION END ###

# %% [markdown]
r"""
## Convergence across dimensions

The cell below provides a vectorized helper `estimate_pi_n_ball_running` and a
plotting function `plot_samples_needed`.  These are already implemented for
you — run the cell to see how the mean absolute error $|\hat\pi - \pi|$
decreases with sample count for each dimension on a log-log scale.

Notice that:
- All curves have approximately the same slope of $-\frac{1}{2}$, confirming
  the universal $\mathcal{O}(1/\sqrt{N})$ Monte Carlo convergence rate.
- Higher-dimensional curves sit higher (larger error for the same $N$),
  because the acceptance rate decreases with dimension.
"""

# %%
def estimate_pi_n_ball_running(n: int, n_samples: int) -> np.ndarray:
    """Compute running pi estimates from the volume of a positive orthant of
    the unit n-ball, vectorized over all sample counts simultaneously.

    Samples n_samples points uniformly in [0,1]^n, then uses a cumulative
    sum to compute the acceptance rate V_o after each sample, and converts
    to a pi estimate via: pi = (2^n * V_o * Gamma(n/2 + 1))^(2/n).

    Args:
        n: Dimension of the ball.
        n_samples: Total number of random samples to draw.

    Returns:
        An array of shape (n_samples,) containing the pi estimate after
        each successive sample.
    """
    samples = RNG.uniform(0, 1, (n, n_samples))
    accepted = np.sum(samples**2, axis=0) < 1
    V_o = np.cumsum(accepted) / np.arange(1, n_samples + 1)
    return ((2**n) * V_o * math.gamma(n * 0.5 + 1))**(2/n)


def plot_samples_needed() -> None:
    """Plot mean absolute error of pi estimates vs. sample count for several
    n-ball dimensions on a log-log scale.

    For each dimension n in [2, 5, 10, 15],  runs n_trials independent trials of
    estimate_pi_n_ball_running and plots the mean |estimate - pi| with a +/- 1
    standard deviation shaded band. Log-spaced sample counts are used so
    that all decades are equally represented on the x-axis.

    Saves the figure to 'estimates.pdf'.
    """
    ns = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    n_samples = 100000
    n_trials = 200
    sample_counts = np.unique(
        np.logspace(0, np.log10(n_samples), 100).astype(int)
    )

    threshold = 0.1

    plt.style.use("ggplot")
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    crossing_samples = {}

    for n in tqdm(ns, unit="dim"):
        errors = np.array([
            np.abs(estimate_pi_n_ball_running(n, n_samples)[sample_counts - 1] - np.pi)
            for _ in tqdm(range(n_trials), unit="trial", leave=False)
        ])
        mean_err = errors.mean(axis=0)
        std_err = errors.std(axis=0)
        line, = ax.plot(sample_counts, mean_err, label=f"D={n}")
        ax.fill_between(
            sample_counts,
            np.maximum(mean_err - std_err, 1e-3),
            mean_err + std_err,
            alpha=0.2,
            color=line.get_color(),
        )
        idx = np.argmax(mean_err < threshold)
        if idx > 0:
            crossing_samples[n] = sample_counts[idx]

    ax.axhline(threshold, color="black", linestyle="--", linewidth=0.8, label=f"threshold={threshold}")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.minorticks_on()
    ax.grid(which="minor", alpha=0.3)
    ax.set_xlabel("Number of samples")
    ax.set_ylabel(r"$|\hat{\pi} - \pi|$")
    ax.legend()

    if crossing_samples:
        dims = list(crossing_samples.keys())
        counts = list(crossing_samples.values())
        ax2.plot(dims, counts, "o-")
        ax2.set_yscale("log")
        ax2.minorticks_on()
        ax2.grid(which="minor", alpha=0.3)
        ax2.set_xlabel("Dimension")
        ax2.set_ylabel(f"Samples to reach $|\\hat{{\\pi}} - \\pi| < {threshold}$")

    plt.tight_layout()
    plt.savefig("estimates.pdf")


plot_samples_needed()
