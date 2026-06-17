# hw6 — Overhaul draft (stochastic pattern · mirrors hw16)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw6 (Monte Carlo approximation of an
expectation). Matches the **hw16 stochastic pilot** — distributional/convergence tests,
seeded, floor-and-guard, budget-tuned. **Draft only — no hw6 files are modified; the diffs
below are proposed, not applied.**

**Split: autograded → 55 / 35 / 10** (repo canon; correctness machine-verified).

hw6 is a **hybrid**: code (`hw.py` + `test_hw.py`) computes a sample-based estimate of
`E_{U(-1,9)}[f(X)]`; the written part (`hw.tex`) holds the analytic derivation that gives the
closed-form target. Unlike hw16, the recovery reference is a **closed form** (`18.61`) — no
grid integration needed.

**Two real defects fixed:** (1) `test_expectation_values` **pins the exact running-mean RNG
stream** under `seed=100` (couples the grade to the student's RNG call order); (2) the module
**samples, prints, plots, and writes a PDF at import** — `import hw` runs the whole demo.

> **All tolerances, the target, and the timing below were measured** against a refactored
> reference (seed sweep + mutation tests), not guessed.

---

## 1. Prompt rewritten into the 8-part template (markdown)

> Authored here; mirrored into `README.md` (§4c). The interpretation prompt is added as a
> markdown cell in `hw.py` (§4a). The analytic derivation + figure/caption stay in `hw.tex`.

**1. Context & purpose.** When an expectation has no convenient closed form you can *estimate*
it by averaging the integrand over random samples — Monte Carlo integration. Here you compute
the same `E[f(X)]` two ways (analytic + Monte Carlo) and watch the estimate converge.

**2. Learning objectives** (Bloom verb + the graded check each is measured by):
- **O1** *Implement* `f` and identify the analytic target. *(Apply — Correctness:
  `test_f_matches_formula`, `test_true_expectation_is_analytic`)*
- **O2** *Draw* i.i.d. samples from `U(−1,9)`. *(Apply — Correctness:
  `test_draw_samples_uniform`, `test_draw_samples_reproducible_but_random`)*
- **O3** *Estimate* `E[f(X)]` by Monte Carlo and show it **recovers the analytic value**.
  *(Analyze — Correctness: `test_mc_recovers_analytic_expectation`,
  `test_mc_estimate_varies_with_seed`, `test_running_expectations_converges`)*
- **O4** *Interpret* the convergence — sampling error, how many samples are "enough", and when
  Monte Carlo fails. *(Evaluate — Interpretation rubric; the autograder cannot check this)*

**3. The task (outcome, not recipe).** Implement `f`; draw samples from `U(−1,9)`; estimate
`E[f(X)]` and produce the convergence curve. Show the estimate approaches the analytic value
`18.61`.

**4. Allowed methods (scope stated plainly).** **The autograder tests the recovery invariant
— that your estimate converges to the analytic `E[f(X)]` — and that your samples are
`U(−1,9)`, never your specific NumPy calls.** Any correct way to draw uniform samples and
average `f` earns full credit. **Scope:** this assignment *is* Monte Carlo with uniform
sampling — "any approach" means any valid uniform sampler + sample mean, **not** a different
estimator (e.g. quadrature), which the tests are not designed to reward.

**5. How you'll be assessed (criteria shown up front).**
- *Correctness (autograded, 55%)* — §2: `f` matches its formula; samples are `U(−1,9)`; the
  Monte Carlo estimate recovers `18.61` within `±0.5` across seeds; **every recovery floor is
  paired with a degeneracy guard** (variance, varies-with-seed, non-flat curve). Thresholds
  visible in `test_hw.py`.
- *Interpretation (rubric, 35%)* — the §6 prompt, scored Claim/Evidence/Reasoning/Limits.
- *Process (10%)* — seeded, **no work at import** (`__main__`-guarded), labeled convergence
  plot, runs clean.

**6. Required interpretation** (markdown cell in `hw.py`): one short paragraph on the
**convergence** — from your curve, roughly how many samples are needed before the estimate
stabilizes; why the estimate is noisier at small `N` (Monte Carlo error shrinks like
`1/√N`); and **one** situation where Monte Carlo estimation would struggle (a heavy-tailed
integrand, the wrong sampling support, or correlated samples).

**7. Going further (optional, ungraded).** Estimate the standard error of your estimate from
the sample variance, and check it shrinks like `1/√N` as you increase the sample count.

**8. Submission & reproducibility.** Commit `hw.py` (code + interpretation paragraph),
`hw.tex`/`hw.pdf` (analytic derivation + figure/caption), and
`sample_based_approximation.pdf`. Keep the `seed=` arguments. The grader imports `f`,
`draw_samples`, `monte_carlo_expectation`, `running_expectations`, `true_expectation` — keep
those names/signatures. Run `pytest test_hw.py` locally first.

---

## 2. Autograder — distributional/convergence tests (no pinned draws)

### 2.1 Reference target and locked tolerances (measured)

The target is the **closed-form** analytic expectation, confirmed two ways:

```
E_{U(-1,9)}[f(X)] = (1/(b-a)) * ∫_{-1}^{9} f(x) dx = 18.61   (exact; fine numerical = 18.610000)
Var(f(X)) ≈ 163.4,  std(f(X)) ≈ 12.79
```

**Seed sweep (12 seeds)** of `monte_carlo_expectation(N, seed)`:

| N | std of estimate (predicted) | 12-seed max abs error | chosen? |
|---|---|---|---|
| 1,000 | 0.40 | 0.886 | demo only (too loose to be a floor) |
| **20,000** | **0.13** | **0.202** | **✅ test N** |

Locked test thresholds (recovery uses **fixed seeds 0–4**, all inside the swept set, so the
run is deterministic and the "unlucky seed" risk is removed at lock time):

| Check | Threshold | Margin vs. observed |
|---|---|---|
| recovery floor | `|est − 18.61| ≤ 0.5` at `N=20000` | 2.5× the worst-of-12 error |
| varies-with-seed guard | `std(estimates over 5 seeds) > 0.01` | real sampler std ≈ 0.13 |
| sampler variance guard | `Var(samples) > 1.0` (≈ 8.33 expected) | rejects constant draws |
| sampler support | samples in `[−1, 9]`, mean ≈ 4 | distributional |

### 2.2 Floor-and-guard, verified by mutation

| Degenerate submission | Caught by | Observed |
|---|---|---|
| **Frozen** sampler (constant draws = 4) | variance guard, recovery floor, varies-with-seed, non-flat-curve | est `14.36`, var `0` |
| **Hardcoded** `monte_carlo_expectation → 18.61` | **varies-with-seed guard** (recovery floor *passes* — this is why the guard is needed) | `std=0` across seeds |
| **Wrong interval** `U(0,1)` | recovery floor | est `35.55` |

No bare threshold a trivial answer clears. (The hardcoded-constant case is the canonical
demonstration that the recovery floor **must** be paired with a guard.)

### 2.3 Honest limits (where this can still be wrong)

- **A wrong sampler could pass a loose check.** A sampler with the right mean but a subtly
  wrong shape could match `E[f]` within `±0.5`. Mitigation: the `draw_samples` test pins the
  *distribution* (support `[−1,9]`, variance ≈ 8.33), not just the downstream mean; residual
  risk (correct mean+variance, wrong higher moments) is pushed onto the interpretation layer.
- **A correct sampler could fail on an unlucky seed** — removed by fixing the recovery seeds
  (0–4) to ones the 12-seed sweep already passed with ≥2.5× margin. The varies-with-seed guard
  (`std>0.01`) sits far below a real sampler's `std≈0.13`, so a correct sampler effectively
  never trips it.
- **Method-scoped, stated plainly.** Full credit is for *any correct uniform sampler + sample
  mean*; the tests don't reward (or check) a non-Monte-Carlo estimator. This is narrower than
  hw16's "any sampler with the right stationary distribution" — flagged so "any approach" is
  not oversold.

### 2.4 Budget — measured

`__main__`-guarded drivers → `import hw` = **0.41–0.55 s** (numpy + matplotlib only; no
sampling/plot/savefig at import; **no PDF written at import**). Full suite (7 tests) =
**≈ 0.25 s** (`0.25 / 0.24 / 0.27 s` across three runs). Well within budget.

### 2.5 The rewritten `test_hw.py` (replaces the file wholesale)

Validated: **7 passed in 0.27s** against the refactored reference. Removes the pinned
running-mean checks; adds formula + distributional + recovery + guard tests, each independent
with an actionable message.

```python
"""Tests for hw6 — Monte Carlo expectation: convergence/recovery, not pinned RNG draws.

Stochastic behaviour is checked by recovery of the analytic E[f(X)] and by guards that
reject degenerate output, robust to RNG-stream changes.
"""
import numpy as np
from pytest import approx
from hw import f, draw_samples, monte_carlo_expectation, running_expectations, true_expectation

A, B = -1, 9
ANALYTIC = 18.61            # closed form: (1/(b-a)) * integral_a^b f(x) dx  (written part)
N_TEST = 20_000            # large enough that the recovery floor is tight + seed-robust
TOL = 0.5                  # > 2x the 12-seed max error (0.20) at N_TEST


# --- O1: f matches the polynomial (any equivalent impl), vectorized ---
def test_f_matches_formula():
    x = np.array([-1.0, 0.0, 2.0, 4.0, 9.0])
    expected = 35 + 3*x - 3*x**2 + 0.2*x**3 + 0.01*x**4
    assert f(x) == approx(expected, rel=1e-12), "f(x) must equal 35 + 3x - 3x^2 + 0.2x^3 + 0.01x^4"


# --- O1: the analytic value the student transcribed from the written part ---
def test_true_expectation_is_analytic():
    assert true_expectation == approx(ANALYTIC, rel=1e-3), \
        f"true_expectation should be the analytic E[f(X)] = {ANALYTIC}"


# --- O2: draw_samples is Uniform(-1, 9) (distributional) + GUARD not constant ---
def test_draw_samples_uniform():
    x = draw_samples(5000, seed=0)
    assert x.shape == (5000,), "draw_samples(n) must return n samples"
    assert x.min() >= A and x.max() <= B, f"samples must lie in [{A}, {B}]"
    assert x.mean() == approx((A + B) / 2, abs=0.3), "sample mean should be ~4 for U(-1,9)"
    assert x.var() == approx((B - A) ** 2 / 12, rel=0.2), "sample variance should be ~8.33"
    assert x.var() > 1.0, "GUARD: samples must vary (not a constant/frozen draw)"


def test_draw_samples_reproducible_but_random():
    assert draw_samples(1000, seed=7) == approx(draw_samples(1000, seed=7)), \
        "same seed must reproduce the same draws"
    assert not np.allclose(draw_samples(1000, seed=7), draw_samples(1000, seed=8)), \
        "different seeds must give different draws"


# --- O3: MC estimate RECOVERS the analytic expectation (FLOOR) across a seed sweep ---
def test_mc_recovers_analytic_expectation():
    for seed in range(5):
        est = monte_carlo_expectation(N_TEST, seed=seed)
        assert est == approx(ANALYTIC, abs=TOL), \
            f"seed {seed}: MC estimate {est:.3f} should be near analytic {ANALYTIC} (+/-{TOL})"


# --- O3: GUARD — the estimate must actually vary with the RNG (rejects a hardcoded constant) ---
def test_mc_estimate_varies_with_seed():
    ests = np.array([monte_carlo_expectation(N_TEST, seed=s) for s in range(5)])
    assert ests.std() > 0.01, \
        "GUARD: estimates identical across seeds — output is constant/hardcoded, not sampled"
    assert ests.std() < 5.0, "estimates wildly unstable — estimator is not converging"


# --- O3: convergence curve is well-formed and converges (consistency + GUARD) ---
def test_running_expectations_converges():
    sizes, values = running_expectations(1000, seed=0)
    assert len(sizes) == len(values) and len(values) > 10, "curve arrays must align and be non-trivial"
    assert np.all(np.diff(sizes) > 0), "sample sizes must increase"
    assert abs(values[-1] - ANALYTIC) < 1.5, "the curve should settle near the analytic value"
    assert values.std() > 0.0 and not np.allclose(values, values[0]), \
        "GUARD: a flat curve means the sampler/estimator is degenerate"
```

---

## 3. `hw6/rubric.md` (NEW — autograded split 55/35/10)

Shipped to students (TILT). Interpretation = CERL on **convergence/result reading** — what the
autograder structurally can't verify. Full file in the §4d diff.

| Layer | Weight | How |
|---|:---:|---|
| **Correctness** | **55%** | machine-verified by `test_hw.py` (§2.5): formula + analytic value + uniform-sampler + recovery + floor-and-guard. Independent → partial credit. |
| **Interpretation** | **35%** | the §6 paragraph, 0–3 on Claim/Evidence/Reasoning/Limits. PASS = ≥2 every dimension. |
| **Process** | **10%** | seeded; `import hw` does no work; convergence plot labeled; runs clean. |

---

## 4. Proposed unified diffs (per file — NOT applied)

### 4a. `hw.py` — refactor module script into seedable functions + `__main__`-guard + interpretation cell

The module-level sampling/printing/plotting/`savefig` is replaced by named functions
(`draw_samples`, `monte_carlo_expectation`, `running_expectations`) and a `__main__` block, so
`import hw` is cheap and the recovery invariant is testable. **`### SOLUTION START/END ###`
markers are preserved** (and `f` keeps a `...` placeholder so the stripped template compiles).

```diff
--- a/hw.py
+++ b/hw.py
@@
 # %%
 import numpy as np
 from matplotlib import pyplot as plt
-# %config InlineBackend.figure_format = "retina"
+
+A, B = -1, 9  # support of the uniform density U(a, b)

-# %% [markdown]
-# Then, define the function `f` ...
-
-# %%
 def f(x):
     ...
     ### YOUR CODE HERE ###
     ### SOLUTION START ###
     return 35 + 3*x - 3*(x**2) + 0.2*(x**3) + 0.01*(x**4)
     ### SOLUTION END ###

-
-# %%
-# Set the random seed to 100 (you learned how to do this in HW3).
-
-### YOUR CODE HERE ###
-### SOLUTION START ###
-rng = np.random.default_rng(100)
-### SOLUTION END ###
-
-# %%
-# Next, sample 1000 values from U(-1, 9) ...  Store the array ... in `xs`.
-### YOUR CODE HERE ###
-### SOLUTION START ###
-xs = rng.uniform(low=-1, high=9, size=1000)
-### SOLUTION END ###
-
-# Construct an array ... apply `f` ... Store ... in `vals`. ... (vectorized!)
-### YOUR CODE HERE ###
-### SOLUTION START ###
-vals = f(xs)
-### SOLUTION END ###
-
-# Create an array to store the sizes of the subsets of samples
-sample_subset_sizes = np.arange(1, xs.shape[0], 10)
-
-# Create an array to store expectations
-expectations = np.zeros((sample_subset_sizes.shape[0]))
-
-# ... loop computes approximate expectations for each subset size ...
-for i in range(sample_subset_sizes.shape[0]):
-    expectations[i] = vals[0:sample_subset_sizes[i]].mean()
-
-# Print the approximate expectation computed using all 1000 samples.
-print("Approximate expectation using 1000 samples: ", expectations[-1])
-
-# %%
-plt.plot(sample_subset_sizes, expectations)
-
-# The true, analytic result of the expected value ...
-### YOUR CODE HERE ###
-### SOLUTION START ###
-true_expectation = 18.61
-### SOLUTION END ###
-
-# Plot the approximate expectations
-plt.plot(
-    np.array([sample_subset_sizes[0], sample_subset_sizes[-1]]),
-    np.array([true_expectation, true_expectation]), color='r'
-)
-plt.xlabel('Sample size')
-plt.ylabel('Approximate expectation')
-plt.title('Evolution of expectation of $f(x)$')
-plt.savefig("sample_based_approximation.pdf")
+
+def draw_samples(n, seed=100):
+    """Draw n i.i.d. samples from U(-1, 9)."""
+    rng = np.random.default_rng(seed)
+    ### YOUR CODE HERE ###
+    ### SOLUTION START ###
+    return rng.uniform(low=A, high=B, size=n)
+    ### SOLUTION END ###
+
+
+def monte_carlo_expectation(n=1000, seed=100):
+    """Sample-based approximation to E_{U(-1,9)}[f(X)] (FCML Eq. 2.23)."""
+    ### YOUR CODE HERE ###
+    ### SOLUTION START ###
+    return float(f(draw_samples(n, seed)).mean())
+    ### SOLUTION END ###
+
+
+def running_expectations(n=1000, seed=100, step=10):
+    """Running MC estimate as the sample size grows 1..n (for the convergence plot)."""
+    xs = draw_samples(n, seed)
+    vals = f(xs)
+    sizes = np.arange(1, n, step)
+    ### YOUR CODE HERE ###
+    ### SOLUTION START ###
+    values = np.array([vals[:k].mean() for k in sizes])
+    ### SOLUTION END ###
+    return sizes, values
+
+
+# The analytic expectation from the written part of this homework.
+### YOUR CODE HERE ###
+### SOLUTION START ###
+true_expectation = 18.61
+### SOLUTION END ###
+
+
+# %% [markdown]
+# ## Required interpretation (answer in the cell below)
+#
+# In one short paragraph: from your convergence curve, roughly how many samples are
+# needed before the estimate stabilizes? Why is the estimate noisier at small `N`
+# (the Monte-Carlo error shrinks like $1/\sqrt{N}$)? Name one situation where Monte
+# Carlo estimation would struggle — a heavy-tailed integrand, the wrong sampling
+# support, or correlated samples.
+#
+# *Your answer here.*
+
+
+if __name__ == "__main__":
+    print("Approximate expectation using 1000 samples:", monte_carlo_expectation(1000))
+    sizes, values = running_expectations(1000)
+    plt.plot(sizes, values)
+    plt.plot([sizes[0], sizes[-1]], [true_expectation, true_expectation], color="r")
+    plt.xlabel("Sample size")
+    plt.ylabel("Approximate expectation")
+    plt.title("Evolution of expectation of $f(x)$")
+    plt.savefig("sample_based_approximation.pdf")
```

### 4b. `test_hw.py` — replaced wholesale by §2.5 (pinned RNG stream → distributional/recovery)

```diff
--- a/test_hw.py
+++ b/test_hw.py
@@
-"""Tests for the homework."""
-
-from pytest import approx
-from hw import expectations
-
-
-def test_expectation_values():
-    """Test model parameters found using least-squares approach."""
-    assert expectations[0:10] == approx([3.57855833, 16.35364788, ... ])
-    assert expectations[-1] == approx(17.713951811257257)
+# (full contents in OVERHAUL.md §2.5 — formula + distributional + recovery + guards)
```

### 4c. `README.md` — 8-part framing + criteria up front (replaces the 1/0.5/0 gate)

```diff
--- a/README.md
+++ b/README.md
@@
-# README
-
-## Instructions
-...
-# Grading
-
-- 1 point: Homework is complete and correct (code passes all automated
-  correctness tests, PR is not merged, existing docstrings have not been
-  edited or deleted).
-- 0.5 points: Homework is incomplete or has errors.
-- 0 points: Homework was not submitted on time.
-...
+# HW6 — Monte Carlo Estimation of an Expectation
+
+> Overhauled (stochastic pattern). The autograder checks *distributional recovery* of the
+> analytic expectation, not pinned random draws. Specifications-based; rubric in `rubric.md`.
+
+## 1. Context & purpose
+Estimate an expectation by averaging the integrand over random samples (Monte Carlo), and
+watch it converge to the analytic value you derive by hand.
+
+## 2. Learning objectives
+- **O1** Implement `f` and identify the analytic target. *(apply — Correctness)*
+- **O2** Draw i.i.d. samples from `U(−1,9)`. *(apply — Correctness)*
+- **O3** Estimate `E[f(X)]` and show it recovers the analytic value. *(analyze — Correctness)*
+- **O4** Interpret convergence and Monte-Carlo error. *(evaluate — Interpretation)*
+
+## 3. The task (outcome, not recipe)
+Implement `f`, sample from `U(−1,9)`, estimate `E[f(X)]`, and produce the convergence curve;
+show the estimate approaches the analytic value `18.61`.
+
+## 4. Allowed methods
+The autograder tests the **recovery invariant** (your estimate → the analytic `E[f(X)]`) and
+that your samples are `U(−1,9)` — never your specific NumPy calls. **Scope:** this assignment
+*is* Monte Carlo with uniform sampling; "any approach" means any valid uniform sampler + sample
+mean, not a different estimator.
+
+## 5. How you'll be assessed (criteria shown up front)
+| Bundle | Weight | Pass when… |
+|--------|:------:|------------|
+| **Correctness** | **55%** | `pytest test_hw.py` green — `f` matches its formula; samples are `U(−1,9)`; the MC estimate recovers `18.61` within `±0.5` across seeds; recovery floors paired with degeneracy guards. |
+| **Interpretation** | **35%** | the paragraph in `hw.py` reaches Proficient+ on every Claim/Evidence/Reasoning/Limits dimension (`rubric.md`). |
+| **Process** | **10%** | seeded; `import hw` does no work; convergence plot labeled; runs clean. |
+
+**Revision:** Correctness re-runs on every push; Interpretation gets one revise-and-resubmit.
+
+## 6. Submission
+Commit `hw.py` (code + interpretation), `hw.tex`/`hw.pdf` (analytic derivation + figure and
+caption), and `sample_based_approximation.pdf`. Keep the `seed=` arguments. Run the tests
+locally first.
```

### 4d. `rubric.md` — NEW file

```diff
--- /dev/null
+++ b/rubric.md
@@
+# HW6 — Grading rubric (Monte Carlo expectation)
+
+Autograded HW: machine-verified correctness + a human-scored interpretation layer for what the
+autograder structurally cannot check (convergence/result reading). Split **55 / 35 / 10** per
+the repo rule for autograded HWs (see the repo-root `rubric.md`).
+
+## Correctness (55) — machine-verified
+
+`pytest test_hw.py`. Independent tests → partial credit; thresholds visible in the file:
+`f` matches its polynomial; `true_expectation` equals the analytic `18.61`; `draw_samples` is
+`U(−1,9)` (support, mean ≈ 4, variance ≈ 8.33, not constant); the Monte Carlo estimate recovers
+`18.61` within `±0.5` across seeds; **every recovery floor is paired with a degeneracy guard**
+(sample variance, varies-with-seed, non-flat convergence curve). Any correct uniform sampler +
+sample mean passes; RNG draw order is never tested.
+
+## Interpretation (35) — Claim / Evidence / Reasoning / Limits (0–3 each)
+
+The convergence paragraph in `hw.py`. PASS = ≥2 every dimension; else one revise-and-resubmit.
+
+| Dim | 3 | 2 | 1 | 0 |
+|-----|---|---|---|---|
+| **Claim** | states a defensible "samples needed to stabilize" and that the estimate converges to 18.61 | mostly | partial | missing |
+| **Evidence** | cites the curve (where it settles) / the small-N noise / the estimate value | some | vague | none |
+| **Reasoning** | links larger `N` → smaller error (≈ `1/√N`) → tighter estimate | sound | superficial | absent |
+| **Limits** | names a real failure (heavy-tailed integrand, wrong support, correlated samples, single seed) | one weakly | minimal | none |
+
+## Process (10)
+
+Seeded via `seed=`; `import hw` does no work (drivers `__main__`-guarded); convergence plot
+labeled; notebook runs top-to-bottom.
+
+**LLM pre-grading** may draft per-dimension scores + one-line reasons; a human confirms and is
+final.
```

### 4e. `make_release` — ship `rubric.md` to students (TILT)

```diff
--- a/make_release
+++ b/make_release
@@
 cp requirements.txt release
 cp test_hw.py release
 cp README.md release
+cp rubric.md release
```

> **`hw.tex` left unchanged.** The analytic derivation (`18.61`) and the figure/caption are the
> written part and already earn their marks; they fold into the hybrid grade. *(Minor
> pre-existing nit, not fixed here: the figure caption says "over 10,000" while the plot uses
> 1000 samples.)*

---

## 5. Objective → check/row map (alignment contract)

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| **O1** implement `f` / analytic target | Apply | `test_f_matches_formula`, `test_true_expectation_is_analytic` | ✅ autograded |
| **O2** sample `U(−1,9)` | Apply | `test_draw_samples_uniform`, `test_draw_samples_reproducible_but_random` | ✅ autograded |
| **O3** MC estimate recovers analytic | Analyze | `test_mc_recovers_analytic_expectation`, `test_mc_estimate_varies_with_seed`, `test_running_expectations_converges` | ✅ autograded |
| **O4** interpret convergence | Evaluate | Interpretation rubric (CERL) | ✅ rubric |
| *(communication/reproducibility)* | — | Process (10%) | ✅ partly mechanical, partly rubric |

**Every objective maps to a check or row.** **Flagged as not machine-measurable:** O4 — how
many samples are "enough", the `1/√N` error intuition, and *why/when* Monte Carlo fails are
structurally beyond the autograder (the recovery test confirms *that* it converged at `N`, not
the student's understanding of *why*). That gap is the reason interpretation carries 35%.

---

## 6. Effort & budget

| Component | Change vs. current |
|-----------|--------------------|
| Code (fill `f`, sampler, estimator) | unchanged work, now in named functions (~1–2 h) |
| Interpretation paragraph | **+~15 min** (new) |
| Analytic derivation (`hw.tex`) | unchanged |
| Local iteration | **faster** — `import hw` / `pytest` no longer sample + write a PDF at import |

Net within 5–6 hrs/week. The refactor adds structure, not student effort; no computation to
trim.

---

## 7. Judgment calls beyond the spec

1. **Refactor to seedable functions (required contract change).** The grader's contract moves
   from the module-level array `expectations` to functions `f`, `draw_samples`,
   `monte_carlo_expectation`, `running_expectations`, `true_expectation`. This is what makes the
   recovery invariant testable and the import cheap (the analogue of hw16's `run_K_fold_cv`
   return change). Documented as the one required contract change.
2. **Closed-form target used directly.** Unlike hw16 (grid integration), hw6 has an analytic
   `E[f(X)] = 18.61`, so the recovery reference is exact — no reference computation in the suite.
3. **Test N (20,000) ≠ demo N (1,000).** The recovery test picks its own larger N for a tight,
   seed-robust floor; the convergence demo/plot keeps 1,000 (pedagogical). Mirrors hw16.
4. **Kept a `...` placeholder in `f`** so the solution-stripped student template still compiles
   (matches the original's defensive pattern; verified by byte-compiling the stripped file).
5. **`true_expectation` kept as a SOLUTION-marked name and tested ≈ 18.61** — a closed-form
   floor that ties the code to the written analytic result (hybrid coherence).
6. **`hw.tex` untouched; `make_release` ships `rubric.md`.**

---

## 8. Validation numbers

- **Suite:** `7 passed in 0.27s` against the refactored reference (3 runs: 0.25 / 0.24 / 0.27 s).
- **`import hw`:** 0.41–0.55 s (numpy + matplotlib only); **no PDF written at import**.
- **Stripped template:** byte-compiles cleanly (no `SyntaxError`).
- **Mutation test (guards):** frozen sampler → rejected by 4 tests; **hardcoded `18.61` →
  passes the recovery floor but rejected by the varies-with-seed guard**; wrong interval
  `U(0,1)` → rejected by the recovery floor.

---

## 9. Proposed commit message (when applied — do NOT commit now)

```
hw6 overhaul: distributional/recovery autograder + MC interpretation (stochastic)

- test_hw.py: replace the pinned running-mean RNG-stream check with formula +
  distributional + recovery tests. Closed-form target E[f(X)] = 18.61; recover
  within +/-0.5 at N=20000; every recovery floor paired with a degeneracy guard
  (sample variance, varies-with-seed, non-flat curve). Tolerances locked over a
  12-seed sweep; suite ~0.27s. (7 passed.)
- hw.py: refactor the module-level sampling/printing/plotting into seedable
  functions (draw_samples, monte_carlo_expectation, running_expectations) and a
  __main__ block so `import hw` is cheap (no sampling/savefig at import); add a
  Required-Interpretation markdown cell (convergence, 1/sqrt(N) error, failure
  modes). SOLUTION markers preserved; f keeps a `...` placeholder so the stripped
  template compiles.
- README.md: 8-part framing; criteria-up-front specs table (replaces 1/0.5/0).
- rubric.md (new): autograded 55/35/10; CERL interpretation on convergence.
- make_release: ship rubric.md.

Contract changes from module-level `expectations` to functions. Recovery
invariant tested, never the RNG draw order. hw.tex (analytic derivation) unchanged.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
