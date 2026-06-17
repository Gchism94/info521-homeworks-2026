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

> **This draft now covers BOTH halves.** The **code/MC half** (§2, §4a–§4e) was drafted and
> validated earlier and is **unchanged here**. The **written analytic-derivation half** (`hw.tex`,
> LaTeX `%%% Answer %%%` markers, mirroring the hw5 pilot) is added in this additive pass: see
> the new **§4f** (`hw.tex` diff) and the **two-component rubric** in §3. The objective→row map
> (§5) now maps the derivation objective **W1** to a written rubric row (previously unmeasured).

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
- **W1** *Derive* `E[f(X)]` analytically for `X~U(−1,9)` and obtain `18.61`. *(Analyze —
  Written derivation rubric, steps W-A…W-D — see §3)*
- **O1** *Implement* `f` and identify the analytic target. *(Apply — Correctness:
  `test_f_matches_formula`, `test_true_expectation_is_analytic`)*
- **O2** *Draw* i.i.d. samples from `U(−1,9)`. *(Apply — Correctness:
  `test_draw_samples_uniform`, `test_draw_samples_reproducible_but_random`)*
- **O3** *Estimate* `E[f(X)]` by Monte Carlo and show it **recovers the analytic value**.
  *(Analyze — Correctness: `test_mc_recovers_analytic_expectation`,
  `test_mc_estimate_varies_with_seed`, `test_running_expectations_converges`)*
- **O4** *Interpret* the convergence — sampling error, how many samples are "enough", and when
  Monte Carlo fails. *(Evaluate — Interpretation rubric; the autograder cannot check this)*

**3. The task (outcome, not recipe).** *(Written)* Derive `E[f(X)]` analytically for
`X~U(−1,9)`, showing the steps, and arrive at `18.61`. *(Code)* Implement `f`; draw samples
from `U(−1,9)`; estimate `E[f(X)]` and produce the convergence curve, showing the estimate
approaches the analytic value `18.61`.

**4. Allowed methods (scope stated plainly).** **The autograder tests the recovery invariant
— that your estimate converges to the analytic `E[f(X)]` — and that your samples are
`U(−1,9)`, never your specific NumPy calls.** Any correct way to draw uniform samples and
average `f` earns full credit. **Scope:** this assignment *is* Monte Carlo with uniform
sampling — "any approach" means any valid uniform sampler + sample mean, **not** a different
estimator (e.g. quadrature), which the tests are not designed to reward.

**5. How you'll be assessed (criteria shown up front).** Two components (proposed weight
**Written 30% / Code 70%** — see §3, flagged for ratification):
- *Written derivation (30%)* — the per-step rubric in §3 (steps W-A…W-D), each scored on the
  validity of the move; any valid route to `18.61` earns full credit.
- *Code / Monte Carlo (70%, internally 55/35/10)*:
  - *Correctness (55%)* — §2: `f` matches its formula; samples are `U(−1,9)`; the Monte Carlo
    estimate recovers `18.61` within `±0.5` across seeds; **every recovery floor is paired with
    a degeneracy guard** (variance, varies-with-seed, non-flat curve). Thresholds visible in
    `test_hw.py`.
  - *Interpretation (35%)* — the §6 prompt, scored Claim/Evidence/Reasoning/Limits.
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

## 3. `hw6/rubric.md` (NEW — TWO weighted components: Written derivation + Code/MC)

hw6 is a hybrid, so the rubric has **two top-level components** with an inter-component weight.
Full file content in the §4d diff; shipped to students (TILT).

### ⚖️ Proposed inter-component weight — **FLAG FOR RATIFICATION**

> **Proposed: Written derivation 30% / Code-MC 70% of the HW.** Rationale (effort-weighted):
> the analytic derivation is a single polynomial integral (~25–30 min) while the code half —
> implement `f`, the sampler, the estimator, the convergence curve, and the interpretation
> paragraph — is ~1.5–2 h; 30% gives the derivation meaningful weight without overshadowing the
> bulk of the work. **Alternatives to consider:** 25/75 (lighter written) or 35/65 (heavier
> written). **This split is your decision — please ratify or override.**

### 3a. Component A — WRITTEN analytic derivation (proposed 30%) — per-step rubric

Mirrors the hw5 pilot. Enumerate the major logical steps; **each is scored on the validity of
the move, not on matching this key's exact algebra. Any valid route to `18.61` earns full
credit** (e.g. integrating term-by-term, or using the uniform moment formula
`E[X^k] = (b^{k+1}−a^{k+1})/((k+1)(b−a))` + linearity). Tiers 0–3 map to a fraction of each
step's points (3→100%, 2→80%, 1→45%, 0→0%); weights below sum to 30 (HW-level points).

| Step | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
|------|-----|:---:|---------------|----------------|----------------|---|
| **W-A · Setup** | W1 | 7 | writes `E[f(X)] = ∫ f(x)p(x)dx`, states `p(x)=1/(b−a)` on `[a,b]` so the integral reduces to `∫_a^b f/(b−a)` | setup right, support/pdf implicit | wrong pdf or limits but intent | missing |
| **W-B · Antiderivative** | W1 | 8 | integrates term by term: `35x + (3/2)x² − x³ + 0.05x⁴ + 0.002x⁵` | minor coefficient slip | partial / wrong terms | missing |
| **W-C · Evaluate** | W1 | 7 | applies `[·]_a^b` and divides by `(b−a)` correctly (on the student's own antiderivative) | minor slip | sets up but can't evaluate | missing |
| **W-D · Substitute → 18.61** | W1 | 8 | substitutes `a=−1, b=9`, shows the arithmetic to `18.61` | right value, minor arithmetic slip | substitutes but can't finish | missing/incorrect |

**Load-bearing vs. independent.** W-A is **load-bearing** (a wrong pdf/limits caps the
downstream values) but **route-free**. W-B/W-C/W-D form a value-chain, yet each **move** is
gradeable on the student's own previous line — an upstream slip caps the final value, not the
downstream method credit. (No CERL row here: the interpretation layer lives in the code half;
the written half is scored purely on derivation validity.)

### 3b. Component B — CODE / Monte Carlo (proposed 70%) — internally 55/35/10 (unchanged)

| Layer | Weight (of component) | How |
|---|:---:|---|
| **Correctness** | **55%** | machine-verified by `test_hw.py` (§2.5): formula + analytic value + uniform-sampler + recovery + floor-and-guard. Independent → partial credit. |
| **Interpretation** | **35%** | the §6 paragraph, 0–3 on Claim/Evidence/Reasoning/Limits. PASS = ≥2 every dimension. |
| **Process** | **10%** | seeded; `import hw` does no work; convergence plot labeled; runs clean. |

**Effective HW-level weights** (at the proposed 30/70): Written derivation 30% · Code
Correctness 38.5% · Code Interpretation 24.5% · Code Process 7%.

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

### 4d. `rubric.md` — NEW file (TWO components)

```diff
--- /dev/null
+++ b/rubric.md
@@
+# HW6 — Grading rubric (hybrid: written derivation + Monte Carlo code)
+
+Two components. **Proposed inter-component weight: Written derivation 30% / Code-MC 70% of the
+HW — to be ratified by the instructor** (alternatives 25/75 or 35/65). The code component keeps
+the autograded 55/35/10 split (machine-verified correctness + CERL interpretation + process).
+
+## Component A — Written analytic derivation (30%) — per-step rubric
+
+Submitted in `hw.tex`/`hw.pdf` (hard copy ok). Each step is scored on the **validity of the
+move**, not on matching this key's algebra. **Any valid route to `E[f(X)] = 18.61` earns full
+credit** (term-by-term integration, or the uniform-moment formula + linearity). Tiers 0–3 map
+to a fraction of each step's points.
+
+| Step | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
+|------|:---:|---------------|----------------|----------------|---|
+| **W-A · Setup** | 7 | `E[f]=∫f·p`, `p=1/(b−a)` on `[a,b]`, reduces to `(1/(b−a))∫_a^b f` | setup right, support implicit | wrong pdf/limits | missing |
+| **W-B · Antiderivative** | 8 | `35x + (3/2)x² − x³ + 0.05x⁴ + 0.002x⁵` | minor coeff slip | partial | missing |
+| **W-C · Evaluate** | 7 | applies `[·]_a^b` and `/(b−a)` correctly | minor slip | can't evaluate | missing |
+| **W-D · Substitute → 18.61** | 8 | `a=−1, b=9`, arithmetic to `18.61` | minor arithmetic slip | can't finish | missing |
+
+W-A is load-bearing (caps downstream values) but route-free; W-B/W-C/W-D moves are gradeable
+independently on the student's own previous line.
+
+## Component B — Code / Monte Carlo (70%) — autograded 55/35/10
+
+### Correctness (55) — machine-verified
+`pytest test_hw.py`. Independent tests → partial credit; thresholds visible in the file:
+`f` matches its polynomial; `true_expectation` equals the analytic `18.61`; `draw_samples` is
+`U(−1,9)` (support, mean ≈ 4, variance ≈ 8.33, not constant); the Monte Carlo estimate recovers
+`18.61` within `±0.5` across seeds; **every recovery floor is paired with a degeneracy guard**
+(sample variance, varies-with-seed, non-flat convergence curve). Any correct uniform sampler +
+sample mean passes; RNG draw order is never tested.
+
+### Interpretation (35) — Claim / Evidence / Reasoning / Limits (0–3 each)
+The convergence paragraph in `hw.py`. PASS = ≥2 every dimension; else one revise-and-resubmit.
+
+| Dim | 3 | 2 | 1 | 0 |
+|-----|---|---|---|---|
+| **Claim** | states a defensible "samples needed to stabilize" and that the estimate converges to 18.61 | mostly | partial | missing |
+| **Evidence** | cites the curve (where it settles) / the small-N noise / the estimate value | some | vague | none |
+| **Reasoning** | links larger `N` → smaller error (≈ `1/√N`) → tighter estimate | sound | superficial | absent |
+| **Limits** | names a real failure (heavy-tailed integrand, wrong support, correlated samples, single seed) | one weakly | minimal | none |
+
+### Process (10)
+Seeded via `seed=`; `import hw` does no work (drivers `__main__`-guarded); convergence plot
+labeled; notebook runs top-to-bottom.
+
+**LLM pre-grading** may draft per-dimension scores + one-line reasons; a human confirms and is
+final. (LLM pre-grading is weak on the written derivation — a human grades W-A…W-D.)
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

### 4f. `hw.tex` — written-half framing + polished derivation (additive; mirrors hw5)

Two minimal, format-stable edits (per the format note, the full 8-part prose lives in this
`OVERHAUL.md`; `hw.tex` gets only what must be in the document):
**(a)** a TILT prompt line **outside** the `%%% Answer %%%` markers that reveals the target
`E[f(X)] = 18.61` and points to `rubric.md` (retained after the strip);
**(b)** the reference derivation **inside** the markers, polished to earn full marks — name the
assumptions, make each step explicit (setup → antiderivative → evaluate → substitute), show the
substitution arithmetic to `18.61`, and add a reference interpretation line. All inside-marker
content (derivation, result line, figure) is stripped by `make_release`. *(Also fixes the
pre-existing caption nit — "10,000" → the actual convergence description.)*

```diff
--- a/hw.tex
+++ b/hw.tex
@@
 Then, compute a sample-based approximation to this expectation by filling out
 the necessary code in \texttt{hw.py}.
-What is the value you get for the approximation (using all 1000 generated
-samples)?
 Include the generated figure \texttt{sample\_based\_approximation.pdf} in the
-written portion. In the caption for the figure, include a description of the
-trend you see in the plot (you learned how to insert figures with captions in
-\LaTeX{} in HW0).
+written portion, with a caption describing the trend you see.
+
+\bigskip
+
+\noindent\emph{Criteria \& target (shown up front, TILT).} Your derivation should
+arrive at $\mathbf{E}_{p(x)}\{f(X)\} = 18.61$, and your Monte Carlo estimate in
+\texttt{hw.py} should converge to this value. The analytic derivation is graded by
+the per-step rubric in \texttt{rubric.md}: \emph{any} mathematically valid route to
+$18.61$ earns full credit, but you must show each step.

 \subsection*{Solution}
 %%% Answer START %%%
-\ans{%
-\begin{align*}
-\mathbf{E}_{p(x)} \{ 35 + 3x - 3x^2 + 0.2x^3 + 0.01x^4 \} = \int_{-\infty}^{\infty} \left( ... \right) p(x) \, \mathrm{d}x
-\end{align*}
-With $X \sim U(a,b)$, then its pdf is $p(x) = \frac{1}{b-a}$, and the expectation is:
-{\scriptsize
-\begin{align*}
-\int_{a}^{b} \left( ... \right) \frac{1}{b - a} \, \mathrm{d}x & = \frac{1}{b-a}\int_a^b (...) \, \mathrm{d}x \\
-& = \frac{35x + \frac{3}{2}x^2 - \frac{3}{3}x^3 + \frac{0.2}{4}x^4 + \frac{0.01}{5}x^5 \Bigr|_a^b}{b-a} \\
-& = \frac{(35b + ...) - (35a + ...)}{b - a}
-\end{align*}
-}
-With $a = -1$ and $b = 9$, the analytically computed expectation is 18.61.
-\begin{figure}[htbp]
-    \centering
-    \includegraphics[width=0.5\textwidth]{sample_based_approximation.pdf}
-    \caption{Plot of sampling approximation over 10,000; the red line
-    represents the true expected value.}
-\end{figure}
-}
+\ans{%
+\noindent\textbf{Assumptions.} $X \sim \mathcal{U}(a,b)$, so its density is
+$p(x) = \frac{1}{b-a}$ for $x \in [a,b]$ and $0$ otherwise; write
+$f(x) = 35 + 3x - 3x^2 + 0.2x^3 + 0.01x^4$. By the definition of expectation and
+the linearity of integration,
+\begin{align*}
+\mathbf{E}_{p(x)}\{f(X)\}
+&= \int_{-\infty}^{\infty} f(x)\, p(x)\, \mathrm{d}x
+= \int_{a}^{b} f(x)\, \frac{1}{b-a}\, \mathrm{d}x
+= \frac{1}{b-a}\int_{a}^{b} f(x)\, \mathrm{d}x,
+\end{align*}
+since $p(x)=0$ outside $[a,b]$.
+
+\noindent Integrating term by term,
+\begin{align*}
+\int f(x)\,\mathrm{d}x = 35x + \tfrac{3}{2}x^2 - x^3 + 0.05\,x^4 + 0.002\,x^5 + C,
+\end{align*}
+so the expectation is
+\begin{align*}
+\mathbf{E}_{p(x)}\{f(X)\}
+= \frac{\left[\,35x + \tfrac{3}{2}x^2 - x^3 + 0.05x^4 + 0.002x^5\,\right]_{a}^{b}}{b-a}.
+\end{align*}
+
+\noindent Substituting $a=-1$, $b=9$ (so $b-a = 10$):
+\begin{align*}
+\text{at } x=9:&\quad 315 + 121.5 - 729 + 328.05 + 118.098 = 153.648,\\
+\text{at } x=-1:&\quad -35 + 1.5 + 1 + 0.05 - 0.002 = -32.452,\\
+\mathbf{E}_{p(x)}\{f(X)\} &= \frac{153.648 - (-32.452)}{10} = \frac{186.1}{10} = 18.61.
+\end{align*}
+
+\noindent\textbf{Interpretation.} $18.61$ is the exact value the Monte Carlo
+estimate in \texttt{hw.py} approximates; as the sample size grows the sample-based
+approximation (blue curve) converges to this analytic value (red line).
+\begin{figure}[htbp]
+    \centering
+    \includegraphics[width=0.5\textwidth]{sample_based_approximation.pdf}
+    \caption{Sample-based approximation of $\mathbf{E}_{p(x)}\{f(X)\}$ as the number
+    of samples grows; the red line marks the analytic value $18.61$.}
+\end{figure}
+}
 %%% Answer END %%%
```

---

## 5. Objective → check/row map (alignment contract)

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| **W1** derive `E[f(X)]` analytically → 18.61 | Analyze | **Written derivation rubric, steps W-A…W-D** (§3a) | ✅ written rubric |
| **O1** implement `f` / analytic target | Apply | `test_f_matches_formula`, `test_true_expectation_is_analytic` | ✅ autograded |
| **O2** sample `U(−1,9)` | Apply | `test_draw_samples_uniform`, `test_draw_samples_reproducible_but_random` | ✅ autograded |
| **O3** MC estimate recovers analytic | Analyze | `test_mc_recovers_analytic_expectation`, `test_mc_estimate_varies_with_seed`, `test_running_expectations_converges` | ✅ autograded |
| **O4** interpret convergence | Evaluate | Interpretation rubric (CERL) | ✅ rubric |
| *(communication/reproducibility)* | — | Process (10%) | ✅ partly mechanical, partly rubric |

**Every objective now maps to a check or row.** **W1 (the analytic derivation) was previously
unmeasured** — the old 1/0.5/0 gate scored the written part only as "complete"; it now maps to
the per-step Written derivation rubric (§3a). **Flagged as not machine-measurable:** O4 — how
many samples are "enough", the `1/√N` error intuition, and *why/when* Monte Carlo fails are
structurally beyond the autograder (the recovery test confirms *that* it converged at `N`, not
the student's understanding of *why*). That gap is the reason the code interpretation carries
35% (of the code component).

---

## 6. Effort & budget

| Component | Change vs. current |
|-----------|--------------------|
| Code (fill `f`, sampler, estimator) | unchanged work, now in named functions (~1–2 h) |
| Interpretation paragraph | **+~15 min** (new) |
| Analytic derivation (`hw.tex`) | **same student effort** (~25–30 min); only the *grading* changes (gate → per-step rubric) |
| Local iteration | **faster** — `import hw` / `pytest` no longer sample + write a PDF at import |

Net within 5–6 hrs/week. The refactor and the per-step written rubric add structure and better
feedback, **not student effort**; no computation to trim.

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
6. **`make_release` ships `rubric.md`.**

**Written-half pass (this additive round):**

7. **Inter-component weight 30/70 — FLAGGED for ratification (§3).** The HW had no principled
   written-vs-code split; I propose Written 30% / Code 70% (effort-weighted) and explicitly
   leave it as the instructor's decision (alternatives 25/75, 35/65).
8. **W1 was previously unmeasured.** The analytic derivation was only gate-graded; it now maps
   to a per-step rubric row (§3a, §5).
9. **Minimal `hw.tex` edits, mirroring hw5 (LaTeX, not hw9/Typst).** The full 8-part prose stays
   in this `OVERHAUL.md`; `hw.tex` gets only the TILT target line (outside markers) and the
   polished derivation (inside `%%% Answer %%%`). The target `18.61` is revealed in the prompt
   (TILT), while the derivation/result line stays stripped — same approach as hw9.
10. **Code half untouched.** No edits to §2, §4a (`hw.py`), §4b (`test_hw.py`), §4c
    (`README.md`), or §4e (`make_release`); all code-half numbers stand.

---

## 8. Validation numbers

- **Suite:** `7 passed in 0.27s` against the refactored reference (3 runs: 0.25 / 0.24 / 0.27 s).
- **`import hw`:** 0.41–0.55 s (numpy + matplotlib only); **no PDF written at import**.
- **Stripped template:** byte-compiles cleanly (no `SyntaxError`).
- **Mutation test (guards):** frozen sampler → rejected by 4 tests; **hardcoded `18.61` →
  passes the recovery floor but rejected by the varies-with-seed guard**; wrong interval
  `U(0,1)` → rejected by the recovery floor.

**Written-half pass (this round):**
- **`hw.tex` strip check (no compile, per format note):** ran the `make_release` sed on the
  proposed `hw.tex`. **Stripped (absent from release):** assumptions block, "integrating term by
  term", the antiderivative (`0.05x⁴`/`0.002`), the substitution arithmetic (`153.648`, `186.1`),
  the inside result line `= 18.61`, the reference interpretation, `\includegraphics`. **Retained
  (student-facing):** the prompt, the TILT target reveal (`= 18.61`), the `rubric.md` pointer,
  `\subsection*{Solution}`, `\section{Workload}`. Markers balanced (1 START / 1 END); `\ans{`
  absent from the release. **All checks PASS.**
- **Code half unchanged:** §2/§4a/§4b numbers (`7 passed in 0.27s`, `import` 0.41–0.55 s,
  stripped-template compiles, mutation results) are carried over verbatim — not re-touched.

---

## 9. Proposed commit message (when applied — do NOT commit now)

```
hw6 overhaul: two-component rubric (written derivation + MC autograder)

CODE/MC half (stochastic pattern):
- test_hw.py: replace the pinned running-mean RNG-stream check with formula +
  distributional + recovery tests. Closed-form target E[f(X)] = 18.61; recover
  within +/-0.5 at N=20000; every recovery floor paired with a degeneracy guard
  (sample variance, varies-with-seed, non-flat curve). 12-seed sweep; ~0.27s,
  7 passed.
- hw.py: refactor module-level sampling/printing/plotting into seedable functions
  (draw_samples, monte_carlo_expectation, running_expectations) + a __main__ block
  so `import hw` is cheap; add a Required-Interpretation markdown cell. SOLUTION
  markers preserved; f keeps a `...` placeholder so the stripped template compiles.
- README.md: 8-part framing; criteria-up-front specs table (replaces 1/0.5/0).

WRITTEN half (derivation pattern, mirrors hw5):
- hw.tex: wrap the analytic E[f(X)] derivation in the 8-part framing; reveal the
  target 18.61 in the prompt (TILT, outside %%% Answer %%%); polish the reference
  derivation inside the markers (assumptions, explicit antiderivative + evaluation
  + substitution arithmetic to 18.61, reference interpretation line). Strip check
  passes (derivation/result stripped, prompt+target retained).

- rubric.md (new): TWO components — Written derivation (per-step W-A..W-D) +
  Code/MC (55/35/10). Proposed inter-component weight Written 30% / Code 70%,
  FLAGGED for instructor ratification. Objective W1 (derivation), previously
  unmeasured, now maps to a written rubric row.
- make_release: ship rubric.md.

Contract changes from module-level `expectations` to functions; recovery invariant
tested, never the RNG draw order.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
