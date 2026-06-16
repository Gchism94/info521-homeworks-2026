# hw16 — Overhaul draft (Scope A pilot · stochastic/MCMC template)

Instantiates `OVERHAUL_FRAMEWORK.md` on hw16 (Metropolis-Hastings MCMC for Bayesian
logistic regression). **Draft only — no hw16 files are modified.** This is the template for
the whole approximate-inference cluster (hw13/14/15/16 → Unit 5, "four ways to the same
posterior"): tests check *formulas* and *distributional recovery*, never pinned RNG draws.

Real API confirmed in `hw16/hw.py`:
`MetropolisSampler(X, t, proposal_variance, prior_variance, seed=100)` with
`log_likelihood(w)`, `log_prior(w)`, `sample_from_proposal(w)`,
`compute_acceptance_ratio(current, candidate)`, `generate_sample(w)`,
`generate_samples(num_samples)`; module-level `X, t` from `data/`; `SAMPLER = MetropolisSampler(X, t, 0.1, 2)`
at `hw.py:234` plus sampling/plotting at module scope.

**Audit corrections carried in:** the "prior_variance 2-vs-0.5" report was *not* a bug
(tests build their own samplers — `REVIEW.md` corrected claim #1). The real problems are
(a) `test_generate_sample`/`test_generate_samples` pin the exact accepted draws **and** the
exact accept/reject pattern under `seed=100`, coupling the grade to the RNG *call order*
inside the student's code; and (b) module-level sampling/plotting runs at import (slow/fragile
under the 10s CI timeout).

---

## 1. Prompt rewritten into the 8-part template (replaces `hw16/README.md` body + `hw.py` cells)

**1. Context & purpose.** When a posterior has no closed form, MCMC lets you *sample* from
it and estimate any expectation you want. You'll build the simplest sampler
(Metropolis-Hastings) for the same Bayesian logistic model you approximated with Laplace in
hw15 — and check that two very different methods recover the *same* posterior.

**2. Learning objectives.** By the end you can:
- **O1** Compute a log-likelihood and log-prior in a numerically stable way.
  *(Apply — autograded)*
- **O2** Form the Metropolis acceptance ratio from those log-densities. *(Apply — autograded)*
- **O3** Run a chain whose stationary distribution is the posterior. *(Analyze — autograded)*
- **O4** Judge the sampler: does it recover hw15's posterior? how is mixing/acceptance?
  *(Evaluate — rubric)*

**3. The task (outcome, not recipe).** Implement the sampler and draw a chain for the
posterior of a Bayesian logistic-regression weight vector. Demonstrate that the chain's
posterior mean/covariance match the hw15 Laplace estimate within tolerance, and report the
acceptance rate.

**4. What you may and may not use.** Any internally-consistent RNG usage is fine — the
grade does **not** depend on your draw order or seed. You must work in **log-space** for the
likelihood/prior (numerical stability), and the acceptance test must be a correct
Metropolis ratio.

**5. How you'll be assessed (shown up front).**
- *Correctness (autograded, 55%)* — `log_likelihood`/`log_prior` match their defining
  formulas; `compute_acceptance_ratio` equals `exp(Δlog-posterior)`; a burned-in chain
  recovers the reference posterior mean within tolerance; covariance is symmetric PSD;
  acceptance rate is in a sane band. Thresholds visible in `test_hw.py`.
- *Interpretation (rubric, 35%)* — the §6 prompts.
- *Process (10%)* — seeded, runs clean (no work at import), labeled trace/contour plots.

**6. Required interpretation** (markdown cells in `hw.py`):
- **(i)** Compare your MCMC posterior mean/covariance to hw15's Laplace result — where do
  they agree, where differ, and why?
- **(ii)** Report and interpret your acceptance rate: what does a very high or very low rate
  say about the proposal variance?

**7. Going further (optional).** Sweep the proposal variance and plot acceptance rate vs.
effective sample size; comment on the trade-off.

**8. Submission & reproducibility.** Seed via the `seed=` constructor arg. Guard all
sampling/plotting behind `if __name__ == "__main__":` so importing the module is cheap (the
autograder imports it). Implement the unchanged method contract.

---

## 2. Rewritten `test_hw.py` (formula + distributional recovery; no pinned draws)

Independent tests, actionable messages. `log_likelihood`/`log_prior`/acceptance are
deterministic given data ⇒ checked against their formulas (not magic constants). Everything
stochastic is checked by *recovery/property*, robust to RNG-stream changes and call order.

```python
"""Tests for hw16 — formula checks + distributional recovery, not pinned RNG draws."""
import numpy as np
from pytest import approx
from hw import MetropolisSampler, X, t

def _sampler(seed=0):
    return MetropolisSampler(X, t, 0.1, 0.5, seed=seed)

# --- O1: log-likelihood equals the Bernoulli logistic formula (any equivalent impl) ---
def test_log_likelihood_matches_formula():
    s = _sampler()
    for w in (np.array([0.0, 0.0]), np.array([1.0, 2.0]), np.array([4.0, 3.0])):
        p = 1.0 / (1.0 + np.exp(-(X @ w)))
        expected = np.sum(t * np.log(p) + (1 - t) * np.log(1 - p))
        assert s.log_likelihood(w) == approx(expected, rel=1e-9), \
            f"log_likelihood({w}) should be {expected:.6f}"

# --- O1: log-prior equals the diagonal-Gaussian formula -(1/2σ²) wᵀw ---
def test_log_prior_matches_formula():
    sigma2 = 0.25
    s = MetropolisSampler(X, t, 0.1, sigma2, seed=0)
    for w in (np.array([0.0, 0.0]), np.array([-2.0, 3.0]), np.array([1.0, 2.0])):
        expected = -(1.0 / (2.0 * sigma2)) * (w @ w)
        assert s.log_prior(w) == approx(expected, rel=1e-9), \
            f"log_prior({w}) should be {expected:.6f}"

# --- O2: acceptance ratio = exp(Δ log-posterior) ---
def test_acceptance_ratio_matches_formula():
    s = _sampler()
    cur, cand = np.array([0.0, 0.0]), np.array([4.0, 3.0])
    log_r = (s.log_prior(cand) + s.log_likelihood(cand)) - (s.log_prior(cur) + s.log_likelihood(cur))
    assert s.compute_acceptance_ratio(cur, cand) == approx(np.exp(log_r), rel=1e-9)

# --- O3: proposal is shaped right and reproducible under a fixed seed (no value pin) ---
def test_proposal_shape_and_reproducible():
    a = MetropolisSampler(X, t, 0.1, 0.5, seed=123)
    b = MetropolisSampler(X, t, 0.1, 0.5, seed=123)
    w = np.array([1.0, 2.0])
    pa, pb = a.sample_from_proposal(w), b.sample_from_proposal(w)
    assert pa.shape == (2,), f"proposal should have shape (2,), got {pa.shape}"
    assert pa == approx(pb), "same seed must give the same proposal draw"

# --- O3: a burned-in chain recovers the posterior (method-agnostic, RNG-stream-robust) ---
def test_chain_recovers_posterior_mode():
    s = _sampler(seed=0)
    chain = np.asarray(s.generate_samples(num_samples=20000))[5000:]   # drop burn-in
    mean = chain.mean(axis=0)
    # Reference MAP/Laplace mean for this dataset (shared with hw15); loose tolerance.
    W_REF = np.array([1.63985881, 1.99983755])
    assert mean == approx(W_REF, rel=0.15, abs=0.15), \
        f"posterior mean {mean} should be near the hw15 MAP {W_REF}"

def test_chain_covariance_symmetric_psd():
    s = _sampler(seed=1)
    chain = np.asarray(s.generate_samples(num_samples=20000))[5000:]
    cov = np.cov(chain.T)
    assert np.allclose(cov, cov.T), "posterior covariance must be symmetric"
    assert np.all(np.linalg.eigvalsh(cov) > 0), "posterior covariance must be positive definite"

def test_acceptance_rate_in_sane_band():
    s = _sampler(seed=2)
    chain = np.asarray(s.generate_samples(num_samples=5000))
    moves = np.any(np.diff(chain, axis=0) != 0, axis=1)
    rate = moves.mean()
    assert 0.05 <= rate <= 0.95, f"acceptance rate {rate:.2f} is degenerate (proposal mis-scaled?)"
```

`W_REF` is a documented reference shared with hw15 (the through-line), checked with loose
`rel/abs` so any correct sampler passes regardless of RNG stream.

---

## 3. `hw16/rubric.md` (interpretation; shared analytic rubric)

Prompts (i)–(ii), each 0–3 on Claim/Evidence/Reasoning/Limits. Specs bundle:
"Interpretation = PASS" needs ≥2 on every dimension; one revise-and-resubmit otherwise.
*Exemplar (i):* states means agree and MCMC covariance is a touch wider (Claim+Evidence),
because Laplace is a Gaussian approximation at the mode while MCMC captures skew (Reasoning),
noting agreement degrades if the chain hasn't mixed (Limits).

---

## 4. Proposed `hw.py` edits (marker-preserving)

Guard the import-time work so the autograder can import cheaply; no logic changes.

```diff
-SAMPLER = MetropolisSampler(X, t, 0.1, 2)
-# ... module-level generate_samples(...) + plotting ...
+if __name__ == "__main__":
+    SAMPLER = MetropolisSampler(X, t, 0.1, 2)
+    # ... existing module-level generate_samples(...) + plotting, indented under __main__ ...
```

Solution markers (`### SOLUTION START/END ###`) and the method/return contract the grader
imports are unchanged. (Exact diff finalized against the real module tail when applied.)

## 5. Alignment & effort

| Objective | Assessed by | Type |
|-----------|-------------|------|
| O1 log-densities | `test_log_likelihood/prior_matches_formula` | autograded |
| O2 acceptance ratio | `test_acceptance_ratio_matches_formula` | autograded |
| O3 run a valid chain | proposal + recovery + covariance + acceptance-band tests | autograded |
| O4 judge the sampler | rubric (i),(ii) | rubric |

**Effort:** roughly unchanged (~2–3h); two short interpretation paragraphs replace nothing
removed, but the `__main__` guard makes local runs faster. Within budget. **Note:** O3's
recovery test needs a few thousand samples — confirm it finishes inside the 10s CI timeout
when applied; if tight, lower `num_samples` to the smallest count that still recovers
`W_REF` within tolerance.
