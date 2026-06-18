# hw1 — Overhaul draft (code-outcome pattern · Jupytext notebook · simple linear regression)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw1 (1-D least-squares: predict the men's 100m
winning time). Matches the **hw3/hw4 code-outcome pilots**. **Draft only — no hw1 files are
modified; the diffs below are proposed, not applied.**

**Split: autograded → 55 / 35 / 10** (repo canon; correctness machine-verified).

> **STEP 0 — classification: CODE-OUTCOME.** The graded artifact is `test_hw.py` importing
> `SimpleLinearModel`. There is a *separate* hard-copy worksheet (deriving the normal equations)
> that the lab then *uses* — that worksheet is a distinct deliverable, graded on paper, **out of
> scope here** (not folded in → this is code-outcome, **not** a type-1 hybrid). The overhaul
> targets the autograded lab.

**Defects fixed** (per the rollout map): magic-constant pins (`w0==36.4164…`, `w1==-0.0133…`);
import-time work (data load, three plots incl. a 3-D loss surface, `train`, `predict`, `print` at
module scope); no graded interpretation; the 1/0.5/0 gate. **Plus a real bug found in the
reference material** (§0 below).

---

## 0. Reference-correctness audit (do not assume the key — hw12 had a wrong one)

Re-derived the closed form independently from `data100m.csv` (N = 27):

| Quantity | Reference / pinned | Re-derived | Verdict |
|----------|--------------------|------------|---------|
| `w0` | `36.41645590250286` | `36.41645590250286` | ✅ exact |
| `w1` | `-0.013330885710960602` | `-0.013330885710960602` | ✅ exact |
| OLS optimality | — | `Σrₙ = -7.8e-14`, `Σrₙxₙ = -1.2e-10` | ✅ both normal equations hold |
| model vs baseline MSE | — | `0.0503` vs `0.2681` (intercept-only) | ✅ healthy floor-AND-guard margin |

**The pinned parameters are correct.** But there is a **bug in the provided `mse_loss`** (used for
the 3-D loss-surface plot, not for training or grading):

```python
return (np.sum(w1*x + w0 - t)**2)/len(x)   # sums residuals, THEN squares
```

This squares the *sum* of residuals instead of summing the *squares*. At the OLS optimum
`Σrₙ ≈ 0`, so this "loss" evaluates to `≈ 2.3e-28` (verified) — and it is zero along an **entire
line** in `(w0, w1)` space, so the plotted surface is a parabolic **trough**, not a bowl with a
unique minimum. That directly contradicts the surrounding narrative ("find the lowest point on the
surface"). **Fix:** `np.sum((w1*x + w0 - t)**2)/len(x)`. (This code is *not* inside a SOLUTION
marker — it is instructor-provided, so the fix ships to students. Flagged in §6.)

---

## 1. Prompt rewritten into the 8-part template (markdown — mirrored into `README.md`, §4b)

**1. Context & purpose.** Your first ML model: fit a straight line by least squares and use it to
predict the 2012 Olympic 100m winning time. This is the 1-D base case of the regression you will
generalize to matrix form (hw2) and to polynomials with cross-validation (hw3).

**2. Learning objectives** (Bloom + the graded row that measures each):
- **O1** *Implement* the least-squares fit so `train` sets `w0, w1` to the closed-form solution.
  *(Apply — Correctness: closed-form, centroid, orthogonality)*
- **O2** *Produce* predictions from the fitted line. *(Apply — Correctness: predict-is-affine)*
- **O3** *Demonstrate* the fit beats a trivial baseline. *(Analyze — Correctness: beats-baseline)*
- **O4** *Interpret* the parameters and the limits of extrapolation. *(Evaluate — Interpretation)*

**3. The task (outcome, not recipe).** Complete `SimpleLinearModel.train` so the fitted line
minimizes the mean squared error, then predict the 2012 time. **Any method that returns the
least-squares fit earns full autograded credit** — the provided closed form, `np.polyfit`, the
normal equations via `np.linalg.lstsq`, etc.

**4. What you may and may not use.** Any NumPy/linear-algebra routine that yields the OLS fit is
allowed; you need not use the provided `xbar/xxbar` scaffold. You may **not** hard-code the two
target numbers — the tests include property checks a constant cannot satisfy.

**5. How you'll be assessed (criteria shown up front — these are the actual tests).**
- *Correctness (55%, autograded, partial credit across 6 independent tests):* closed-form `w0,w1`
  (`rel=1e-3`); line passes through `(x̄, t̄)`; **both normal equations** (`Σr=0`, `Σr·x=0`);
  **beats the intercept-only baseline by ≥2×** (floor-AND-guard); slope negative & physical;
  `predict` is affine and shape-preserving.
- *Interpretation (35%):* the §6 reflection, scored Claim/Evidence/Reasoning/Limits.
- *Process (10%):* notebook runs clean, `import hw` is cheap, plots labeled, docstrings intact.

**6. Required interpretation** (a markdown cell, ~5–8 sentences): state what `w1` means in
seconds/year and what `w0` is; cite your 2012 prediction against the actual 9.63 s; explain **why
the slope is negative**; and give **at least one real limit of extrapolating this linear model**
(e.g. it eventually predicts impossible/negative times; no uncertainty bands; small N; a regime
change like the 1896 outlier).

**7. Going further (optional, ungraded).** Refit excluding the early (pre-1900) games and compare
the 2012 prediction; or add a quadratic term and discuss whether it helps.

**8. Submission & reproducibility.** Deterministic (no RNG → no seed needed). Autograder imports
`SimpleLinearModel` from `hw` and calls `train(x, t)` (sets `.w0`, `.w1`) and `predict(x)` — keep
those signatures. `import hw` must be cheap (driver under `if __name__ == "__main__"`). Run
`pytest` locally. The hard-copy worksheet (normal-equations derivation) is submitted separately.

---

## 2. `hw1/rubric.md` — autograded + CERL (split 55 / 35 / 10)

### 2a. Correctness (55) — independent autograded tests (partial credit by construction)

| Test | Obj | Pts | Checks | Why it admits any valid method |
|------|-----|:---:|--------|-------------------------------|
| `test_closed_form_params` | O1 | 12 | `w0≈36.4165`, `w1≈-0.013331` (`rel=1e-3`) | closed-form scalar — exact with rel headroom |
| `test_passes_through_centroid` | O1 | 8 | `w0 + w1·x̄ ≈ t̄` | a defining property of *every* OLS fit |
| `test_normal_equations_orthogonality` | O1 | 12 | `Σr ≈ 0` **and** `Σr·x ≈ 0` | the two normal equations — the full OLS characterization |
| `test_beats_intercept_only_baseline` | O3 | 10 | `MSE_model ≤ ½·MSE_meanonly` | **floor-AND-guard**: outcome floor + a constant predictor cannot pass |
| `test_slope_sign_and_scale` | O1 | 6 | `w1 < 0`, `-0.05 < w1 < 0` | sign/scale guard against flipped or runaway fits |
| `test_predict_is_affine` | O2 | 7 | `predict(x) ≈ w0+w1·x`, shape preserved | structural — any correct `predict` passes |

**Sum = 55.** Tests are mutually independent: a bug in `predict` does not zero the parameter
tests, and vice versa. **Floor-AND-guard is `test_beats_intercept_only_baseline`** — paired with
the orthogonality property so the trivial `w1=0, w0=t̄` model (which *does* sit on the centroid)
is still rejected.

### 2b. Interpretation (35) — Claim / Evidence / Reasoning / Limits (0–3 each)

The §6 reflection (12 raw → 35%). PASS = ≥2 every dimension. (Shared framework rubric §4.)

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | states `w1` ≈ −0.0133 s/yr (times falling) and the 2012 prediction correctly | mostly | partial | missing |
| **Evidence** | cites the fitted `w0,w1`, the ~9.59 s prediction vs the actual 9.63 s | some numbers | vague | none |
| **Reasoning** | links least-squares slope to the downward trend; why negative | sound | superficial | absent |
| **Limits** | a real extrapolation limit (negative times eventually; no error bars; small N; 1896 outlier) | one weakly | minimal | none |

### 2c. Process (10) — reproducibility & communication

| Sub-dim | Pts | Full credit when… |
|---------|:---:|-------------------|
| Runs clean | 4 | `pytest` green; `import hw` cheap (driver guarded) |
| Figures | 3 | axes labeled, data vs fit distinguishable |
| Hygiene | 3 | provided docstrings intact; no hard-coded answers |

---

## 3. Objective → rubric-row map (alignment contract)

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| **O1** least-squares fit | Apply | Correctness: closed-form + centroid + orthogonality + slope | ✅ |
| **O2** predictions | Apply | Correctness: `test_predict_is_affine` | ✅ |
| **O3** beats a baseline | Analyze | Correctness: `test_beats_intercept_only_baseline` | ✅ |
| **O4** interpret params + limits | Evaluate | **Interpretation** (CERL) | ✅ |
| *(reproducibility/communication)* | — | **Process** | ✅ (cross-cutting, not an O#) |

**Every objective maps to a row; no row is orphaned.** Process is the standard communication layer.

---

## 4. Proposed diffs (per file — NOT applied)

### 4a. `hw.py` — fix `mse_loss`; `__main__`-guard the driver (markers preserved)

The three SOLUTION blocks (`tbar`, `xtbar`, the `w0/w1` formulas) are **unchanged**. Two edits,
both **outside** SOLUTION markers (instructor code → ship to students): fix `mse_loss`, and move
the data-load + matplotlib import + plots + `train`/`predict`/`print` into `main()` called under
`if __name__ == "__main__"`, so `import hw` no longer loads data, imports matplotlib, or renders a
3-D surface.

```diff
--- a/hw.py
+++ b/hw.py
@@ def mse_loss(w0, w1, x, t):
-    return (np.sum(w1*x + w0 - t)**2)/len(x)
+    # Square each residual, then average (the mean squared error).
+    return np.sum((w1*x + w0 - t)**2)/len(x)
@@ (module scope: the data load, the matplotlib import, all plt.* plotting,
@@  the 3-D loss-surface loop, `model = ...; model.train(...)`, the 2012 predict
@@  and print are moved verbatim into a `main()` and run only under __main__)
+def main():
+    from matplotlib import pyplot as plt
+    x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)
+    plt.style.use("ggplot")
+    # ... (existing plots, loss surface, training, prediction, print — unchanged) ...
+    model = SimpleLinearModel()
+    model.train(x, t)
+    print(model.predict(2012))
+
+
+if __name__ == "__main__":
+    main()
```

> **Notebook-format note (judgment call, §6.2).** Guarding the driver in `main()` keeps `import hw`
> cheap for the autograder while still running top-to-bottom in Jupyter (`__name__ == "__main__"`
> in a kernel) and as `python hw.py`. The lighter alternative — guard *only* the matplotlib import
> + the 3-D surface block, leaving the small inline plots per cell — is offered if you prefer to
> preserve the strict per-cell narrative. (Measured: the matplotlib import + surface dominate the
> 0.55 s; see §7.)

### 4b. `README.md` — replace the 1/0.5/0 gate with the 8-part framing + criteria-up-front table

```diff
-# Grading
-- 1 point: Homework is complete and correct (passes all automated correctness
-    tests, feedback PR is not merged, existing docstrings have not been
-    edited or deleted, written component has no errors).
-- 0.5 points: Homework is incomplete or has errors.
-- 0 points: Homework was not submitted on time.
+# Grading (overhauled — specifications-based; full rubric in `rubric.md`)
+
+| Bundle | Weight | Pass when… |
+|--------|:------:|------------|
+| **Correctness** | **55%** | the 6 autograded tests in `test_hw.py` (closed-form params, centroid, both normal equations, beats-baseline, slope sign, affine predict). Any method that yields the OLS fit passes. |
+| **Interpretation** | **35%** | the required reflection cell reaches Proficient+ on Claim/Evidence/Reasoning/Limits. |
+| **Process** | **10%** | notebook runs clean, `import hw` cheap, figures labeled, docstrings intact. |
+
+One revise-and-resubmit per bundle that falls short. (The hard-copy worksheet is graded
+separately.)
```
*(The 8-part Context/Objectives/Task/Allowed/Criteria/Interpretation/Going-further/Submission
prose from §1 is added above the lab instructions.)*

### 4c. `test_hw.py` — replace the two magic-constant pins with the 6-test suite

```diff
--- a/test_hw.py
+++ b/test_hw.py
@@
-def test_model_params():
-    """Test model parameters found using least-squares approach."""
-    x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)
-    model = SimpleLinearModel()
-    model.train(x, t)
-    assert model.w0 == approx(36.41645590250286)
-    assert model.w1 == approx(-0.013330885710960602)
+# (full 6-test suite — see §2a; validated 6/6 against the reference, mutation-tested)
+def _fit():
+    x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)
+    m = SimpleLinearModel(); m.train(x, t); return x, t, m
+
+def test_closed_form_params():
+    _, _, m = _fit()
+    assert m.w0 == approx(36.41645590250286, rel=1e-3)
+    assert m.w1 == approx(-0.013330885710960602, rel=1e-3)
+
+def test_passes_through_centroid():
+    x, t, m = _fit()
+    assert m.w0 + m.w1 * x.mean() == approx(t.mean(), abs=1e-6)
+
+def test_normal_equations_orthogonality():
+    x, t, m = _fit()
+    r = t - m.predict(x)
+    assert np.sum(r) == approx(0.0, abs=1e-6)
+    assert np.dot(r, x) == approx(0.0, abs=1e-4)
+
+def test_beats_intercept_only_baseline():
+    x, t, m = _fit()
+    assert np.mean((t - m.predict(x))**2) <= 0.5 * np.mean((t - t.mean())**2)
+
+def test_slope_sign_and_scale():
+    _, _, m = _fit()
+    assert m.w1 < 0 and -0.05 < m.w1 < 0.0
+
+def test_predict_is_affine():
+    _, _, m = _fit()
+    xq = np.array([1900.0, 1950.0, 2000.0])
+    assert m.predict(xq) == approx(m.w0 + m.w1 * xq)
+    assert m.predict(xq).shape == xq.shape
```

### 4d. `make_release` — ship `rubric.md` (TILT); markers already preserved

```diff
 cp test_hw.py release
 cp README.md release
+cp rubric.md release
```
(The existing `sed '/### SOLUTION START ###/,/### SOLUTION END ###/d'` already strips the three
solution blocks; the `main()` guard and `mse_loss` fix are outside markers and ship intact.)

### 4e. `rubric.md` — NEW file (full content of §2; shipped to students)

Identical to §2a–2c above (autograded table + CERL + Process), prefaced with the recorded split
note (autograded 55/35/10) and the specs-bundle / one-resubmit policy.

---

## 5. Effort & budget

| Component | Change |
|-----------|--------|
| Coding the fit | unchanged (~20–30 min) |
| Reflection cell | **+~15 min** (new) |
| Net | well within 5–6 hrs/week; import-time fix makes the autograder faster |

No busywork added; the 3-D loss-surface plot is retained (now correct) but no longer runs on import.

---

## 6. Judgment calls beyond the spec

1. **`mse_loss` bug fixed** (square-then-sum). It only feeds the loss-surface plot, but the plot
   is qualitatively wrong without it and contradicts the narrative. Fix ships to students. **Flagged
   for confirmation.**
2. **Driver guarded via `main()`** (notebook-format tradeoff above). The lighter "guard only the
   matplotlib/3-D block" alternative is offered.
3. **Worksheet left out of scope** — it is a separate hard-copy deliverable; this overhaul is the
   autograded lab only. (Its normal-equations derivation is the *through-line* the lab consumes.)
4. **Six tests weighted `12/8/12/10/6/7`** = 55; closed-form heaviest, the floor-AND-guard and the
   normal-equations property carry the method-independent credit.
5. **Interpretation as a markdown cell** in the notebook (framework default: prose beside the
   numbers/plots the Evidence dimension cites), not a separate `REFLECTION.md`.
6. **Through-line:** hw1 (1-D) → hw2 (matrix form) → hw3 (polynomial + CV). Noted as the Scope-B
   consolidation candidate; reference values kept consistent.

---

## 7. Validation results (run against the reference `hw.py`)

Environment: repo `.venv` (numpy 2.1, pytest, matplotlib). All numbers measured.

- **Reference key re-derived:** `w0`, `w1` reproduce the pinned values **exactly**; both normal
  equations satisfied (`Σr=-7.8e-14`, `Σr·x=-1.2e-10`). `mse_loss` bug confirmed
  (`2.3e-28 ≈ 0` at the optimum vs the true MSE `0.0503`). ✅
- **New suite vs reference:** **6 passed in 0.04 s.** ✅
- **Import-time fix:** `import hw` **0.550 s → 0.034 s** (16× cheaper); `SimpleLinearModel` still
  importable. ✅
- **Mutation-tested guards** (degenerate models must fail):
  | Injected model | Tests that correctly FAIL |
  |----------------|---------------------------|
  | intercept-only (`w1=0, w0=t̄`) | closed-form, orthogonality, **beats-baseline**, slope-sign |
  | sign-flipped slope | closed-form, orthogonality, **beats-baseline**, slope-sign |
  | broken `predict` (returns `w0`) | predict-affine, orthogonality, **beats-baseline** |
  | reference (correct) | none — all 6 pass ✅ |

  The floor-AND-guard catches the trivial constant model that the centroid property alone would
  miss.

---

## 8. Proposed commit message (when applied — do NOT commit now)

```
hw1 overhaul: outcome/property tests + reflection for 1-D least squares (code-outcome)

- README.md: 8-part prompt + criteria-up-front table; replaces the 1/0.5/0 gate.
  Allowed-approaches: any method yielding the OLS fit passes (polyfit/lstsq/normal
  equations), no hard-coded answers.
- test_hw.py: replace the two magic-constant pins (w0/w1) with 6 independent tests
  (split 55/35/10, Correctness 55 = 12/8/12/10/6/7): closed-form params (rel=1e-3),
  centroid, BOTH normal equations, beats-intercept-only-baseline (floor-AND-guard),
  slope sign/scale, affine predict. Mutation-tested: intercept-only, sign-flipped,
  and broken-predict models all fail the guard; reference passes 6/6 in 0.04s.
- rubric.md (new): autograded 55 + CERL interpretation 35 (params meaning +
  extrapolation limits) + Process 10. Shipped to students (TILT).
- hw.py: fix mse_loss (square-then-sum; the old code zeroed along a line and made
  the 3-D loss surface a trough, not a bowl) and move the data-load/matplotlib/
  plots/train/predict/print driver into main() under `if __name__ == "__main__"`.
  The three SOLUTION blocks (tbar, xtbar, w0/w1) are unchanged; both edits are
  outside the markers (instructor code) so they ship. import hw: 0.55s -> 0.034s.
- make_release: also copies rubric.md (sed solution-strip unchanged).
- through-line: 1-D least squares -> hw2 (matrix form) -> hw3 (polynomial + CV);
  the hard-copy worksheet derivation is the separate deliverable the lab consumes.

Reference math verified: w0/w1 reproduce the pinned values exactly. Autograder:
6 tests, 0.04s wall, import 0.034s.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
