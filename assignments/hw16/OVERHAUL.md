# hw16 — Overhaul draft (Scope A pilot · stochastic/MCMC template)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw16 (Metropolis-Hastings MCMC for Bayesian
logistic regression). **Draft only — no hw16 files are modified; the diffs below are
proposed, not applied.** This is the template for the approximate-inference cluster
(hw13/14/15/16 → Unit 5, "ways to the same posterior"): tests check *formulas* and
*distributional recovery* of the stationary distribution, never pinned RNG draws.

**All tolerances, the reference posterior, and the wall-time number below were measured**
against the real `hw.py` over a seed sweep (see §2.1), not guessed.

Real API confirmed in `hw16/hw.py`:
`MetropolisSampler(X, t, proposal_variance, prior_variance, seed=100)` with
`log_likelihood(w)`, `log_prior(w)`, `sample_from_proposal(w)`,
`compute_acceptance_ratio(current, candidate)`, `generate_sample(w)`,
`generate_samples(num_samples) -> list`; module-level `X, t` loaded from `data/`. The grader
imports `MetropolisSampler, X, t`. **Two real problems in the current setup:**
1. `test_generate_sample` / `test_generate_samples` pin the exact accepted draws *and* the
   accept/reject pattern under `seed=100` — coupling the grade to the RNG **call order**
   inside the student's code (a correct sampler that draws in a different order fails).
2. `SAMPLER.generate_samples(5000)` and six `plot_*` calls run at **module scope**, so
   `import hw` does a full 5000-step MCMC + opens figures (slow/fragile under a CI timeout).

> **Point split.** Autograded HW → **Correctness 55 / Interpretation 35 / Process 10** (repo
> canon: correctness is machine-verified; see repo-root `rubric.md`).

---

## 1. Prompt rewritten into the 8-part template

> Replaces the body of `hw16/README.md`; the objectives + interpretation prompts are mirrored
> into markdown cells of `hw.py` (§4b). Full text in the §4 diffs.

**1. Context & purpose.** When a posterior has no closed form, MCMC lets you *sample* from it
and estimate any expectation you want. You'll build the simplest sampler (Metropolis-Hastings)
for a Bayesian logistic-regression posterior and verify that the chain's stationary
distribution **is** that posterior.

**2. Learning objectives** (Bloom verb + the graded check/row each is measured by):
- **O1** *Compute* a numerically stable log-likelihood and log-prior.
  *(Apply — Correctness: `test_log_likelihood_matches_formula`, `test_log_prior_matches_formula`)*
- **O2** *Form* the Metropolis acceptance ratio from those log-densities.
  *(Apply — Correctness: `test_acceptance_ratio_equals_exp_delta_logpost`,
  `test_acceptance_ratio_reversible_and_monotone`)*
- **O3** *Run* a chain whose stationary distribution is the posterior, and recover its
  moments. *(Analyze — Correctness: proposal-distribution, recovery, covariance, and
  degeneracy tests)*
- **O4** *Diagnose* the sampler — convergence/burn-in, mixing/acceptance, autocorrelation,
  and when/why it would fail. *(Evaluate — Interpretation rubric; the autograder cannot
  check this structurally)*

**3. The task (outcome, not recipe).** Implement the sampler and draw a chain for the
posterior over the logistic-regression weights. Show that the burned-in chain recovers the
reference posterior **mean and covariance** within tolerance, and report the acceptance rate.

**4. Allowed methods.** **Any correct sampler whose stationary distribution is the target
posterior earns full outcome credit** — Metropolis-Hastings, a different symmetric proposal,
Gibbs, etc. The autograder tests the **stationary-distribution invariant** (recovered
moments), never your sampler choice or draw order. The assignment ships an MH scaffold, so the
*per-method* unit tests (`sample_from_proposal` is Gaussian, `compute_acceptance_ratio =
exp(Δlog-posterior)`) assume MH; the **recovery/convergence tests on `generate_samples` are
sampler-agnostic** (see the honest limits in §2.3). You must work in **log-space** for
numerical stability.

**5. How you'll be assessed (criteria shown up front).**
- *Correctness (autograded, 55%)* — formula checks for the log-densities and acceptance
  ratio; a burned-in chain recovers the reference posterior mean (`abs ≤ 0.25`) and
  covariance; **every recovery floor is paired with a degeneracy guard** (acceptance band,
  variance floor, mean ≠ prior). Thresholds are visible in `test_hw.py`.
- *Interpretation (rubric, 35%)* — the §6 prompts, scored Claim/Evidence/Reasoning/Limits.
- *Process (10%)* — seeded, **no work at import** (`__main__`-guarded drivers), labeled
  trace/contour plots, runs clean.

**6. Required interpretation** (markdown cells in `hw.py`):
- **I1 — Convergence.** Show evidence the chain converged: pick a burn-in from the trace,
  justify it, and say how mixing/autocorrelation informed the choice.
- **I2 — Failure modes.** Report your acceptance rate; explain how proposal/step-size
  controls it and what a near-0 or near-1 rate would do to the estimate.
- **I3 — Limits.** What does the recovered posterior *not* tell you (finite-sample Monte
  Carlo error, dependence on burn-in, single chain, this dataset only)?

**7. Going further (optional, ungraded).** Sweep the proposal variance; plot acceptance rate
and effective sample size vs. step size and comment on the trade-off.

**8. Submission & reproducibility.** Seed via the `seed=` constructor arg. Guard all
sampling/plotting behind `if __name__ == "__main__":` so importing the module is cheap.
Commit `hw.py` (code + I1–I3 markdown). The method/return contract the grader imports is
unchanged. Run `pytest test_hw.py` locally first.

---

## 2. Autograder rewritten to distributional / convergence tests

### 2.1 Reference posterior and the locked tolerances (measured, not guessed)

The target posterior `p(w) ∝ exp(log_prior(w) + log_likelihood(w))` has no closed form, so the
reference is a **high-accuracy deterministic grid integration** of the unnormalized posterior
(step `0.02` over `[-3, 10]²`), at the canonical test config `proposal_variance=0.1`,
`prior_variance=0.5`:

```
REF_MEAN = [0.97630035, 1.09621848]
REF_COV  = [[ 0.24711961, -0.10095126],
            [-0.10095126,  0.23222917]]     # ref std ≈ [0.497, 0.482]
```

> Note: this corrects the earlier draft's `W_REF ≈ [1.64, 2.00]`, which matched **neither**
> prior variance (the grid gives `[0.976, 1.096]` at σ²=0.5 and `[1.512, 1.728]` at σ²=2.0).
> Verifying against the grid caught it.

**Seed sweep (12 seeds, `N=5000`, burn-in `1000`)** at the canonical config:

| Quantity | Observed over 12 seeds | Locked test threshold | Margin |
|---|---|---|---|
| max abs mean error / component | **0.103** | recover within `abs = 0.25` | 2.4× |
| acceptance rate | **0.640 – 0.665** | guard band `0.05 – 0.95` | wide |
| posterior std (min component) | **0.455** | guard `std > 0.2`; cov diag `> 0.04` | 2.3× |
| ‖posterior mean‖ | **≥ 1.437** | guard `‖mean‖ > 0.5` (≠ prior mean 0) | 2.9× |
| unique-state fraction | **0.64** | guard `unique > 0.1·N` | 6× |

The recovery test uses **fixed seeds 0,1,2** (all inside the swept set), so the run is
deterministic and the "unlucky seed" risk is eliminated at lock time, not left to chance.

### 2.2 Floor-and-guard, verified by mutation

Every recovery floor is paired with a guard that fails degenerate output; I verified the
guards by mutating the sampler:

| Degenerate sampler | Caught by | Observed |
|---|---|---|
| **Frozen** (always returns `[0,0]`) | recovery-mean floor, covariance-PSD, unique-states | mean `[0,0]`; cov not PD; 1 unique state |
| **Prior baseline** (returns i.i.d. prior draws — right shape, wrong target) | recovery-mean floor + `‖mean‖>0.5` guard | mean `[0.015, 0.006]` rejected |
| **Tiny proposal** (`σ²=1e-8`, micro-steps) | variance floor / acceptance band | std ≈ `0.005`, acc ≈ `0.996` |
| **Huge proposal** (`σ²=200`, stuck) | acceptance band / unique-states | acc ≈ `0.002`, 0.2% unique |

No bare threshold a trivial answer could clear.

### 2.3 Honest limits (where this can still be wrong)

- **A wrong sampler could pass a loose check.** A sampler targeting a *slightly* wrong
  posterior (e.g. a subtly mis-scaled prior) could land inside `abs=0.25`. Mitigations: the
  **exact** formula tests on `log_prior`/`log_likelihood` (`rel=1e-9`) pin the densities, and
  the **covariance** recovery test constrains the shape, not just the location. Residual risk
  is pushed onto the interpretation layer (I1/I3).
- **A correct sampler could fail on an unlucky seed** — eliminated here by fixing the recovery
  seeds to ones the 12-seed sweep already passed with ≥2.4× margin. The remaining realistic
  failure is a correct-but-poorly-mixing sampler that needs more burn-in than 1000; the
  generous tolerance absorbs normal mixing variation, and I2 asks the student to report
  exactly this.
- **Sampler-agnostic credit is only at the outcome level.** `test_*_recovers_*` /
  `*_covariance_*` / `*_moves_*` pass for *any* sampler that fills `generate_samples`
  correctly. The per-method tests (`proposal_distribution_*`, `acceptance_ratio_*`) presume
  the shipped MH scaffold; a student who replaced the scaffold with Gibbs would forgo that
  partial credit while still passing the outcome tests. Flagged as a scaffold-vs-outcome
  tension, acceptable because the assignment provides the MH skeleton.

### 2.4 Budget — measured wall time

Drivers/plots are `__main__`-guarded, so `import hw` is **0.36 s** (numpy+matplotlib only; no
MCMC at import). The full suite (10 tests, 5 chains of `N=5000` + 6000 proposal draws) runs in
**≈ 1.5–1.6 s** (pytest-reported: 1.61 / 1.49 / 1.57 s across three runs). Comfortably within
the "few seconds" budget; no need to shrink `N`.

### 2.5 The rewritten `test_hw.py` (replaces the file wholesale)

Validated: **10 passed in 1.61s** against the real (guarded) `hw.py`. Removes the four pinned
checks (`test_sample_from_proposal`, `test_generate_sample`, `test_generate_samples`, and the
magic-constant `test_compute_acceptance_ratio`); keeps the analytic formula checks; adds
distributional/convergence/guard tests.

```python
"""Tests for hw16 — formula checks + distributional/convergence recovery.

No pinned RNG draws. Stochastic behaviour is checked by recovery of the target
posterior and by guards that fail degenerate chains, robust to RNG-stream changes.
"""
import numpy as np
from pytest import approx

from hw import MetropolisSampler, X, t

# Canonical test configuration (mixing is healthy here; see OVERHAUL.md §2).
PROP_VAR, PRIOR_VAR = 0.1, 0.5
N, BURN = 5000, 1000

# High-accuracy reference posterior for PRIOR_VAR=0.5: deterministic grid integration
# of exp(log_prior + log_likelihood), step 0.02 over [-3, 10]^2. (OVERHAUL.md §2.1.)
REF_MEAN = np.array([0.97630035, 1.09621848])
REF_COV = np.array([[0.24711961, -0.10095126],
                    [-0.10095126, 0.23222917]])


def _sampler(seed=0):
    return MetropolisSampler(X, t, PROP_VAR, PRIOR_VAR, seed=seed)


def _chain(seed):
    return np.asarray(_sampler(seed).generate_samples(num_samples=N))


def _accept_rate(chain):
    return np.any(np.diff(chain, axis=0) != 0, axis=1).mean()


# --- O1: log-likelihood equals the Bernoulli-logistic formula (any equivalent impl) ---
def test_log_likelihood_matches_formula():
    s = _sampler()
    for w in (np.array([0.0, 0.0]), np.array([1.0, 2.0]), np.array([4.0, 3.0])):
        p = 1.0 / (1.0 + np.exp(-(X @ w)))
        expected = np.sum(t * np.log(p) + (1 - t) * np.log(1 - p))
        assert s.log_likelihood(w) == approx(expected, rel=1e-9), \
            f"log_likelihood({w}) should equal the logistic log-lik {expected:.6f}"


# --- O1: log-prior equals the diagonal-Gaussian form -(1/2 sigma^2) w.w ---
def test_log_prior_matches_formula():
    sigma2 = 0.25
    s = MetropolisSampler(X, t, PROP_VAR, sigma2, seed=0)
    for w in (np.array([0.0, 0.0]), np.array([-2.0, 3.0]), np.array([1.0, 2.0])):
        expected = -(1.0 / (2.0 * sigma2)) * (w @ w)
        assert s.log_prior(w) == approx(expected, rel=1e-9), \
            f"log_prior({w}) should equal -(1/2sigma^2) w.w = {expected:.6f}"


# --- O2: acceptance ratio = exp(delta log-posterior) (property, not a pinned value) ---
def test_acceptance_ratio_equals_exp_delta_logpost():
    s = _sampler()
    cur, cand = np.array([0.0, 0.0]), np.array([4.0, 3.0])
    log_r = ((s.log_prior(cand) + s.log_likelihood(cand))
             - (s.log_prior(cur) + s.log_likelihood(cur)))
    assert s.compute_acceptance_ratio(cur, cand) == approx(np.exp(log_r), rel=1e-9)


# --- O2: acceptance ratio respects detailed balance (symmetric proposal) ---
def test_acceptance_ratio_reversible_and_monotone():
    s = _sampler()
    a, b = np.array([0.0, 0.0]), np.array([4.0, 3.0])
    r_ab = s.compute_acceptance_ratio(a, b)
    r_ba = s.compute_acceptance_ratio(b, a)
    assert r_ab * r_ba == approx(1.0, rel=1e-9), "r(a->b) * r(b->a) must equal 1"
    assert r_ab > 1.0, "moving to the higher-posterior point should give ratio > 1"
    assert s.compute_acceptance_ratio(a, a) == approx(1.0), "self-move ratio must be 1"


# --- O3: proposal is a Gaussian centred at w with cov sigma^2 I (distributional) ---
def test_proposal_distribution_centered_and_scaled():
    s = _sampler(seed=0)
    w = np.array([1.0, 2.0])
    draws = np.array([s.sample_from_proposal(w) for _ in range(6000)])
    assert draws.shape == (6000, 2), "each proposal must have shape (2,)"
    assert draws.mean(axis=0) == approx(w, abs=0.05), \
        f"proposal mean {draws.mean(axis=0)} should be centered at w={w}"
    cov = np.cov(draws.T)
    assert np.diag(cov) == approx([PROP_VAR, PROP_VAR], rel=0.20), \
        f"proposal variances {np.diag(cov)} should be ~{PROP_VAR}"
    assert abs(cov[0, 1]) < 0.03, "proposal covariance should be (near) diagonal"


def test_proposal_reproducible_under_seed():
    w = np.array([1.0, 2.0])
    a = MetropolisSampler(X, t, PROP_VAR, PRIOR_VAR, seed=123).sample_from_proposal(w)
    b = MetropolisSampler(X, t, PROP_VAR, PRIOR_VAR, seed=123).sample_from_proposal(w)
    assert a == approx(b), "same seed must reproduce the same proposal draw"


# --- O3: a burned-in chain RECOVERS the posterior mean (floor) AND is non-degenerate (guard) ---
def test_chain_recovers_posterior_mean():
    for seed in (0, 1, 2):
        chain = _chain(seed)
        post = chain[BURN:]
        mean = post.mean(axis=0)
        # FLOOR: recovered mean matches the grid reference within a seed-robust tolerance.
        assert mean == approx(REF_MEAN, abs=0.25), \
            f"seed {seed}: posterior mean {mean} should be near reference {REF_MEAN}"
        # GUARD (paired): reject degenerate output a trivial answer could emit.
        rate = _accept_rate(chain)
        assert 0.05 <= rate <= 0.95, \
            f"seed {seed}: acceptance rate {rate:.3f} is degenerate (proposal mis-scaled)"
        assert np.all(post.std(axis=0) > 0.2), \
            f"seed {seed}: posterior std {post.std(axis=0)} collapsed (no exploration)"
        assert np.linalg.norm(mean) > 0.5, \
            f"seed {seed}: mean {mean} matches the prior mean 0 (chain ignored the data)"


# --- O3: covariance recovered, symmetric and PSD (floor) + not collapsed (guard) ---
def test_chain_covariance_recovered_and_psd():
    cov = np.cov(_chain(3)[BURN:].T)
    assert np.allclose(cov, cov.T), "posterior covariance must be symmetric"
    assert np.all(np.linalg.eigvalsh(cov) > 0), "posterior covariance must be positive definite"
    assert np.diag(cov) == approx(np.diag(REF_COV), rel=0.5), \
        f"posterior variances {np.diag(cov)} should be near reference {np.diag(REF_COV)}"
    # GUARD: a frozen/constant chain has ~0 variance.
    assert np.all(np.diag(cov) > 0.04), "covariance collapsed — chain is not exploring"


# --- O3: explicit degeneracy guard (independent partial-credit case) ---
def test_chain_moves_and_is_not_constant():
    chain = _chain(4)
    n_unique = len(np.unique(chain, axis=0))
    assert n_unique > 0.1 * len(chain), \
        f"only {n_unique} unique states in {len(chain)} samples — chain barely moves"
    assert not np.allclose(chain, chain[0]), "chain never left its initial state"


def test_generate_samples_length_and_shape():
    samples = np.asarray(_sampler(seed=7).generate_samples(num_samples=50))
    assert samples.shape == (50, 2), f"expected (50, 2) samples, got {samples.shape}"
```

---

## 3. `hw16/rubric.md` (NEW — autograded split 55/35/10)

Shipped to students (TILT). Interpretation = CERL on **convergence/result reading**, the
layer the autograder structurally can't verify.

| Layer | Weight | How |
|---|:---:|---|
| **Correctness** | **55%** | machine-verified by `test_hw.py` (§2.5): formula checks + recovery + floor-and-guard. Independent tests → partial credit. |
| **Interpretation** | **35%** | I1–I3, each 0–3 on Claim/Evidence/Reasoning/Limits. PASS = ≥2 every dimension. |
| **Process** | **10%** | seeded; `import hw` does no work; trace/contour plots labeled; runs clean. |

Interpretation rubric (full content of the new file is in the §4c diff):

| Dim | 3 | 2 | 1 | 0 |
|---|---|---|---|---|
| **Claim** | states a defensible burn-in + acceptance rate and whether the chain converged | mostly | partial | missing |
| **Evidence** | cites the trace plot / acceptance number / autocorrelation from *their* run | some | vague | none |
| **Reasoning** | links proposal/step-size → acceptance → mixing → MC error | sound | superficial | absent |
| **Limits** | names a real failure (poor mixing, too-small burn-in, single chain, dataset-specific) | one weakly | minimal | none |

---

## 4. Proposed unified diffs (per file — NOT applied)

### 4a. `hw.py` — `__main__`-guard the import-time drivers (no logic change; markers preserved)

Wrap the six module-scope driver/plot statements so `import hw` is cheap. The
`MetropolisSampler` class and every `### SOLUTION START/END ###` block are untouched, and the
imported contract (`MetropolisSampler, X, t`) is unchanged.

```diff
--- a/hw.py
+++ b/hw.py
@@ -64,7 +64,8 @@ def plot_data(X, t) -> tuple[Figure, Axes]:
     plt.tight_layout()
     return fig, axes

-plot_data(X, t)
+if __name__ == "__main__":
+    plot_data(X, t)


 # %%
@@ -230,11 +231,12 @@ class MetropolisSampler:
 # The following uses the sampler to gather 5000 samples with $\sigma_\text{proposal}^2 = 0.1$ and $\sigma_\text{prior}^2 = 0.5$.

 # %%
-# Create an instance of the sampler
-SAMPLER = MetropolisSampler(X, t, 0.1, 2)
-
-# Generate 5000 samples. 
-W_SAMPLES = SAMPLER.generate_samples(5000)
+if __name__ == "__main__":
+    # Create an instance of the sampler
+    SAMPLER = MetropolisSampler(X, t, 0.1, 2)
+
+    # Generate 5000 samples.
+    W_SAMPLES = SAMPLER.generate_samples(5000)
@@ -257,7 +259,8 @@ def plot_w_samples(w_samples: list) -> tuple[Figure, Axes]:
     return fig, axes

 # %%
-plot_w_samples(W_SAMPLES)
+if __name__ == "__main__":
+    plot_w_samples(W_SAMPLES)
@@ -263,7 +266,8 @@
 # If we plot again ...

 # %%
-plot_w_samples(W_SAMPLES[2000:])
+if __name__ == "__main__":
+    plot_w_samples(W_SAMPLES[2000:])
@@ -294,7 +298,8 @@ def plot_w_samples_decision_boundaries(
         axes.plot(x, y, color="k", linewidth=0.5)


-plot_w_samples_decision_boundaries(X, t, W_SAMPLES, 200, 220)
+if __name__ == "__main__":
+    plot_w_samples_decision_boundaries(X, t, W_SAMPLES, 200, 220)
@@ -350,4 +355,5 @@ def plot_w_samples_contours(
     axes.set_xlim((-5, 5))
     axes.set_ylim((-5, 5))
 # %%
-plot_w_samples_contours(X, t, W_SAMPLES, 200, 5000)
+if __name__ == "__main__":
+    plot_w_samples_contours(X, t, W_SAMPLES, 200, 5000)
```

### 4b. `hw.py` — add the Required-Interpretation markdown cell (ships to students)

Appended after the final plot cell; pure comment cell (`# %% [markdown]`), no execution.

```diff
--- a/hw.py
+++ b/hw.py
@@ -355,3 +361,17 @@
 if __name__ == "__main__":
     plot_w_samples_contours(X, t, W_SAMPLES, 200, 5000)
+
+# %% [markdown]
+# ## Required interpretation (answer in the cells below)
+#
+# **I1 — Convergence.** Using the trace/scatter plots above, pick a burn-in and justify
+# it; comment on mixing and autocorrelation (do successive samples look independent?).
+#
+# **I2 — Failure modes.** Report your acceptance rate. Explain how the proposal variance
+# (step size) controls it, and what a near-0 or near-1 acceptance rate would do to your
+# posterior estimate.
+#
+# **I3 — Limits.** What does this recovered posterior *not* tell you? (Monte-Carlo error
+# from a finite chain, sensitivity to burn-in, a single chain vs. several, this dataset.)
+
+# %% [markdown]
+# *Your answers here.*
```

### 4c. `README.md` — 8-part framing + criteria up front (replaces the 1/0.5/0 gate)

```diff
--- a/README.md
+++ b/README.md
@@ -1,20 +1,52 @@
-# README
-
-This repository contains a [Jupytext
-notebook](https://jupytext.readthedocs.io/en/latest/), similar to the ones you
-have seen in previous homeworks.
-
-You will need to fill in the missing code. This will have you complete the
-implementations for Metropolis-Hastings MCMC estimation of the Bayesian logistic
-regression model.
-
-
-### Submission
-
-In order to complete your submission, you will need to commit and push the updated `hw.py` file that contains your code.
-
-# Grading
-
-- 1 point: Homework is complete and correct
-- 0.5 points: Homework is incomplete or has errors.
-- 0 points: Homework was not submitted on time.
+# HW16 — MCMC for Bayesian Logistic Regression
+
+> Overhauled (Scope-A pilot, stochastic/MCMC template). Grading is **specifications-based**;
+> the autograder checks *distributional recovery*, not pinned random draws. Rubric in
+> `rubric.md`.
+
+## 1. Context & purpose
+
+When a posterior has no closed form, MCMC lets you *sample* from it and estimate any
+expectation. You'll build a Metropolis-Hastings sampler for a Bayesian logistic-regression
+posterior and verify that the chain's stationary distribution **is** that posterior.
+
+## 2. Learning objectives
+
+- **O1** Compute a numerically stable log-likelihood and log-prior. *(apply — Correctness)*
+- **O2** Form the Metropolis acceptance ratio from those log-densities. *(apply — Correctness)*
+- **O3** Run a chain whose stationary distribution is the posterior and recover its moments.
+  *(analyze — Correctness)*
+- **O4** Diagnose convergence, mixing, and failure modes. *(evaluate — Interpretation)*
+
+## 3. The task (outcome, not recipe)
+
+Implement the sampler, draw a chain for the posterior over the weights, show the burned-in
+chain recovers the reference posterior mean and covariance within tolerance, and report the
+acceptance rate.
+
+## 4. Allowed methods
+
+**Any correct sampler whose stationary distribution is the target posterior earns full
+outcome credit** — MH, a different symmetric proposal, Gibbs. The autograder tests the
+stationary-distribution invariant (recovered moments), never your sampler choice or draw
+order. Work in **log-space** for numerical stability.
+
+## 5. How you'll be assessed (criteria shown up front)
+
+| Bundle | Weight | Pass when… |
+|--------|:------:|------------|
+| **Correctness** | **55%** | `pytest test_hw.py` green — formula checks for the log-densities and acceptance ratio; a burned-in chain recovers the reference mean (`abs ≤ 0.25`) and covariance; recovery floors paired with degeneracy guards. |
+| **Interpretation** | **35%** | I1–I3 (in `hw.py`) each **Proficient+** on every Claim/Evidence/Reasoning/Limits dimension (`rubric.md`). |
+| **Process** | **10%** | seeded; `import hw` does no work; trace/contour plots labeled; runs clean. |
+
+**Revision:** Correctness re-runs on every push (iterate to green); Interpretation gets one
+revise-and-resubmit. An LLM may pre-draft interpretation scores; a human confirms and is final.
+
+## 6. Submission
+
+Commit and push `hw.py` (your code + the I1–I3 markdown answers). Keep the `seed=` argument.
+Run `pytest test_hw.py` locally before submitting.
```

### 4d. `make_release` — ship `rubric.md` to students (TILT)

```diff
--- a/make_release
+++ b/make_release
@@ -7,6 +7,7 @@ mkdir -p release

 # cp .gitignore release  <-- now handled by create_assignment.sh script
 cp README.md release
+cp rubric.md release

 # Copy code, requirements, and tests, stripping solutions out
 if [ -f hw.py ]; then
```

### 4e. `rubric.md` — NEW file

```diff
--- /dev/null
+++ b/rubric.md
@@ -0,0 +1,34 @@
+# HW16 — Grading rubric (autograded MCMC)
+
+Autograded HW: machine-verified correctness + a human-scored interpretation layer for what
+the autograder structurally cannot check (convergence/result reading). Split **55 / 35 / 10**
+per the repo rule for autograded HWs (see the repo-root `rubric.md`).
+
+## Correctness (55) — machine-verified
+
+`pytest test_hw.py`. Independent tests → partial credit; thresholds visible in the file:
+formula checks for `log_likelihood` / `log_prior` / acceptance ratio; a burned-in chain
+recovers the reference posterior mean (`abs ≤ 0.25`) and covariance; **every recovery floor
+is paired with a degeneracy guard** (acceptance band 0.05–0.95, variance floor, mean ≠ prior,
+unique-state fraction). Any correct sampler that recovers the target passes — sampler choice
+and RNG draw order are never tested.
+
+## Interpretation (35) — Claim / Evidence / Reasoning / Limits (0–3 each)
+
+Prompts I1 (convergence/burn-in/mixing), I2 (acceptance rate & failure modes), I3 (limits of
+the recovered distribution). PASS = ≥2 on every dimension; else one revise-and-resubmit.
+
+| Dim | 3 | 2 | 1 | 0 |
+|-----|---|---|---|---|
+| **Claim** | defensible burn-in + acceptance rate; says whether it converged | mostly | partial | missing |
+| **Evidence** | cites the trace plot / acceptance number / autocorrelation from *their* run | some | vague | none |
+| **Reasoning** | links proposal/step-size → acceptance → mixing → MC error | sound | superficial | absent |
+| **Limits** | names a real failure (poor mixing, small burn-in, single chain, dataset-specific) | one weakly | minimal | none |
+
+## Process (10)
+
+Seeded via `seed=`; `import hw` does no work (drivers `__main__`-guarded); trace/contour
+plots labeled; notebook runs top-to-bottom.
+
+**LLM pre-grading** may draft per-dimension scores + one-line reasons; a human confirms every
+grade and is final.
```

---

## 5. Objective → check/row map (alignment contract)

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| **O1** log-densities | Apply | `test_log_likelihood_matches_formula`, `test_log_prior_matches_formula` | ✅ autograded |
| **O2** acceptance ratio | Apply | `test_acceptance_ratio_equals_exp_delta_logpost`, `..._reversible_and_monotone` | ✅ autograded |
| **O3** valid chain + recovery | Analyze | `test_proposal_distribution_*`, `test_proposal_reproducible`, `test_chain_recovers_posterior_mean`, `test_chain_covariance_recovered_and_psd`, `test_chain_moves_and_is_not_constant`, `test_generate_samples_length_and_shape` | ✅ autograded |
| **O4** diagnose convergence/mixing/failure/limits | Evaluate | Interpretation rubric I1–I3 (CERL) | ✅ rubric |
| *(communication/reproducibility)* | — | Process (10%) | ✅ partly rubric, partly mechanical |

**Every objective maps to a check or row.** **Flagged as not machine-measurable:** O4
(burn-in adequacy, mixing quality, autocorrelation, "would it fail under a different
proposal") — these are *structurally* beyond the autograder; the acceptance-band test is only
a coarse proxy. That gap is the reason the interpretation layer exists and is weighted 35%.

---

## 6. Effort & budget

| Component | Change vs. current |
|-----------|--------------------|
| Implementation (fill the MH methods) | unchanged (~2–3 h) |
| I1–I3 interpretation | **+~20–30 min** (replaces the two vague free-text notes) |
| Local iteration | **faster** — `__main__` guard means `import hw` / `pytest` no longer run a 5000-step chain at import |

Net within the syllabus 5–6 hrs/week; hw16 is a lighter week. No derivation/compute busywork
to trim beyond the import-time guard, which is pure speedup.

---

## 7. Judgment calls beyond `OVERHAUL_FRAMEWORK.md`

1. **Reference via grid integration.** The framework's "recovered moments match analytic
   values" has no analytic posterior here, so I use a deterministic 2-D grid integration as
   the high-accuracy reference (framework §5 explicitly allows "analytic *or* high-accuracy
   reference"). Embedded as constants to keep the suite fast (computing the grid is ~4 s).
2. **Corrected the reference value.** The prior draft's `W_REF ≈ [1.64, 2.0]` matched neither
   prior variance; the grid gives `[0.976, 1.096]` at σ²=0.5. Locked the canonical config to
   `prior_variance=0.5` (tighter posterior, cleaner recovery) and recomputed.
3. **Fixed recovery seeds (0,1,2).** Chosen from the 12-seed sweep so the graded run is
   deterministic; the "unlucky seed" failure is removed at lock time rather than left to RNG.
4. **Two-part `hw.py` edit.** The `__main__` guard (process/budget) and a new markdown
   interpretation cell (collection medium per framework §9 for code HWs). Both outside the
   SOLUTION markers; the contract is unchanged.
5. **`make_release` ships `rubric.md`** (TILT). The current script copies README/hw.py/tests
   but not a rubric.
6. **Scaffold-vs-outcome tension** (named honestly in §2.3): full sampler-agnostic credit is
   only on the recovery/convergence tests; the per-method unit tests assume the MH scaffold.

---

## 8. Proposed commit message (when applied — do NOT commit now)

```
hw16 overhaul: distributional/convergence autograder + MCMC interpretation (S2/S3/S5)

- test_hw.py: replace pinned RNG-draw checks (sample_from_proposal /
  generate_sample / generate_samples / magic-constant acceptance) with
  formula checks + distributional recovery of the posterior. Grid-reference
  mean/cov; recover within abs<=0.25; every recovery floor paired with a
  degeneracy guard (acceptance band, variance floor, mean != prior). Tolerances
  locked over a 12-seed sweep; suite runs ~1.6s. (10 passed.)
- hw.py: guard the 6 module-scope driver/plot calls behind
  `if __name__ == "__main__"` so `import hw` is cheap (0.36s, no MCMC at
  import); add a Required-Interpretation markdown cell (I1 convergence,
  I2 acceptance/failure modes, I3 limits). SOLUTION markers + the imported
  contract (MetropolisSampler, X, t) unchanged.
- README.md: 8-part framing; criteria-up-front specs table (replaces 1/0.5/0).
- rubric.md (new): autograded 55/35/10; CERL interpretation on convergence.
- make_release: ship rubric.md.

Autograded split 55/35/10 per repo canon. Stationary-distribution invariant is
tested, never the sampler choice/draw order.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
