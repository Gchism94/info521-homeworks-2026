"""Unit 0 — Tooling & reproducibility (onboarding).

Set up the toolchain (pytest, the SOLUTION-marker workflow) and learn the seed policy that
every later unit assumes: seeded RNGs are reproducible.
"""
import numpy as np


def add(x, y):
    """Return the sum of x and y."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return x + y
    ### SOLUTION END ###
    ...  # placeholder


def seeded_draw(seed, n):
    """Draw n samples from a SEEDED generator so the result is reproducible.
    The seed policy (taught here, assumed everywhere after): same seed -> same draw."""
    ### YOUR CODE HERE ###
    ### SOLUTION START ###
    return np.random.default_rng(seed).uniform(0, 1, n)
    ### SOLUTION END ###
    ...  # placeholder
