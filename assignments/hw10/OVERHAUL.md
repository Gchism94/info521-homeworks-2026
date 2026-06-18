# hw10 — Overhaul draft (HYBRID type-2 · code predictive-variance + caption interpretation)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw10 (predictive variance / error bars). The code
generates the plots; the `hw.tex` captions **interpret those plots** → **hw11 type-2 hybrid**
(code + interpretation of its own output), a single autograded HW with the captions folded into the
Interpretation rubric. **Draft only — diffs proposed, not applied.**

**Split: autograded → 55 / 35 / 10** (type-2: captions = the Interpretation 35 layer).

> **STEP 0 — classification: HYBRID type-2.** Not two separate deliverables (type-1/hw6) — the
> written captions describe/contrast the *figures the code produces*. So this is code-outcome with
> the interpretation folded in (hw11 pattern), one split.

**Defects fixed:** magic-constant pins on closed-form quantities; **a real `sigma_sq` normalization
bug** (§0); heavy import-time work (matplotlib + RNG + **three loops writing 12 PDFs to `images/`**,
plus a numerical RuntimeWarning); 1/0.5/0 gate; ungraded captions.

---

## 0. Reference-correctness audit (do not assume the key — hw12 had a wrong one)

Re-derived the test quantities independently:

| Quantity | Pinned | `/global N=40` (current) | `/n_train` (correct MLE) | Verdict |
|----------|--------|--------------------------|--------------------------|---------|
| `cov_w` (order 1, x=[1,2,3]) | `[[0.0533,−0.0229],[−0.0229,0.0114]]` | matches pin | `[[0.711,−0.305],…]` | ⚠️ pin embeds the bug |
| `predictive_variance(0.5)` | `0.033335027` | `0.033335027` | `0.444467` | ⚠️ pin embeds the bug |

**The pinned values bake in a bug.** `train` computes
`sigma_sq = (1/N)·(tᵀt − tᵀXw)` using the **module-global `N=40`**, not the actual training-set
size. The MLE noise variance is `RSS/n_train`; even in the main notebook the model trains on the
gap-removed set (~31 points), so `/40` is wrong there too. The test (3 points) divides by 40 → off
by ~13×. **Fix:** `sigma_sq = (1/X.shape[0])·(…)` — correct MLE, and it removes the global-`N`
coupling (needed to guard the driver cleanly). **PENDING-RATIFICATION** (changes the notebook's
error-bar magnitudes, but only by a positive scalar — the *qualitative* captions stay valid).

The graded **relationships** are bug-agnostic and verified: `cov_w == sigma_sq·inv(XᵀX)` (PSD),
`predictive_variance(x) == diag(X_new·cov_w·X_newᵀ) ≥ 0`. The tests target these, not the
bug-tainted absolute value.

> **Numerical note (not graded, flagged):** importing the original `hw.py` emits
> `RuntimeWarning: covariance is not symmetric positive-semidefinite` — the order-9 `inv(XᵀX)` is
> ill-conditioned (Vandermonde, like hw2). It feeds only the `sampled_ws` plot. Left as-is (fixing
> needs centering/scaling `x` — scope creep); it is a great *interpretation* talking point and the
> PSD test deliberately uses a low order.

---

## 1. Prompt rewritten into the 8-part template (markdown → `README.md`)

**1. Context & purpose.** Predictive variance turns a point estimate into *error bars*. You
implement the closed-form parameter covariance and predictive variance, then read off — from the
plots — how uncertainty grows where data is sparse and how model order trades bias for variance.

**2. Learning objectives** (Bloom + graded row):
- **O1** *Implement* `compute_cov_w` = `σ̂²(XᵀX)⁻¹`. *(Apply — Correctness: cov_w tests)*
- **O2** *Implement* the vectorized `predictive_variance`. *(Apply — Correctness: predictive-variance tests)*
- **O3** *Demonstrate* variance grows in the data gap / at the edges. *(Analyze — Correctness:
  `variance_larger_in_gap`)*
- **O4** *Interpret* the three figures (variance vs. order, gap effect, overfitting). *(Evaluate —
  Interpretation: the captions)*

**3. The task.** Fill `compute_cov_w` and `predictive_variance`; generate the three figure sets;
write the three captions. **Any correct vectorized implementation passes.**

**4. What you may / may not use.** Any NumPy linear algebra; `predictive_variance` must be
vectorized (return one variance per input). No hard-coded numbers.

**5. How you'll be assessed.** §2 — autograded property tests (55), caption CERL (35), process (10).

**6. Required interpretation.** The three `hw.tex` captions (already prompted there): what the
error bars/sampled functions/sampled datasets show, how they contrast across orders, and the effect
of removing `2.5 ≤ x ≤ 4.5`. Scored Claim/Evidence/Reasoning/Limits.

**7. Going further (optional).** Center/scale `x` and refit order 9; show the PSD warning disappears.

**8. Submission & reproducibility.** Seeded `default_rng(100)`. Autograder imports
`PolynomialRegressionModel`, `sample_dataset`, `generate_synthetic_data`; keep those signatures.
`import hw` must be cheap and must **not** write PDFs (driver under `if __name__ == "__main__"`).

---

## 2. `hw10/rubric.md` — autograded + CERL (split 55 / 35 / 10)

### 2a. Correctness (55) — independent autograded tests (validated 6/6; mutation-tested)

| Test | Obj | Pts | Checks |
|------|-----|:---:|--------|
| `test_cov_w_definition` | O1 | 10 | `cov_w == σ̂²·inv(XᵀX)` (model's own `σ̂²` → bug-agnostic) |
| `test_cov_w_symmetric_psd` | O1 | 8 | symmetric + eigenvalues ≥ 0 |
| `test_predictive_variance_matches_cov_w` | O2 | 12 | `predictive_variance(x) == diag(X_new·cov_w·X_newᵀ)` (couples both methods) |
| `test_predictive_variance_nonnegative` | O2 | 6 | all variances ≥ 0 |
| `test_predictive_variance_vectorized` | O2 | 7 | returns a length-`len(x)` vector = per-point loop |
| `test_variance_larger_in_gap` | O3 | 12 | **floor-AND-guard:** variance at gap center (x=3.5) > at dense x=0 |

**Sum = 55.** No absolute-value pin (it embeds the `sigma_sq` bug); the relationship + gap tests are
method- and bug-independent. Floor-AND-guard = `variance_larger_in_gap`, paired with `matches_cov_w`
so a constant/zero variance is rejected (mutation-verified).

### 2b. Interpretation (35) — CERL on the three captions. PASS = ≥2 each.

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | correctly states the qualitative behavior (error bars grow in the gap/edges; order trade-off) | mostly | partial | missing |
| **Evidence** | cites the specific figures/orders (order-3 tightest; orders 5/9 blow up in the gap) | some | vague | none |
| **Reasoning** | links flexibility/extrapolation → variance; overfitting in sampled datasets | sound | superficial | absent |
| **Limits** | notes where it fails: high-order instability, no data ⇒ no constraint, MLE assumptions | one weakly | minimal | none |

### 2c. Process (10): runs clean + `import hw` cheap + **no PDFs written at import** (4); figures
generated & saved under `__main__` (3); docstrings intact, vectorized, no hard-coded numbers (3).

---

## 3. Objective → rubric-row map

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| O1 `compute_cov_w` | Apply | Correctness: cov_w definition + PSD | ✅ |
| O2 vectorized `predictive_variance` | Apply | Correctness: matches_cov_w + nonneg + vectorized | ✅ |
| O3 variance grows where sparse | Analyze | Correctness: `variance_larger_in_gap` (floor-AND-guard) | ✅ |
| O4 interpret the figures | Evaluate | Interpretation (CERL captions) | ✅ |
| *(reproducibility/communication)* | — | Process | ✅ |

**Every objective maps to a row; none orphaned.**

---

## 4. Proposed diffs (per file — NOT applied)

### 4a. `hw.py` — fix the `sigma_sq` MLE; guard the driver (3 PDF loops) under `__main__` (markers preserved)

```diff
@@ class PolynomialRegressionModel.train @@
-        sigma_sq = ((1 / N) * (t.T @ t - t.T @ X @ w))
+        sigma_sq = (1 / X.shape[0]) * (t.T @ t - t.T @ X @ w)   # MLE: divide by n_train, not the global N
@@ module scope: data generation + matplotlib + the three plot/savefig loops @@
+def main():
+    from matplotlib import pyplot as plt
+    rng = np.random.default_rng(seed=100)
+    x, t = generate_synthetic_data(rng, N=40, x_min=-2, x_max=7,
+                                   noise_variance=6, gap_min=2.5, gap_max=4.5)
+    # ... (the three existing plotting loops, incl. fig.savefig to images/) ...
+
+
+if __name__ == "__main__":
+    main()
```
The two SOLUTION blocks (`compute_cov_w`, `predictive_variance`) are unchanged. `import hw`:
**1.23 s → 0.074 s**, **0 PDFs** written at import (was 12), no RuntimeWarning.

### 4b. `test_hw.py` — replace the two pinned-value asserts with the 6 property tests (§2a, validated).

### 4c. `hw.tex` — unchanged answer captions (the reference); add one line outside `%%% Answer %%%`
pointing to `rubric.md` for the caption criteria. (Strip mechanism already verified: the 3 caption
blocks are removed by `make_release`'s sed; sections + figure scaffold retained.)

### 4d. `README.md` — 8-part framing + criteria table; replaces the 1/0.5/0 gate.

### 4e. `make_release` — ship `rubric.md`:
```diff
 cp test_hw.py release
 cp README.md release
+cp rubric.md release
```

### 4f. `rubric.md` — NEW (full §2; shipped to students).

---

## 5. Effort & budget

| Component | Change |
|-----------|--------|
| Code (two formulas) | unchanged (~30 min) |
| Captions | unchanged (~20 min; now CERL-graded) |
| Net | within budget; import-time fix removes a 1.2 s + 12-PDF side effect from every test run |

---

## 6. Judgment calls beyond the spec

1. **`sigma_sq` MLE bug fixed** (`/global-N` → `/n_train`); pins removed in favor of bug-agnostic
   relationships. **PENDING-RATIFICATION** (changes error-bar magnitudes by a positive scalar; the
   qualitative captions remain valid).
2. **Type-2 hybrid** (captions interpret the code's plots) → single 55/35/10, captions = the
   Interpretation layer (hw11 pattern).
3. **Driver guarded** under `__main__` (no PDFs/plots/RNG at import); graded class/functions stay at
   module scope (the autograder imports them).
4. **No absolute-value pin** — closed-form but bug-tainted; tested by relationship + PSD + gap.
5. **Order-9 PSD RuntimeWarning** left as a flagged numerical limitation (a Going-further /
   interpretation hook), not fixed in this pass.
6. **Through-line:** the design-matrix/normal-equation machinery is hw2's, generalized to order `k`
   (hw1→hw2→hw3→hw10 regression chain).

---

## 7. Validation results (against the reference; repo `.venv`)

- **Key audit:** pins reproduce the buggy `/40` `sigma_sq` exactly; correct `/n_train` gives ~13×
  larger; `cov_w == σ̂²·inv(XᵀX)` (PSD) and `predictive_variance == diag(X·cov_w·Xᵀ)` verified. ✅
- **New suite vs reference (fixed `train`):** **6 passed in 0.06 s.** ✅
- **Import-time fix:** `import hw` **1.23 s → 0.074 s**; **0 PDFs** at import (was 12); RuntimeWarning
  gone from the import path. ✅
- **Mutation-tested guards:**
  | Injected method | Tests that correctly FAIL |
  |-----------------|---------------------------|
  | `cov_w` drops `σ̂²` | `cov_w_definition`, `matches_cov_w` |
  | `predictive_variance` constant | `matches_cov_w`, **`variance_larger_in_gap`** |
  | `predictive_variance` zeros | `matches_cov_w`, **`variance_larger_in_gap`** |
  | `predictive_variance` scalar (not vectorized) | `matches_cov_w`, `vectorized`, `variance_larger_in_gap` |
  | reference (correct) | none — all 6 pass ✅ |
- **Written strip check:** `make_release` sed removes all 3 reference captions; 4 sections + figure
  scaffold retained; 3 answer blocks. ✅

---

## 8. Proposed commit message (this commit)

```
hw10 overhaul: property/PSD tests + caption CERL for predictive variance (hybrid type-2)

Type-2 hybrid (code generates plots; hw.tex captions interpret them) -> single
autograded split 55/35/10, captions folded into the Interpretation layer (hw11 pattern).

- REFERENCE FIX (PENDING-RATIFICATION): hw.py train() computed sigma_sq with the
  module-global N=40 instead of the training-set size, so the MLE noise variance was
  wrong (off ~13x for the 3-point test; wrong in the main flow too, ~31 gapped points).
  Fix sigma_sq = (1/X.shape[0])*(t^T t - t^T X w); also removes the global-N coupling.
  The pinned cov_w / predictive_variance(0.5) baked in the bug -> removed.
- test_hw.py: replace the 2 pinned asserts with 6 property/outcome tests (Correctness
  55 = 10/8/12/6/7/12): cov_w == sigma_sq inv(X^T X), cov_w symmetric+PSD,
  predictive_variance == diag(X_new cov_w X_new^T) (couples both methods), nonnegative,
  vectorized, and variance_larger_in_gap (floor-AND-guard). Bug-agnostic (relationships,
  not absolute values). Mutation-tested (constant/zero/non-vectorized/sigma-less all
  fail); 6/6 vs reference in 0.06s.
- hw.py: move the data generation + matplotlib + the THREE plot/savefig loops into
  main() under `if __name__ == "__main__"`. import hw: 1.23s -> 0.074s; 0 PDFs written
  at import (was 12); the order-9 "covariance not PSD" RuntimeWarning leaves the import
  path. SOLUTION markers unchanged.
- rubric.md (new): autograded 55 + caption CERL 35 (variance vs order, gap effect,
  overfitting) + Process 10 (incl. no-PDF-at-import). Shipped to students.
- README.md: 8-part framing + criteria table; replaces 1/0.5/0.
- make_release: ships rubric.md (sed Python + LaTeX strips unchanged; verified the 3
  captions strip and sections/figure scaffold remain).
- through-line: design-matrix/normal-equation machinery from hw2, generalized to order k.

FLAG: sigma_sq fix changes error-bar magnitudes (qualitative captions still valid) —
pending instructor ratification. Order-9 Vandermonde PSD warning left as a flagged
numerical limitation / interpretation hook.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
