"""Unit 2a — Probability & estimation foundations (I): Poisson, Bernoulli MLE, Fisher info.

Only Part A (Poisson) has autograded code. Parts B (Bernoulli MLE) and C (Fisher
information) are written derivations, graded per-step by a human (see specs.md).

Use only the standard-library `math` package for Part A.
"""

import math

LAMBDA, LOW, HIGH = 3, 2, 6


def poisson(x: int, lam: float) -> float:
    """Poisson pmf  P(X=x) = lam^x / x! * e^{-lam}."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return (math.pow(lam, x) / math.factorial(x)) * math.exp(-lam)
    ### SOLUTION END ###
    ...  # placeholder: keeps the stripped student template valid


def calculate_poisson_pmf_a() -> float:
    """P(LOW <= X <= HIGH) for X ~ Poisson(LAMBDA)."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    probability = sum(poisson(y, LAMBDA) for y in range(LOW, HIGH + 1))
    ### SOLUTION END ###
    return probability


def calculate_poisson_pmf_b() -> float:
    """P(X < LOW or X > HIGH) for X ~ Poisson(LAMBDA) — the complement of (a)."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    probability = 1 - calculate_poisson_pmf_a()
    ### SOLUTION END ###
    return probability
