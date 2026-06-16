# # Exact Bayesian Inference for Coin Game Scenario
#
# Author: Adarsh Pyarelal
#
# (Adapted from code originally written by Clayton Morrison)

# NOTE: You are only allowed to use the following imports.
#       You may not import any other modules / functions.
from scipy.special import gamma  # The Gamma function
from scipy.special import loggamma  # The log of the Gamma function
from scipy.special import (
    binom,
)  # binomial coefficient; i.e.: number of combinations, AKA "N choose K"
import numpy as np  # NOTE: includes numpy.log and numpy.exp
from matplotlib import pyplot as plt
# %matplotlib inline
# %config InlineBackend.figure_format = "retina"

def B(a: float, b: float):
    """Returns the beta function B(a, b) (see PML1 section 2.7.4)."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return (gamma(a) * gamma(b)) / gamma(a + b)
    ### SOLUTION END ###


def Beta(r, a: float, b: float):
    """Computes the beta distribution Beta(r|a, b) (see PML1 section 2.7.4)."""

    # Hint: You can use the beta function you implemented above.
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return (1 / B(a, b)) * np.power(r, a - 1) * np.power((1 - r), b - 1)
    ### SOLUTION END ###


def posterior(r, N: int, y_N: int, a: float, b: float):
    """
    Calculates the posterior density of r.

    Args:
        r: Vector of values of r for which to compute the posterior density.
        N: Total number of coin flips.
        y_N: Number of observed heads
        a: Parameter of the prior Beta(r|a, b) - can be loosely interpreted as number of
           heads previously observed in (a + b) coin tosses.
        b: Parameter of the prior Beta(r|a, b) - can be loosely interpreted as number of
           tails previously observed in (a + b) coin tosses.

    Returns:
         Vector of values corresponding to the prior density evaluated for a
         vector of values of r.
    """
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    a_posterior = y_N + a
    b_posterior = N - y_N + b
    return Beta(r, a_posterior, b_posterior)
    ### SOLUTION END ###


def calculate_marginal_likelihood(
    N: int, y_N: int, a: float, b: float
) -> float:
    """
    Calculates the marginal likelihood of the data as a function of the
    prior parameterization.

    NOTE: Due to the potential for numerical underflow while performing the
    calculation, it is recommended to calculate the marginal likelihood in log-space
    (i.e., take the log of the equation used to compute the marginal likelihood)
    and then take the exponential of the result (np.exp(result)) to get back the
    probability density.

    You can use the `loggamma` function imported at the top of the module for
    this implementation.

    Note however, that you do not need a 'logbinom' function, you can simply do
    `np.log(binom(_, _))`.

    Args:
        n: Total number of observations (how many coin flips)
        y_N: Number of observed heads
        a: Parameter of the prior Beta(r|a, b) - can be loosely interpreted as number of
           heads previously observed in (a + b) coin tosses.
        b: Parameter of the prior Beta(r|a, b) - can be loosely interpreted as number of
           tails previously observed in (a + b) coin tosses.

    Returns:
        The marginal likelihood.
    """
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    marginal_likelihood = (
        np.log(binom(N, y_N))
        + loggamma(a + b)
        - loggamma(a)
        - loggamma(b)
        + loggamma(a + y_N)
        + loggamma(b + N - y_N)
        - loggamma(a + b + N)
    )
    marginal_likelihood = np.exp(marginal_likelihood)
    return marginal_likelihood
    ### SOLUTION END ###


def calculate_probability_of_winning(
    N: int, y_N: int, a: float, b: float
) -> float:
    """
    Returns the probability of winning given the observed data and the
    prior.

    NOTE: Due to the potential for numerical underflow while performing the
    calculation, it is recommended to calculate the marginal likelihood in
    log-space (i.e., take the log of the equation used to compute the marginal
    likelihood) and then take the exponential of the result (np.exp(result))
    to get back the probability density.

    Args:
        N: Number of coin flips
        y_N: Number of observed heads
        a: Parameter of the prior Beta(r|a, b) - can be loosely interpreted as number of
           heads previously observed in (a + b) coin tosses.
        b: Parameter of the prior Beta(r|a, b) - can be loosely interpreted as number of
           tails previously observed in (a + b) coin tosses.

    Returns:
        Probability of winning given observed data and prior.
    """

    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    def expected_value_new_observation(y_new):
        a_posterior = a + y_N
        b_posterior = b + N - y_N
        log_expected_value = (
            np.log(binom(10, y_new))
            + loggamma(a_posterior + b_posterior)
            - loggamma(a_posterior)
            - loggamma(b_posterior)
            + loggamma(a_posterior + y_new)
            + loggamma(b_posterior + 10 - y_new)
            - loggamma(a_posterior + b_posterior + 10)
        )
        return np.exp(log_expected_value)

    total_prob_of_losing = 0
    for y_new in range(7, 11):
        total_prob_of_losing += expected_value_new_observation(y_new)
    probability_of_winning = 1 - total_prob_of_losing
    return probability_of_winning
    ### SOLUTION END ###


def plot_densities(r, prior, posterior, title: str):
    """
    Helper function to plot the prior and posterior

    Args:
        r: Array of r values (between 0 and 1) -- determines the x-axis values
        prior: Prior density values -- determines y-axis values
        posterior: Posterior density values -- determines y-axis values
        title: Title of the figure (Used to indicate the scenario)
        plot_root: Path to root directory for plots to be saved

    Returns:
        None
    """
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(r, prior, label="prior")
    ax.plot(r, posterior, label="posterior")
    ax.set_xlabel("$r$")
    ax.set_ylabel("$p(r)$")
    plt.legend(loc="upper left")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f"{title}.pdf")


def run_scenario(
    N: int,
    y_N: int,
    a: float,
    b: float,
    title: str,
    plot_p: bool = True,
):
    """
    Calculate the prior and posterior densities, the marginal
    likelihood of the data, and the probability of winning the game (assuming
    you need 6 or fewer heads out of 10 tosses) given prior beliefs about
    heads and tails, and the observed data (parameterized by the total number
    of coin flips, N, and the number of heads, y_N).

    Args:
        N: Total number of observations
        y_N: Total number of observed heads
        a: Parameter of the prior Beta(r|a, b) - can be loosely interpreted as number of
           heads previously observed in (a + b) coin tosses.
        b: Parameter of the prior Beta(r|a, b) - can be loosely interpreted as number of
           tails previously observed in (a + b) coin tosses.
        title: Title of scenario
        plot_p: Flag controlling whether to plot; default True

    Returns:
        A tuple (r_prior, r_posterior, marginal_likelihood, probability_of_winning), where

        - r_prior, r_posterior are vectors of prior density values computed for
          100 equally-spaced values of r between 0 and 1.
        - marginal_likelihood is the marginal likelihood of the observed data
          given the prior parameters
        - probability_of_winning is the expected probability of winning the
          game given the prior and observed data.
    """
    print(f"Calculating beliefs for {title}\n")
    r = np.linspace(0, 1, 100)

    r_prior = Beta(r, a, b)
    r_posterior = posterior(r, N, y_N, a, b)
    marginal_likelihood = calculate_marginal_likelihood(N, y_N, a, b)
    probability_of_winning = calculate_probability_of_winning(N, y_N, a, b)

    if plot_p:
        plot_densities(r, r_prior, r_posterior, title)

    print(f"marginal_likelihood: {marginal_likelihood:.2f}")
    print(f"probability_of_winning: {probability_of_winning:.2f}")

    return r_prior, r_posterior, marginal_likelihood, probability_of_winning


if __name__ == "__main__":
    # The evidence:
    N = 20  # Number of coin flips
    y_N = 14  # number of observed heads

    # Scenarios - differences in prior beliefs
    run_scenario(N, y_N, 1, 1, "Scenario_1")
    run_scenario(N, y_N, 50, 50, "Scenario_2")
    run_scenario(N, y_N, 5, 1, "Scenario_3")
