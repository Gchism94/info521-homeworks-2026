"""Tests for the hw."""

import numpy as np
from pytest import approx

from hw import MetropolisSampler, X, t


def test_log_likelihood():
    sampler = MetropolisSampler(X, t, 0.1, 0.5)
    assert sampler.log_likelihood(np.array([0, 0])) == approx(
        -27.725887222397812
    )
    assert sampler.log_likelihood(np.array([4, 3])) == approx(
        -0.024440235038283346
    )
    assert sampler.log_likelihood(np.array([1, 2])) == approx(
        -0.37838713200054364
    )


def test_log_prior():
    sampler = MetropolisSampler(X, t, 0.1, 0.25)
    assert sampler.log_prior(np.array([0, 0])) == approx(-0.0)
    assert sampler.log_prior(np.array([-2, 3])) == approx(-26.0)
    assert sampler.log_prior(np.array([1, 2])) == approx(-10.0)


def test_sample_from_proposal():
    sampler = MetropolisSampler(X, t, 0.1, 0.5, seed=100)
    current_sample = np.array([1.0, 2.0])
    candidate_sample = sampler.sample_from_proposal(current_sample)
    assert candidate_sample.shape == (2,)

    # Using the same seed should result in the same candidate sample drawn.
    sampler2 = MetropolisSampler(X, t, 0.1, 0.5, seed=100)
    assert sampler2.sample_from_proposal(current_sample) == approx(
        candidate_sample
    )


def test_compute_acceptance_ratio():
    sampler = MetropolisSampler(X, t, 0.1, 0.5)
    current_sample = np.array([0.0, 0.0])
    candidate_sample = np.array([4.0, 3.0])
    assert sampler.compute_acceptance_ratio(
        current_sample, candidate_sample
    ) == approx(np.exp(2.701446987359529))


def test_generate_sample():
    sampler = MetropolisSampler(X, t, 0.1, 0.5, seed=100)
    w = np.array([0.0, 0.0])

    # The first two candidates will be rejected (w stays at [0, 0])
    assert sampler.generate_sample(w) == approx([0.0, 0.0])
    assert sampler.generate_sample(w) == approx([0.0, 0.0])

    # The candidate is accepted
    assert sampler.generate_sample(w) == approx(
        [0.2218197563565942, 0.22293218080707125]
    )


def test_generate_samples():
    sampler = MetropolisSampler(X, t, 0.1, 0.5, seed=100)
    samples = sampler.generate_samples(num_samples=3)
    first_six = np.array([v for pair in samples for v in list(pair)])
    assert first_six == approx(
        [0, 0, 0, 0, 0.2218197563565942, 0.22293218080707125]
    )
