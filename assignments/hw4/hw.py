# # HW4
#
# ## Poisson probabilities
#
# (Adapted from FCML Ex. 2.3)
#
# $X$ is a random variable that can take any non-negative integer
# value. The probability mass function for $X$ is the Poisson distribution:
#
# $$
#     P(X = x) = \frac{\lambda^x}{x!}e^{-\lambda}
# $$
#
# Using the facts that (i) for a discrete random variable, the pmf gives the probabilities of the individual events occurring, and (ii) the probabilities are additive, fill in the necessary code below to compute the following:
#
# 1. In `calculate_poisson_pmf_a`, compute the probability that $2 \leq X \leq 6$ for $\lambda = 3$.
# 2. In `calculate_poisson_pmf_b`, using the fact that one outcome has to happen, compute the probability that $X < 2$ or $X > 6$ (again, for $\lambda = 3$).
#
# Do not use any packages other than the `math` package from the
# Python standard library. 

import math

LAMBDA, LOW, HIGH = 3, 2, 6

def poisson(x: int, lam: float) -> float:
    """Returns the Poisson pmf given x and lambda"""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return (math.pow(lam, x) / math.factorial(x)) * math.exp(-lam)
    ### SOLUTION END ###

def calculate_poisson_pmf_a() -> float:
    """
    Calculate probability that LOW <= X <= HIGH for X ~ Poisson(lambda=LAMBDA)
    """
    # Set the variable `probability` to the answer
    ### YOUR CODE HERE
    ### SOLUTION START ###
    probability = sum(poisson(y, LAMBDA) for y in range(LOW, HIGH+1))
    ### SOLUTION END ###
    return probability


def calculate_poisson_pmf_b() -> float:
    """
    Calculate probability that X < LOW or X > HIGH for X ~ Poisson(lambda=LAMBDA)
    """
    # Set the variable `probability` to the answer
    ### YOUR CODE HERE
    ### SOLUTION START ###
    probability = 1 - calculate_poisson_pmf_a()
    ### SOLUTION END ###
    return probability

# ## Workload
#
# How many hours did you spend on this homework assignment outside of class?
#
# ## Acknowledgments
#
# Cite all the people you've worked with on this homework, as well as any other resources you used apart from the FCML textbook. If you did not work with anyone else, please say so.
#


