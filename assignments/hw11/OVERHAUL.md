# hw11 — Overhaul draft (HYBRID · mirrors the hw6 two-component template)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw11 (exact Bayesian inference for a coin game).
**Draft only — no hw11 files are modified; the diffs below are proposed, not applied.**

---

## STEP 0 — Classification / decomposition

hw11 has two components; the written part is **LaTeX** (`hw.tex`, `%%% Answer START/END %%%`
markers — confirmed; *not* Typst), so the written pattern mirrors **hw5**.

| Component | What it is | Closest pattern | Notes |
|---|---|---|---|
| **A — Code: exact inference** | `B`, `Beta`, `posterior`, `calculate_marginal_likelihood`, `calculate_probability_of_winning`, `run_scenario` | **code-outcome** (hw3) | **Deterministic** — Beta densities on a fixed grid `r=linspace(0,1,100)`, **no RNG**. So this is *not* the stochastic pattern; **no seed/tolerance sweep applies**. Already `__main__`-guarded (`hw.py:234`). |
| **B — Written: interpret the posteriors** | explain what the priors represent, why prior→posterior shapes change, and why the three scenarios differ | **interpretation, NOT derivation** | ⚠️ **Classification flag:** the task's "written → per-step rubric" assumes a *derivation*. hw11's written half is an **explanation of figures** — there are no derivation steps to score. The correct instrument is **CERL** (the shared analytic rubric), not a per-step rubric. See §3 / judgment call 1. |

**Defects to fix:** (1) `test_hw.py` pins **full 100-element arrays** (`R_PRIOR_*`, `R_POSTERIOR_*`)
— brittle, all-or-nothing; (2) closed-form scalars are pinned (fine, but not paired with
guards); (3) the 1/0.5/0 gate; (4) the written explanation is graded by an informal
"1 point for a reasonable explanation" line (buried *inside* the answer markers, so students
never even see the criterion).

---

## 1. Prompt rewritten into the 8-part template (markdown)

> Authored here; mirrored into `README.md` (§4e). The code interpretation is delivered as the
> **written half** (`hw.tex`), so there is no separate in-notebook interpretation cell.

**1. Context & purpose.** Bayesian inference updates a prior belief with observed data to get a
posterior. Here the conjugate Beta–Binomial model gives the posterior in closed form; you'll
compute it, the marginal likelihood, and a predictive win probability, then read off what the
posteriors *mean*.

**2. Learning objectives** (Bloom verb + the graded check/row each is measured by):
- **O1** *Implement* the Beta function and density. *(Apply — Code Correctness:
  `test_beta_function`, `test_beta_density_valid`)*
- **O2** *Compute* the conjugate posterior. *(Apply/Analyze — Code Correctness:
  `test_posterior_is_conjugate_update`, `test_posterior_mode_recovers_map`,
  `test_posterior_differs_from_prior`)*
- **O3** *Compute* the marginal likelihood and predictive win probability (log-space).
  *(Apply — Code Correctness: `test_marginal_likelihood_values`,
  `test_marginal_likelihood_is_distribution`, `test_probability_of_winning_values`)*
- **O4** *Interpret* how prior strength/location shapes the posterior and why the three
  scenarios differ. *(Evaluate — Written Interpretation rubric, CERL)*

**3. The task (outcome, not recipe).** *(Code)* Implement the Beta/posterior/marginal-likelihood/
win-probability functions; `run_scenario` produces the three prior/posterior plots. *(Written)*
Include the three plots and explain, for each scenario, what the prior encodes, why the
posterior takes its shape, and why the three posteriors differ.

**4. Allowed methods (scope stated plainly).** *(Code)* The autograder tests the **mathematical
objects**, never your code path: `posterior` must equal the conjugate update
`Beta(r, a+y_N, b+N−y_N)` (any correct route passes); the marginal likelihoods over all
outcomes must form a valid distribution; closed-form scalars are checked exactly (`rel=1e-6`).
**Scope:** the prompt restricts imports to `scipy.special` (`gamma`/`loggamma`/`binom`) + numpy;
work in **log-space** for the marginal likelihood/predictive (numerical stability). *(Written)*
**Any correct, well-supported explanation earns full credit** — the rubric scores the quality
of the reasoning, not a specific wording.

**5. How you'll be assessed (criteria shown up front).** Multi-component (proposed
**Code-Correctness 55% / Written-Interpretation 35% / Process 10%** — see §3, flagged):
- *Code Correctness (55%)* — §2 property/identity + floor-AND-guard tests; thresholds visible in
  `test_hw.py`.
- *Written Interpretation (35%, CERL)* — the `hw.tex` explanation, scored
  Claim/Evidence/Reasoning/Limits.
- *Process (10%)* — runs clean, plots generated + captioned, imports respected.

**6. Required interpretation** (in `hw.tex`): for each scenario, state what the prior encodes
(**Claim**), cite the posterior peak location and spread from your plots (**Evidence**), tie the
shape to prior strength vs. the 14/20 evidence (**Reasoning**), and note an assumption/limit —
i.i.d. tosses, correctly-specified prior, small-N or mis-specification risk (**Limits**).

**7. Going further (optional, ungraded).** Vary `y_N` or the prior strength and describe how the
win probability responds; or overlay the posterior predictive for the next 10 tosses.

**8. Submission & reproducibility.** Commit `hw.py` (code), `hw.tex`/`hw.pdf` (the three plots +
captions + explanation). The grader imports `B, Beta, posterior,
calculate_marginal_likelihood, calculate_probability_of_winning, run_scenario` — keep those
names/signatures (`run_scenario(N, y_N, a, b, title, plot_p)` returning
`(r_prior, r_posterior, marginal_likelihood, probability_of_winning)`). Run `pytest test_hw.py`
locally first.

---

## 2. Code component — property/identity + floor-AND-guard tests (no array pins)

Deterministic problem → **no RNG, no seed/tolerance sweep**; exact match kept only for
closed-form scalars (`rel=1e-6`). The 100-element array pins are replaced by the **conjugacy
identity**, **normalization**, and **mode recovery**. Validated: **9 passed in ~0.35 s**.

```python
"""Tests for hw11 — exact Bayesian inference: property/identity + floor-AND-guard.

Deterministic (no RNG): closed-form scalars are pinned with rel headroom; the 100-element
arrays are replaced by the conjugacy identity + normalization + recovery of the mode.
"""
import numpy as np
from pytest import approx
from hw import B, Beta, posterior, calculate_marginal_likelihood, calculate_probability_of_winning, run_scenario

R = np.linspace(0, 1, 100)


# --- B: beta function closed-form + symmetry ---
def test_beta_function():
    assert B(1, 1) == approx(1.0), "B(1,1) = 1"
    assert B(2, 3) == approx(1/12), "B(2,3) = G(2)G(3)/G(5) = 1/12"
    assert B(3, 5) == approx(B(5, 3)), "B is symmetric"


# --- Beta: valid density (uniform at a=b=1, integrates to 1, non-negative) + GUARD not flat ---
def test_beta_density_valid():
    assert Beta(R, 1, 1) == approx(np.ones_like(R)), "Beta(r,1,1) is the uniform density (=1)"
    for a, b in [(2, 2), (5, 2), (1, 3)]:
        dens = Beta(R, a, b)
        assert np.all(dens >= 0), f"Beta(.,{a},{b}) must be non-negative"
        assert np.trapezoid(dens, R) == approx(1.0, abs=2e-2), f"Beta(.,{a},{b}) must integrate to 1"
    assert Beta(R, 5, 2).std() > 0.1, "GUARD: a non-uniform Beta must not be flat"


# --- posterior IS the conjugate Beta update (identity replaces the pinned 100-elt array) ---
def test_posterior_is_conjugate_update():
    N, y_N, a, b = 20, 14, 1, 1
    expected = Beta(R, a + y_N, b + N - y_N)   # Beta(15, 7)
    assert posterior(R, N, y_N, a, b) == approx(expected), \
        "posterior must be the conjugate update Beta(r, a+y_N, b+N-y_N)"
    assert np.trapezoid(posterior(R, N, y_N, a, b), R) == approx(1.0, abs=2e-2), \
        "posterior must integrate to 1"


# --- posterior mode recovers the MAP (meaningful summary, not the full array) + GUARD not flat ---
def test_posterior_mode_recovers_map():
    N, y_N, a, b = 20, 14, 1, 1
    post = posterior(R, N, y_N, a, b)
    map_r = R[np.argmax(post)]
    assert map_r == approx(0.7, abs=0.02), f"MAP for Beta(15,7) is (a-1)/(a+b-2)=0.7, got {map_r:.3f}"
    assert post.max() > 3 * post.mean(), "GUARD: posterior must be peaked, not flat"


# --- GUARD: informative data moves the posterior away from the prior ---
def test_posterior_differs_from_prior():
    N, y_N, a, b = 20, 14, 1, 1
    prior = Beta(R, a, b)
    post = posterior(R, N, y_N, a, b)
    assert not np.allclose(prior, post), "posterior must differ from prior under informative data"


# --- marginal likelihood: closed-form values (FLOOR) ---
def test_marginal_likelihood_values():
    assert calculate_marginal_likelihood(20, 14, 1, 1) == approx(0.04761904761904764, rel=1e-6)
    assert calculate_marginal_likelihood(20, 14, 50, 50) == approx(0.04414512187268132, rel=1e-6)
    assert calculate_marginal_likelihood(20, 14, 5, 1) == approx(0.05759457933370968, rel=1e-6)


# --- GUARD: marginal likelihood over all outcomes y=0..N is a valid distribution (sums to 1) ---
def test_marginal_likelihood_is_distribution():
    for a, b in [(1, 1), (50, 50), (5, 1)]:
        total = sum(calculate_marginal_likelihood(20, y, a, b) for y in range(21))
        assert total == approx(1.0, abs=1e-9), \
            f"marginal likelihoods over y=0..N must sum to 1 (prior a={a},b={b}), got {total:.6f}"


# --- probability of winning: closed-form values (FLOOR) + in [0,1] (GUARD) ---
def test_probability_of_winning_values():
    for (a, b), expected in [((1, 1), 0.4047040093758656), ((50, 50), 0.7586215827278409), ((5, 1), 0.29156872811586365)]:
        p = calculate_probability_of_winning(20, 14, a, b)
        assert p == approx(expected, rel=1e-6), f"P(win) for prior ({a},{b}) should be {expected}"
        assert 0.0 <= p <= 1.0, "P(win) must be a probability in [0,1]"


# --- integration contract: run_scenario returns the documented 4-tuple, wired consistently ---
def test_run_scenario_contract():
    r_prior, r_post, ml, pw = run_scenario(20, 14, 1, 1, "S", False)
    assert len(r_prior) == 100 and len(r_post) == 100, "densities are length-100 grids"
    assert r_post == approx(posterior(R, 20, 14, 1, 1)), "run_scenario posterior must match posterior()"
    assert 0 < ml <= 1 and 0 <= pw <= 1, "marginal likelihood and P(win) must be valid probabilities"
```

### 2.1 Floor-and-guard, verified by mutation

| Degenerate submission | Caught by | Honest note |
|---|---|---|
| `posterior` returns the **prior** (ignores data) | `test_posterior_is_conjugate_update`, `test_posterior_mode_recovers_map`, `test_posterior_differs_from_prior` | mode lands at 0.0, not 0.7 |
| `calculate_marginal_likelihood` returns a **constant** | **value floor** (scenarios 2 & 3 differ) | the sum-to-1 guard alone does **not** catch a `1/21` constant (it coincidentally sums to 1) — the 3-scenario value floor does. The sum-to-1 guard targets a *different* failure: a non-normalized formula (e.g. dropping the binomial coefficient). |
| `calculate_probability_of_winning` returns `0.5` | **value floor** (3 scenarios) | in-range guard alone is insufficient → the value floor carries it |

### 2.2 Budget — measured

`hw.py` is **already `__main__`-guarded**, so no driver/plot runs at import. `import hw` =
**0.36–0.56 s**, essentially the `scipy.special` + `matplotlib` import baseline (0.37 s) — i.e.
**~0 s of assignment work at import**; well within the 10 s CI timeout. Full suite (9 tests) =
**~0.35 s** (`0.33 / 0.38 / 0.40 s`). No `__main__` fix needed (unlike most code HWs).

---

## 3. `hw11/rubric.md` (NEW — multi-component)

### ⚖️ Proposed inter-component weight — **FLAG FOR RATIFICATION**

> **Proposed: Code-Correctness 55% / Written-Interpretation 35% / Process 10%.** Applying the
> recorded hybrid rule: **effort-proportional** (implementing 5 log-space functions ≈ 2–3 h ≫
> writing the ~3-paragraph explanation ≈ 45 min → code-heavy); **primary-objective dominant**
> (the HW *is* "Exact Bayesian Inference" → the inference code is primary); **Bloom-checked**
> (the written explanation is Evaluate-level → a solid 35%); **rounded to 5s**.
>
> Note this **equals the standard autograded 55/35/10** — because hw11's "written" half **is the
> interpretation layer** (delivered in LaTeX instead of notebook markdown), *not* a separate
> derivation as in hw6. So no *new* inter-component weight is invented. **Alternative to
> consider:** **50 / 40 / 10** if you judge the conceptual interpretation to be the intellectual
> core deserving more weight. **Your decision — please ratify or override.**

### 3a. Component A — Code Correctness (proposed 55%) — machine-verified

`pytest test_hw.py` (§2): `B`/`Beta` valid; `posterior` equals the conjugate update + normalized
+ mode at the MAP + differs from prior; marginal likelihood matches the closed-form values
(`rel=1e-6`) **and** sums to 1 over outcomes; win probability matches the closed-form values +
in `[0,1]`; `run_scenario` wired consistently. Independent → partial credit.

### 3b. Component B — Written Interpretation (proposed 35%) — CERL (NOT per-step)

The `hw.tex` explanation of the three figures, scored 0–3 on each dimension. PASS = ≥2 every
dimension; else one revise-and-resubmit. *(Per-step derivation scoring does not apply — this is
an interpretation task, not a derivation; see judgment call 1.)*

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | correctly states what each prior encodes and the posterior it yields | mostly, minor gap | partial | missing/wrong |
| **Evidence** | cites peak locations (≈0.7 / right-of-0.5 / right-of-0.7) and relative spreads from *their* plots | some numbers | vague | none |
| **Reasoning** | explains the posterior as a prior-vs-likelihood (precision-weighted) compromise; why strong priors resist data | sound | superficial | absent/wrong |
| **Limits** | names a real assumption/failure (i.i.d. tosses, mis-specified prior, small N) | one weakly | minimal | none |

### 3c. Process (proposed 10%)

Notebook runs top-to-bottom; the three scenario plots are generated and captioned;
import restrictions respected (`scipy.special` + numpy only). `hw.py` is `__main__`-guarded.

**Effective HW-level weights** (at the proposed 55/35/10): Code Correctness 55% · Written
Interpretation 35% · Process 10%. **LLM pre-grading** may draft CERL scores; a human confirms
and is final.

---

## 4. Proposed unified diffs (per file — NOT applied)

### 4a. `hw.py` — NO change required

The reference `hw.py` already (i) passes every new test in §2 (the conjugacy identity,
normalization, value floors, and sum-to-1 all hold), (ii) is **`__main__`-guarded** so
`import hw` is cheap, and (iii) exposes the exact function/return contract the grader imports.
**No edits, and the `### SOLUTION START/END ###` markers are untouched.** (Confirmed by running
the suite against it — §8.)

### 4b. `test_hw.py` — replaced wholesale (100-element pins → property/identity + floor-AND-guard)

Full contents in §2. Replaces the six array pins (`R_PRIOR_*`, `R_POSTERIOR_*`) and the four
pinned scalars with: closed-form scalar floors (`rel=1e-6`), the conjugacy identity, the
sum-to-1 distribution guard, mode recovery, and differs-from-prior / not-flat / in-range guards.

```diff
--- a/test_hw.py
+++ b/test_hw.py
@@
-from hw import posterior, run_scenario
-import numpy as np
-import pytest
-...
-R_PRIOR_1 = np.array([1.0, 1.0, ... 100 values ...])
-R_POSTERIOR_1 = np.array([... 100 values ...])
-R_PRIOR_2 = np.array([... 100 values ...]); R_POSTERIOR_2 = np.array([...])
-R_PRIOR_3 = np.array([... 100 values ...]); R_POSTERIOR_3 = np.array([...])
-
-@pytest.fixture
-def exercise_results_bayes_coin_game_scenario1():
-    return run_scenario(20, 14, 1, 1, "Scenario 1", False)
-def test_r_prior_scenario_1(...):      assert r_prior == pytest.approx(R_PRIOR_1)
-def test_r_posterior_scenario_1(...):  assert r_posterior == pytest.approx(R_POSTERIOR_1)
-def test_marginal_likelihood_scenario_1(...): assert marginal_likelihood == pytest.approx(0.04761904761904764)
-def test_probability_of_winning_scenario_1(...): assert probability_of_winning == pytest.approx(0.4047040093758656)
-#   ... scenarios 2 and 3 likewise (pinned 100-element arrays + scalars) ...
+# (full contents in OVERHAUL.md §2 — property/identity + floor-AND-guard; no pinned arrays.
+#  Closed-form scalars kept exact at rel=1e-6; 100-elt arrays replaced by the conjugacy
+#  identity, normalization, and mode recovery.)
```

### 4c. `hw.tex` — written-half framing + polished CERL explanation (mirrors hw5)

Two minimal, format-stable edits: **(a)** move the criteria *out* of the answer markers into a
student-facing TILT line (the old "1 point for a reasonable explanation" lived *inside* the
markers, so students never saw it) and state the CERL dimensions + point to `rubric.md`;
**(b)** polish the reference caption *inside* the markers to explicitly cover
Claim/Evidence/Reasoning/**Limits** (the old caption had no Limits). All solution prose stays
inside `%%% Answer %%%`; the prompt + TILT line stay outside (retained after the strip).

```diff
--- a/hw.tex
+++ b/hw.tex
@@
 Then, in your written solution, include these three plots; describe what the priors
 represent, and explain the differences between the priors and posteriors (why do
 they have the shapes they do). Also explain what makes the posteriors between
 the three scenarios not the same.

-%%% Answer START %%%
-\textcolor{RoyalBlue}{Grading: 1 point for a reasonable explanation of what the
-figures represent (as exemplified below).}
-%%% Answer END %%%
+\noindent\emph{How this is graded (shown up front, TILT).} The written explanation is
+scored by the Claim/Evidence/Reasoning/Limits rubric in \texttt{rubric.md}: state what each
+figure shows (Claim), cite the peak locations and spreads from your plots (Evidence), tie the
+posterior shape to prior strength vs.\ the evidence (Reasoning), and note an assumption or
+limit of the analysis (Limits). Any correct, well-supported explanation earns full credit.

 \begin{figure}[htbp]
     \centering
     \includegraphics[width=0.3\textwidth]{Scenario_1.pdf}
     \includegraphics[width=0.3\textwidth]{Scenario_2.pdf}
     \includegraphics[width=0.3\textwidth]{Scenario_3.pdf}
 %%% Answer START %%%
-    \caption{\textcolor{RoyalBlue}{
-        The three figures plot the prior and posterior densities for r under the three
-        different scenarios, but each based on observations of 14 heads ... (original caption) ...
-        }
-    }
+    \caption{\textcolor{RoyalBlue}{
+        \textbf{Claim/Evidence.} The three figures plot prior and posterior densities for $r$,
+        each based on 14 heads ($y_N$) out of 20 tosses ($N$). (a) Scenario 1 uses a uniform
+        prior, so the posterior is data-driven and peaks at $r=14/20=0.7$ with the largest
+        spread (weakest prior). (b) Scenario 2 has a strong $\mathrm{Beta}(50,50)$ prior peaked
+        at $r=0.5$ with small spread; the evidence pulls the posterior right of $0.5$ and widens
+        it only slightly. (c) Scenario 3 has a weak prior leaning toward heads; the posterior
+        shifts to just right of $0.7$ and tightens relative to the prior.
+        \textbf{Reasoning.} The posterior is a precision-weighted compromise between prior and
+        likelihood: a strong prior (large $a+b$) resists the data, while a weak prior lets the
+        14/20 evidence dominate -- which is why the three posteriors differ.
+        \textbf{Limits.} This assumes the tosses are i.i.d.\ Bernoulli and the prior is
+        correctly specified; with very few tosses or a mis-specified prior the posterior (and
+        the win probability) could mislead.
+        }
+    }
     \label{fig:scenarios}
 %%% Answer END %%%
 \end{figure}
```

### 4d. `rubric.md` — NEW file (multi-component)

```diff
--- /dev/null
+++ b/rubric.md
@@
+# HW11 — Grading rubric (hybrid: exact-inference code + written interpretation)
+
+Two components. **Proposed inter-component weight: Code-Correctness 55% / Written-Interpretation
+35% / Process 10% — to be ratified** (this equals the standard autograded split because the
+written half IS the interpretation layer, not a separate derivation; alternative 50/40/10).
+
+## Component A — Code Correctness (55%) — machine-verified
+`pytest test_hw.py`. Independent tests → partial credit; thresholds visible in the file:
+`B`/`Beta` valid (symmetry, uniform at a=b=1, integrates to 1, non-negative); `posterior`
+equals the conjugate update `Beta(r, a+y_N, b+N−y_N)`, is normalized, peaks at the MAP, and
+differs from the prior; marginal likelihood matches the closed-form values (rel=1e-6) **and**
+sums to 1 over outcomes y=0..N; win probability matches the closed-form values and lies in
+[0,1]. Any correct route to the right mathematical objects passes; the implementation path is
+never tested.
+
+## Component B — Written Interpretation (35%) — Claim / Evidence / Reasoning / Limits (0–3 each)
+The `hw.tex` explanation of the three prior/posterior figures. PASS = ≥2 every dimension; else
+one revise-and-resubmit. (Interpretation task → CERL, not a per-step derivation rubric.)
+
+| Dim | 3 | 2 | 1 | 0 |
+|-----|---|---|---|---|
+| **Claim** | states what each prior encodes and the posterior it yields | mostly | partial | missing |
+| **Evidence** | cites peak locations (≈0.7 / right-of-0.5 / right-of-0.7) and spreads from *your* plots | some | vague | none |
+| **Reasoning** | posterior as a prior-vs-likelihood (precision-weighted) compromise; strong priors resist data | sound | superficial | absent |
+| **Limits** | a real assumption/failure (i.i.d. tosses, mis-specified prior, small N) | one weakly | minimal | none |
+
+## Process (10%)
+Notebook runs top-to-bottom; the three plots are generated and captioned; import restrictions
+respected (scipy.special + numpy only); `hw.py` is __main__-guarded.
+
+**LLM pre-grading** may draft CERL scores + one-line reasons; a human confirms and is final.
```

### 4e. `README.md` — 8-part framing + criteria up front (replaces the 1/0.5/0 gate)

```diff
--- a/README.md
+++ b/README.md
@@
-# Grading
-
-- 1 point: Homework is complete and correct
-- 0.5 points: Homework is incomplete or has errors.
-- 0 points: Homework was not submitted on time.
+## How you'll be assessed (criteria shown up front)
+
+| Bundle | Weight | Pass when… |
+|--------|:------:|------------|
+| **Code Correctness** | **55%** | `pytest test_hw.py` green — `B`/`Beta` valid; `posterior` is the conjugate update (normalized, peaked at the MAP); marginal likelihood matches the closed form and sums to 1 over outcomes; win probability matches and is in [0,1]. |
+| **Written Interpretation** | **35%** | the `hw.tex` explanation reaches Proficient+ on every Claim/Evidence/Reasoning/Limits dimension (`rubric.md`). |
+| **Process** | **10%** | runs clean; the three plots generated + captioned; imports respected. |
+
+> Proposed component weight 55/35/10 — see `rubric.md` (flagged for instructor ratification).
+
+**Revision:** Code re-runs on every push; the written interpretation gets one
+revise-and-resubmit. An LLM may draft interpretation scores; a human confirms and is final.
```
*(The two-component "Programming / Written" description and Submission list at the top of the
current `README.md` are kept; only the grading section is replaced.)*

### 4f. `make_release` — ship `rubric.md` to students (TILT)

```diff
--- a/make_release
+++ b/make_release
@@
 cp requirements.txt release
 cp test_hw.py release
 cp README.md release
+cp rubric.md release
```

---

## 5. Objective → check/row map (alignment contract)

| Objective | Bloom | Component | Assessed by | Measurable? |
|-----------|-------|-----------|-------------|:-----------:|
| **O1** Beta function/density | Apply | Code Correctness | `test_beta_function`, `test_beta_density_valid` | ✅ autograded |
| **O2** conjugate posterior | Apply/Analyze | Code Correctness | `test_posterior_is_conjugate_update`, `test_posterior_mode_recovers_map`, `test_posterior_differs_from_prior` | ✅ autograded |
| **O3** marginal likelihood + win prob | Apply | Code Correctness | `test_marginal_likelihood_values`, `test_marginal_likelihood_is_distribution`, `test_probability_of_winning_values` | ✅ autograded |
| **O4** interpret prior→posterior | Evaluate | Written Interpretation | CERL rubric (§3b) | ✅ written rubric |
| *(communication/reproducibility)* | — | Process | Process (10%) | ✅ partly mechanical |

**Every objective maps to a check or row.** **O4 was effectively unmeasured** before (the old
"1 point for a reasonable explanation" gate, hidden inside the answer markers); it now maps to a
structured CERL row. Nothing is unmeasurable; the only structurally-human item is O4 (prose),
which is exactly why it is a rubric row, not a test.

---

## 6. Effort & budget

| Component | Change vs. current |
|-----------|--------------------|
| Code (implement 5 functions) | unchanged (~2–3 h) |
| Written interpretation | **same student effort** (~45 min); only the *grading* changes (hidden gate → visible CERL) |
| Local iteration | unchanged — `hw.py` already `__main__`-guarded; suite ~0.35 s |

Net within 5–6 hrs/week. No `hw.py` refactor and no new computation; the rubric adds structure
and visible criteria, **not student effort**. No busywork to trim.

---

## 7. Judgment calls beyond the spec

1. **Written half is INTERPRETATION, scored by CERL — not a per-step derivation rubric.** The
   task's hybrid template assumes "written → per-step (derivation)". hw11's written part is an
   *explanation of figures* with no derivation steps, so CERL (the shared analytic rubric) is the
   correct instrument. Forcing a per-step rubric here would be a category error. **Flagged.**
2. **Code is code-outcome, not stochastic.** Despite being a *Bayesian* HW, the computation is
   deterministic (Beta on a fixed grid); there is **no RNG**, so no seed/tolerance sweep — the
   floor-and-guard is built from the conjugacy identity, normalization, and value floors instead.
3. **Inter-component weight = standard 55/35/10, flagged.** Unlike hw6 (a genuinely separate
   derivation needing a new 30/70), hw11's written half *is* the interpretation layer, so the
   natural weight is the standard split; alternative 50/40/10 offered. **Flagged for ratification.**
4. **`hw.py` needs no edits.** It already passes the new tests and is `__main__`-guarded; the
   only code-side change is `test_hw.py`. (The brittleness was entirely in the test pins.)
5. **Criteria moved OUT of the answer markers.** The old "1 point" line was *inside* `%%% Answer`
   (stripped → invisible to students); TILT requires criteria be visible, so it moves outside and
   becomes the CERL pointer.
6. **Closed-form scalars kept exact (`rel=1e-6`)** per framework §5, each paired with a structural
   guard (sum-to-1 / in-range); honest caveat (§2.1): the sum-to-1 guard does not catch a `1/21`
   constant — the 3-scenario value floor does.

---

## 8. Validation numbers

- **Code suite:** `9 passed in 0.33s` against the reference `hw.py` (3 runs: 0.33 / 0.38 / 0.40 s).
- **`import hw`:** 0.36–0.56 s — the `scipy.special` + `matplotlib` baseline (0.37 s); ~0 s of
  assignment work at import (already `__main__`-guarded). Within the 10 s CI timeout.
- **Mutation test (guards):** `posterior`→prior rejected by 3 tests; constant marginal likelihood
  rejected by the value floor (scenarios 2 & 3); constant `P(win)=0.5` rejected by the value
  floor. *(Honest: the sum-to-1 guard does not catch a `1/21` constant — the value floor does.)*
- **Written `hw.tex` strip check (no compile, per format note):** ran the `make_release` sed —
  **stripped** (absent from release): the polished caption explanation, the Claim/Evidence/
  Reasoning/Limits prose, `\caption`, the i.i.d. limits line. **Retained** (student-facing): the
  prompt, the TILT criteria line, `Claim/Evidence/Reasoning/Limits`, the `rubric.md` pointer,
  `\includegraphics`, `\section{Workload}`. Markers balanced (1 START / 1 END); braces balanced;
  TILT line outside markers, caption inside. **All checks PASS.**

---

## 9. Proposed commit message (when applied — do NOT commit now)

```
hw11 overhaul: property/guard autograder + CERL interpretation (hybrid)

CODE half (code-outcome; deterministic exact inference):
- test_hw.py: replace the six pinned 100-element arrays (R_PRIOR/POSTERIOR_*)
  and four pinned scalars with property/identity + floor-AND-guard tests:
  conjugacy identity (posterior == Beta(r, a+y_N, b+N-y_N)), normalization,
  mode recovery (MAP=0.7), differs-from-prior; marginal likelihood closed-form
  values (rel=1e-6) + sums-to-1-over-outcomes guard; win-probability values +
  in-[0,1] guard. Independent partial-credit cases. (9 passed, ~0.35s.)
- hw.py: UNCHANGED — already passes the new tests and is __main__-guarded;
  SOLUTION markers and the imported contract untouched.

WRITTEN half (interpretation, mirrors hw5 LaTeX markers):
- hw.tex: move the grading criterion OUT of the answer markers into a visible
  TILT line citing the CERL dimensions + rubric.md; polish the reference caption
  inside %%% Answer %%% to cover Claim/Evidence/Reasoning/Limits (adds the
  missing Limits). Strip check passes (explanation stripped, prompt+criteria
  retained).

- rubric.md (new): TWO components — Code Correctness (55, machine-verified) +
  Written Interpretation (35, CERL) + Process (10). Inter-component weight
  55/35/10 FLAGGED for ratification (alt 50/40/10). Objective O4 (interpretation),
  previously hidden behind a 1/0.5/0 gate, now maps to a CERL row.
- README.md: criteria-up-front specs table (replaces 1/0.5/0).
- make_release: ship rubric.md.

Deterministic HW (no RNG): floor-and-guard from the conjugacy identity +
normalization + value floors, not a seed sweep.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
