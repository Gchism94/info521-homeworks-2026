# hw15 — Overhaul draft (HYBRID type-1 · code Laplace approx + written Beta–Binomial Laplace)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw15. **Two separate deliverables** (hw2/hw14 type-1):
autograded `hw.py` (Laplace approximation for Bayesian logistic regression) **plus** a hard-copy
written derivation in `hw.typ` (Laplace approximation for a Beta prior + Binomial likelihood).
**Draft only — diffs proposed, not applied.**

> **STEP 0 — classification: HYBRID type-1.** `test_hw.py` autogrades deterministic globals
> (`w_MAP`, `g_cov`); the Typst derivation is hard copy. Inter-component weight **60 code / 40
> written** (FLAGGED, §2c).

> **Through-line (preserved).** **hw14** MAP `w_MAP` → **hw15** Laplace `N(w_MAP, (−H)⁻¹)` →
> **hw16** MCMC. The Laplace *mean is the mode* `[1.64, 2.00]` (≠ hw16's posterior mean — the
> map's caution). The written half approximates the **hw11** Beta–Binomial coin posterior (and uses
> the **hw8** Beta moments) with a Gaussian at its mode.

**Defects fixed:** magic pins on deterministic `w_MAP`/`g_cov`; **unseeded `np.random.multivariate_
normal` at module scope**; a **budget blowup** (§0); import-time plots + `print`; 1/0.5/0; no graded
interpretation in either half.

---

## 0. Reference-correctness audit (independently verified)

**Code key** (ran the procedure independently):

| Check | Value | Verdict |
|-------|-------|---------|
| `w_MAP` | `[1.63985881, 1.99983755]` = pin = **hw14 mode** | ✅ exact |
| `g_cov` | `[[3.50656, −1.25042], [−1.25042, 3.17127]]` = pin | ✅ exact |
| `g_cov` symmetric / PSD | eigvals `[2.077, 4.601] > 0` | ✅ |
| `g_cov == (−H)⁻¹` | yes | ✅ defining Laplace covariance |

**Budget blowup found.** The contour cell computes `P = logistic(g @ w_samples.T).mean(axis=1)`
with `g` = (10000, 2) and **`w_samples` = (100000, 2)** → a **10000×100000 (~8 GB) matrix** at
import. The cell's own markdown says *"sample **1000** samples"* — the code uses **100000**. **Fix:**
use **1000** (matches the instruction; `g @ w_samples.T` becomes 10000×1000 ≈ 80 MB) **and** seed
the sampler. The original `import hw` hangs/OOMs; guarded+fixed import is sub-second.

**Written key (Beta–Binomial Laplace)** — verified symbolically (sympy): mode
`r̂ = (γ−1)/(γ+δ−2)` and `ν = (α+β+N−2)³/((y+α−1)(N−y+β−1))` with `γ=y+α`, `δ=N−y+β`. **Both
correct.** ✅

---

## 1. Prompt rewritten into the 8-part template (markdown → `README.md`)

**1. Context & purpose.** The Laplace approximation fits a Gaussian at the posterior mode — the
cheapest way to put a covariance on a non-Gaussian posterior. You build it around the HW14 logistic
MAP (code) and derive it in closed form for the HW11 coin posterior (written), the bridge between
exact conjugacy and the MCMC of HW16.

**2. Learning objectives** (Bloom + graded row):
- *Code* **A-O1** *Recover* the MAP `w_MAP`. *(Apply — Correctness: w_MAP tests)*
- *Code* **A-O2** *Form* the Laplace covariance `g_cov = (−H)⁻¹`. *(Apply — Correctness: g_cov tests)*
- *Code* **A-O3** *Sample* the approximation reproducibly to visualize decision boundaries.
  *(Apply — Process: seeded)*
- *Code* **A-O4** *Interpret* the approximation. *(Evaluate — Code Interpretation)*
- *Written* **B-O1…O4** *Derive* the posterior Beta form, the mode, the curvature `ν`, the closed
  form. *(Apply/Analyze — Written Correctness, per-step)*
- *Written* **B-O5** *Judge* when the Laplace approximation is good/poor. *(Evaluate — Written
  Interpretation)*

**3. The task.** Code: produce `w_MAP` (reuse HW14) and `g_cov = (−H)⁻¹`; sample the Gaussian
**with a seed**. Written: derive `r̂` and `ν` in closed form.

**4. What you may / may not use.** Code: any NumPy; **seed the RNG** (`default_rng(seed)`). Written:
re-parameterized Beta or explicit likelihood (both shown valid). No hard-coded numbers.

**5. How you'll be assessed.** §2 — property/recovery tests (code), per-step rubric (written),
inter-component weight.

**6. Required interpretation.** *Code* (markdown cell): what the sampled decision boundaries show;
why a Gaussian centered at the MAP, and what it misses. *Written* (paragraph): when is the Laplace
approximation accurate vs. poor for the coin posterior (e.g. skewed Beta near `r=0/1`, small `N`)?

**7. Going further (optional).** Compare the Laplace samples' empirical mean/cov to `w_MAP`/`g_cov`.

**8. Submission & reproducibility.** **Seed `default_rng`.** Autograder imports `w_MAP, g_cov`; keep
those names; `import hw` must be cheap (sampling/plots under `__main__`, ≤1000 contour samples).
Written = hard copy; solution stays inside `#answer([…], [])`.

---

## 2. `hw15/rubric.md` — two components at their canon splits

### 2a. Component A — Code (Laplace approximation), internal **55 / 35 / 10**

**Correctness (55) — autograded** (validated 6/6 vs reference; mutation-tested):

| Test | Obj | Pts | Checks |
|------|-----|:---:|--------|
| `test_w_MAP_matches_reference` | A-O1 | 9 | `w_MAP ≈ [1.63986, 1.99984]` (`rel=1e-3`; = hw14) |
| `test_w_MAP_is_stationary` | A-O1 | 9 | **recovery floor:** `‖gradient(w_MAP)‖ < 1e-4` |
| `test_w_MAP_beats_prior_mean` | A-O1 | 8 | **floor-AND-guard:** `logpost(w_MAP) > logpost(0)`, `‖w_MAP‖>1` |
| `test_g_cov_symmetric_psd` | A-O2 | 10 | symmetric, eigenvalues > 0 |
| `test_g_cov_is_inverse_neg_hessian` | A-O2 | 14 | `g_cov ≈ (−H)⁻¹` (the defining relation) |
| `test_g_cov_matches_reference` | A-O2 | 5 | `g_cov ≈ [[3.507,−1.250],[−1.250,3.171]]` (`rel=1e-3`) |

**Sum = 55.** Closed-form pins kept with rel headroom but no longer the *only* gate — the
relationship (`g_cov=(−H)⁻¹`) + PSD + recovery floor carry method-independent credit. Mutation-
verified (`w_MAP=0`, `g_cov=I`, sign-flipped, diagonal-only all fail).

**Interpretation (35) — CERL** on the code reflection. PASS = ≥2 each.

**Process (10):** runs clean + `import hw` cheap + **seeded RNG** (4); plots labeled (3); docstrings
intact (3).

### 2b. Component B — Written (Beta–Binomial Laplace), internal **60 / 30 / 10**

**Correctness (60) — per-step derivation rubric** (any valid route; 3/2/1/0 tiers):

| Step | Obj | Pts | Exemplary |
|------|-----|:---:|-----------|
| **A · Posterior is Beta** | B-O1 | 12 | likelihood×prior `∝ r^{γ−1}(1−r)^{δ−1}`, `γ=y+α, δ=N−y+β` |
| **B · Mode `r̂`** | B-O2 | 18 | `∂ log p/∂r=0` ⇒ `r̂ = (γ−1)/(γ+δ−2)` |
| **C · Curvature `ν`** | B-O3 | 14 | `ν = −∂²log p/∂r²\|_{r̂} = (γ−1)/r̂² + (δ−1)/(1−r̂)²` |
| **D · Closed form** | B-O4 | 16 | simplify to `ν = (α+β+N−2)³/((y+α−1)(N−y+β−1))`; report `N(r̂, 1/ν)` |

**Sum = 60. Load-bearing:** B (the mode) feeds C/D (ν is evaluated at `r̂`); grade C/D on the
student's own `r̂`. B and the C→D simplification are the heavy moves.

**Interpretation (30) — CERL** on when Laplace is accurate vs. poor (skewed Beta near `0/1`, small
`N`; the Gaussian's symmetric tails vs. the bounded `[0,1]` support). PASS = ≥2 each.

**Process (10):** notation, `γ/δ` defined, `log`-posterior stated, legible.

### 2c. Inter-component weight (FLAGGED) — **Code 60 % / Written 40 %**

Code is the through-line anchor (hw14→15→16); the written derivation is substantial but supporting.
**Alternative 55/45.** PENDING-RATIFICATION.

---

## 3. Objective → rubric-row map

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| A-O1 recover MAP | Apply | Correctness: w_MAP tests | ✅ |
| A-O2 Laplace covariance | Apply | Correctness: g_cov tests | ✅ |
| A-O3 sample reproducibly | Apply | Process (seeded) | ✅ |
| A-O4 interpret | Evaluate | Code Interpretation (CERL) | ✅ |
| B-O1…O4 derive `r̂`,`ν` | Apply/Analyze | Written Correctness A–D | ✅ |
| B-O5 judge accuracy | Evaluate | Written Interpretation (CERL) | ✅ |
| *(communication)* | — | Process rows | ✅ |

**Every objective maps to a row; none orphaned.**

---

## 4. Proposed diffs (per file — NOT applied)

### 4a. `hw.py` — seed the sampler; fix the sample count; guard the driver (markers preserved)

`w_MAP` and `g_cov` stay at module scope (deterministic, cheap, imported by the test). The sampling
+ plots move into `main()`, **seeded** and at **1000** contour samples:
```diff
@@ inside the SOLUTION block / driver @@
-w_samples = np.random.multivariate_normal(w_MAP, g_cov, 100000)   # unseeded, at import, 1e9-element contour
+rng = np.random.default_rng(seed=100)             # reproducible
+w_samples = rng.multivariate_normal(w_MAP, g_cov, 1000)   # markdown says "sample 1000"; avoids the 8 GB blowup
@@ module scope: plot_data() call, decision-boundary + contour plots, print(g_cov) @@
+def main():
+    from matplotlib import pyplot as plt
+    # ... (plot_data, decision boundaries, probability contour using the 1000 seeded samples) ...
+
+if __name__ == "__main__":
+    main()
```
Guarded `import hw` is sub-second (was a hang/OOM); `w_MAP`, `g_cov` importable.

### 4b. `test_hw.py` — replace the two pinned asserts with the 6-test property/recovery suite (§2a, validated).

### 4c. `hw.typ` — add Allowed-approaches + Required-interpretation (outside `#answer`) + a reference-interpretation `#answer`. (Derivation verified correct — unchanged.)

### 4d. `README.md` — 8-part framing + hybrid criteria table; replaces 1/0.5/0.

### 4e. `make_release` — ship `rubric.md`:
```diff
     cp test_hw.py release
+    cp rubric.md release
```

### 4f. `rubric.md` — NEW (full §2; shipped).

---

## 5. Effort & budget

| Component | Change |
|-----------|--------|
| Code | unchanged (~25 min) |
| Code reflection | +~15 min |
| Written derivation | unchanged (~40 min) |
| Written interpretation | +~10 min |
| Net | within budget; import fix removes an 8 GB / hang side effect |

---

## 6. Judgment calls beyond the spec

1. **Budget blowup + sample-count bug fixed** (100000 → 1000, matching the markdown) + **RNG
   seeded**. Resolves the unseeded-import + OOM defects at the source.
2. **Pins → recovery floor + relationship + PSD** (g_cov = (−H)⁻¹); closed-form kept with rel tol.
3. **Type-1 hybrid, weight 60/40** (code anchor). PENDING-RATIFICATION.
4. **Driver guarded** under `__main__`; deterministic graded globals stay at module scope.
5. **Through-lines:** hw14 MAP → hw15 Laplace → hw16 MCMC (mode ≠ mean); written approximates the
   hw11 Beta–Binomial posterior using hw8 Beta moments.
6. **Interpretation media:** markdown cell (code) + paragraph (written).

---

## 7. Validation results (against the reference; repo `.venv`)

- **Code key:** `w_MAP` (= hw14) and `g_cov` reproduce the pins exactly; `g_cov` symmetric/PSD;
  `g_cov=(−H)⁻¹`; `‖grad(w_MAP)‖=6e-16`; `logpost(MAP) ≫ logpost(0)`. ✅
- **Written key:** mode and `ν` verified symbolically (sympy). ✅
- **New code suite vs reference:** **6 passed in 0.06 s.** ✅
- **Import-time fix:** original import = 8 GB/hang (10⁹-element contour matrix); guarded+fixed import
  sub-second; `w_MAP`, `g_cov` importable. ✅
- **Mutation-tested guards:**
  | Injected | Tests that correctly FAIL |
  |----------|---------------------------|
  | `w_MAP = 0` | matches, stationary, beats_prior, inverse_neg_hessian |
  | `g_cov = I` | matches, inverse_neg_hessian |
  | `g_cov = inv(+H)` (sign) | symmetric_psd, matches, inverse_neg_hessian |
  | `g_cov` diagonal only | matches, inverse_neg_hessian |
  | reference | none — all 6 pass ✅ |
- **Written strip check:** mirrors hw14 (Typst `#answer`); solution stripped, prompts retained.

---

## 8. Proposed commit message (this commit)

```
hw15 overhaul: property/PSD tests + Beta-Binomial Laplace rubric (hybrid type-1)

Two separate deliverables (autograded Laplace code + hard-copy Beta-Binomial Laplace
derivation), hw2/hw14 type-1. Inter-component weight 60 code / 40 written -- FLAGGED.
Through-line: hw14 MAP -> hw15 Laplace N(w_MAP,(-H)^-1) -> hw16 MCMC (mode, not mean);
the written half approximates the hw11 Beta-Binomial coin posterior (hw8 Beta moments).

Code component (internal 55/35/10):
- REFERENCE FIXES: (a) the contour cell built logistic(g @ w_samples.T) with g (10000x2)
  and w_samples (100000x2) = a ~8 GB matrix that hangs/OOMs at import, though its own
  markdown says "sample 1000" -> use 1000 (10000x1000 ~80 MB). (b) np.random.multivariate_
  normal was UNSEEDED at module scope -> seed default_rng(100) for reproducibility.
- test_hw.py: replace the pinned w_MAP/g_cov asserts with 6 property/recovery tests
  (Correctness 55 = 9/9/8/10/14/5): w_MAP matches (=hw14, rel=1e-3), w_MAP stationary
  (recovery floor ||grad||<1e-4), w_MAP beats prior mean (floor-AND-guard), g_cov
  symmetric+PSD, g_cov == (-H)^-1 (defining relation), g_cov matches (rel). Mutation-
  tested (w_MAP=0, g_cov=I, sign-flip, diagonal-only all fail); 6/6 vs reference, 0.06s.
- hw.py: move plot_data/decision-boundary/contour + print into main() under
  `if __name__ == "__main__"`; w_MAP and g_cov stay at module scope (autograder imports
  them). import hw: hang/OOM -> sub-second. SOLUTION markers unchanged.
- rubric.md: code Interpretation 35 = CERL (decision boundaries; Gaussian-at-mode and
  what it misses); Process 10 (incl. seeded RNG).

Written component (internal 60/30/10):
- hw.typ: add Allowed-approaches + Required-interpretation prompts (outside #answer) and
  a reference-interpretation #answer (when Laplace is accurate vs poor: skewed Beta near
  0/1, small N). Derivation verified symbolically correct -> unchanged.
- rubric.md: per-step Correctness 60 = A/B/C/D = 12/18/14/16 (B mode load-bearing for
  the curvature; mode (g-1)/(g+d-2) and nu=(a+b+N-2)^3/((y+a-1)(N-y+b-1)) sympy-verified).
  Interpretation 30 = CERL; Process 10.

- README.md: 8-part framing + hybrid criteria table; replaces 1/0.5/0.
- make_release: ships rubric.md.

Reference math verified (code Laplace key + Beta-Binomial derivation). Autograder:
6 tests, 0.06s, import sub-second.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
