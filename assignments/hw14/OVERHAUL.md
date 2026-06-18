# hw14 — Overhaul draft (HYBRID type-1 · code logistic-MAP + written Poisson Newton-Raphson)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw14. **Two separate deliverables** (hw6/hw2 type-1):
autograded `hw.py` (Bayesian **logistic** regression MAP via Newton-Raphson) **plus** a hard-copy
written derivation in `hw.typ` (Newton-Raphson update for a **Poisson** likelihood). **Draft only —
diffs proposed, not applied.**

> **STEP 0 — classification: HYBRID type-1.** `test_hw.py` autogrades the code; the Typst derivation
> is hard copy. Two distinct artifacts → each at its canon split, inter-component weight on top
> (**60 code / 40 written**, FLAGGED, §2c).

> **Through-line (preserved).** This is **hw13's target**: the code performs MAP inference on
> exactly the Bayesian-logistic-regression PGM hw13 drew — the `σ²→w` prior edge is the
> regularizer here. Forward: the MAP `w` and the negative Hessian seed **hw15** (Laplace) and
> **hw16** (MCMC). The MAP `[1.64, 2.00]` is the posterior **mode** (≠ hw16's posterior mean — the
> map's standing caution).

**Defects fixed:** magic-constant pin on the post-Newton `w`; import-time work (data load + Newton
loop + two plots + a probability-contour double loop); 1/0.5/0; no graded interpretation in either
half; a notation inconsistency in the written key (§0).

---

## 0. Reference-correctness audit (independently verified)

**Code key** — ran Newton-Raphson independently (10 iters, σ²=10):

| Check | Value | Verdict |
|-------|-------|---------|
| `w_MAP` | `[1.63985881, 1.99983755]` = pin | ✅ exact |
| `‖grad(w_MAP)‖` | `6.0e-16` | ✅ stationary (the MAP condition) |
| Hessian eigvals at MAP | `[-0.481, -0.217]` | ✅ negative-definite (concave maximum) |
| `logpost(MAP)` vs `logpost(0)` | `-0.537` vs `-27.73` | ✅ MAP beats prior mean (floor-AND-guard) |

**Written key (Poisson Newton-Raphson)** — verified by inspection: log-likelihood
`-log(t_n!) + t_n log(wᵀx_n) - wᵀx_n`; gradient `Σ[t_n x_n/(wᵀx_n) - x_n] - w/σ²`; Hessian
`-I/σ² - Σ t_n x_n x_nᵀ/(wᵀx_n)²`; update `w - H⁻¹g`. **All correct.** One blemish: several LHS
write `∂p/∂w` / `∂²p/∂w∂wᵀ` where they mean `∂log p` (lines for the likelihood gradient and the
Hessian); the prior/posterior lines correctly write `∂log p`. **Math is right; notation is
inconsistent.** Minimal fix = insert "log"; **flagged, low-priority** (not a correctness error).

---

## 1. Prompt rewritten into the 8-part template (markdown → `README.md`)

**1. Context & purpose.** Find the MAP estimate of a Bayesian logistic-regression model by
Newton-Raphson — second-order optimization on the log-posterior of the very model you drew in
HW13. The MAP and its (negative) Hessian are the inputs to the Laplace approximation (HW15) and a
reference point for MCMC (HW16).

**2. Learning objectives** (Bloom + graded row):
- *Code* **A-O1** *Implement* the vectorized `logistic`. *(Apply — Correctness: logistic)*
- *Code* **A-O2** *Implement* the log-posterior `gradient` and `hessian`. *(Apply — Correctness:
  gradient/hessian)*
- *Code* **A-O3** *Drive* Newton-Raphson to the MAP. *(Analyze — Correctness: MAP recovery floor)*
- *Code* **A-O4** *Interpret* the estimate, convergence, and decision boundary. *(Evaluate —
  Code Interpretation)*
- *Written* **B-O1…O4** *Derive* the Poisson gradient, prior gradient, Hessian, Newton update.
  *(Apply/Analyze — Written Correctness, per-step)*
- *Written* **B-O5** *Explain* the minus-sign / negative-definite-Hessian / prior-as-regularizer.
  *(Evaluate — Written Interpretation)*

**3. The task.** Code: fill `logistic`, the `p` in `gradient`/`hessian`; the test drives Newton to
the MAP. **Any correct vectorized implementation passes.** Written: derive the Poisson
Newton-Raphson update with a Gaussian prior.

**4. What you may / may not use.** Code: any NumPy. Written: log-posterior or explicit likelihood,
components or matrix-calculus identities (state them). No hard-coded MAP.

**5. How you'll be assessed.** §2 — autograded recovery floor + properties (code); per-step rubric
(written); inter-component weight.

**6. Required interpretation.** *Code* (markdown cell): what the MAP `w` and the decision boundary
say; did Newton converge (it should in a few steps — why so fast?); how the prior `σ²` shapes the
estimate. *Written* (paragraph): the minus sign while maximizing; the negative-definite Hessian
condition; the prior as ridge regularization and the HW13 `σ²→w` edge.

**7. Going further (optional).** Vary `σ²` and watch the MAP shrink toward `0`.

**8. Submission & reproducibility.** Deterministic. Autograder imports `logistic, gradient,
hessian`; keep signatures. `import hw` must be cheap (driver under `__main__`). Written = hard copy;
solution stays inside `#answer([…], [])`.

---

## 2. `hw14/rubric.md` — two components at their canon splits

### 2a. Component A — Code (logistic MAP), internal **55 / 35 / 10**

**Correctness (55) — autograded** (validated 6/6 vs reference; mutation-tested):

| Test | Obj | Pts | Checks |
|------|-----|:---:|--------|
| `test_logistic_properties` | A-O1 | 10 | `logistic(0)=0.5`, `logistic(1)≈0.731`, range (0,1), monotone, `1−logistic(−x)`, vectorized |
| `test_gradient_zero_at_map` | A-O3 | 12 | **recovery floor:** `‖gradient(w_MAP)‖ < 1e-4` (the MAP condition) |
| `test_map_matches_reference` | A-O3 | 10 | `w_MAP ≈ [1.63986, 1.99984]` (`rel=1e-3`) |
| `test_hessian_negative_definite` | A-O2 | 9 | Hessian symmetric, eigenvalues < 0 (concave max) |
| `test_map_beats_prior_mean` | A-O3 | 8 | **floor-AND-guard:** `logpost(MAP) > logpost(0)` and `‖w_MAP‖>1` |
| `test_gradient_hessian_shapes` | A-O2 | 6 | gradient `(2,)`, hessian `(2,2)` |

**Sum = 55.** The pin is replaced by the **recovery floor** (gradient ≈ 0 at the MAP — any correct
optimizer reaches it) plus the closed-form `w` (rel tol) and the negative-definite-Hessian property.
Floor-AND-guard = `map_beats_prior_mean` (a trivial `w=0` estimate fails). Mutation-verified.

**Interpretation (35) — CERL** on the code reflection (MAP/decision boundary, convergence, prior
effect). PASS = ≥2 each (Claim/Evidence/Reasoning/Limits).

**Process (10):** runs clean + `import hw` cheap (4); plots labeled (3); docstrings intact,
vectorized (3).

### 2b. Component B — Written (Poisson Newton-Raphson), internal **60 / 30 / 10**

**Correctness (60) — per-step derivation rubric** (any valid route full credit; 3/2/1/0 tiers):

| Step | Obj | Pts | Exemplary |
|------|-----|:---:|-----------|
| **A · Setup** | B-O1 | 10 | log-posterior = log-prior + Σ log-likelihood |
| **B · Log-lik gradient** | B-O2 | 16 | chain rule on `t_n log(wᵀx_n)` → `t_n x_n/(wᵀx_n) − x_n` |
| **C · Prior gradient** | B-O3 | 8 | `−w/σ²` from the Gaussian log-prior |
| **D · Hessian** | B-O4 | 14 | `−I/σ² − Σ t_n x_n x_nᵀ/(wᵀx_n)²` |
| **E · Newton update** | B-O4 | 12 | `w⁽ⁱ⁺¹⁾ = w⁽ⁱ⁾ − H⁻¹g`, minus retained |

**Sum = 60. Load-bearing step = B** (the chain rule through `log(wᵀx_n)`; an error here caps the
gradient and Hessian values, but C/D/E are graded on the student's own pieces). D depends on B's
gradient.

**Interpretation (30) — CERL** on the §6 written paragraph (minus sign while maximizing;
negative-definite Hessian; prior as regularization + HW13 edge). PASS = ≥2 each.

**Process (10):** notation (incl. **`∂log p` not `∂p`**), prior contribution explicit, legible.

### 2c. Inter-component weight (FLAGGED) — **Code 60 % / Written 40 %**

The code is the **primary objective and the through-line anchor** (hw13→14→15→16); the written
Poisson derivation is substantial but supporting. Effort ≈ balanced (~45 min each), so not 70/30.
**Alternative 55/45.** PENDING-RATIFICATION.

---

## 3. Objective → rubric-row map

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| A-O1 logistic | Apply | Correctness: `logistic_properties` | ✅ |
| A-O2 gradient/Hessian | Apply | Correctness: `hessian_negative_definite`, `shapes` | ✅ |
| A-O3 Newton → MAP | Analyze | Correctness: `gradient_zero_at_map`, `map_matches`, `map_beats_prior_mean` | ✅ |
| A-O4 interpret estimate | Evaluate | Code Interpretation (CERL) | ✅ |
| B-O1…O4 derive | Apply/Analyze | Written Correctness A–E | ✅ |
| B-O5 explain update/Hessian/prior | Evaluate | Written Interpretation (CERL) | ✅ |
| *(communication)* | — | Process rows | ✅ |

**Every objective maps to a row; none orphaned.**

---

## 4. Proposed diffs (per file — NOT applied)

### 4a. `hw.py` — guard the driver under `__main__` (markers preserved)

The three SOLUTION blocks (the `p` computations, `logistic` body) are unchanged. Data load + Newton
loop + two plots + the probability-contour double loop move into `main()`:
```diff
+def main():
+    from matplotlib import pyplot as plt
+    X = np.loadtxt("data/X.csv", delimiter=","); t = np.loadtxt("data/t.csv"); sig_sq = 10
+    w = np.zeros(2)
+    for _ in range(10):
+        w = w - np.linalg.inv(hessian(w, X, sig_sq)) @ gradient(w, X, t, sig_sq)
+    # ... (the existing w-evolution plot + probability-contour plot) ...
+
+if __name__ == "__main__":
+    main()
```
`import hw` measured **0.91 s → 0.037 s**.

### 4b. `test_hw.py` — replace the pinned-`w` assert with the 6-test recovery-floor/property suite (§2a, validated).

### 4c. `hw.typ` — add Allowed-approaches + Required-interpretation (outside `#answer`) + a reference-interpretation `#answer`; (optional, flagged) insert "log" on the `∂p`→`∂log p` LHS. Strip validated (2 `#answer`, solution + ref interp stripped, framing retained).

### 4d. `README.md` — 8-part framing + hybrid criteria table; replaces 1/0.5/0.

### 4e. `make_release` — ship `rubric.md`:
```diff
     cp test_hw.py release
+    cp rubric.md release
```
(Existing Python sed + `make without_answers` unchanged.)

### 4f. `rubric.md` — NEW (full §2; shipped).

---

## 5. Effort & budget

| Component | Change |
|-----------|--------|
| Code | unchanged (~30 min) |
| Code reflection | +~15 min (new) |
| Written derivation | unchanged (~40 min) |
| Written interpretation | +~10 min (new) |
| Net | within budget; import-time fix speeds the autograder |

---

## 6. Judgment calls beyond the spec

1. **Pin → recovery floor.** `w_MAP` pin replaced by `‖grad(MAP)‖<tol` + closed-form `w` (rel) +
   negative-definite Hessian + beats-prior floor-AND-guard. Any correct optimizer passes.
2. **Type-1 hybrid, weight 60/40** (code primary / through-line anchor). PENDING-RATIFICATION.
3. **Driver guarded** under `__main__`; graded functions stay at module scope.
4. **Written notation inconsistency** (`∂p` vs `∂log p`) flagged; math verified correct, fix
   optional/low-priority (avoids over-editing a correct derivation).
5. **Through-line preserved:** hw13 PGM → hw14 MAP (the `σ²→w` edge is the regularizer) → hw15
   Laplace → hw16 MCMC; the interpretation states the hw13 link explicitly. MAP = mode (≠ hw16 mean).
6. **Interpretation media:** markdown cell (code) + paragraph (written).

---

## 7. Validation results (against the reference; repo `.venv`)

- **Code key:** `w_MAP=[1.63985881,1.99983755]` reproduces the pin exactly; `‖grad(MAP)‖=6e-16`;
  Hessian eigvals `[-0.481,-0.217]`<0; `logpost(MAP)=-0.54 > logpost(0)=-27.7`. ✅
- **Written key:** Poisson gradient/Hessian/update verified by inspection; notation blemish noted. ✅
- **New code suite vs reference:** **6 passed in 0.05 s.** ✅
- **Import-time fix:** `import hw` **0.91 s → 0.037 s**; functions importable. ✅
- **Mutation-tested guards:**
  | Injected | Tests that correctly FAIL |
  |----------|---------------------------|
  | `logistic ≡ 0.5` | logistic_properties, gradient_zero, map_matches, beats_prior |
  | gradient drops prior `−w/σ²` | gradient_zero, map_matches |
  | gradient sign-flip | beats_prior, map_matches |
  | hessian drops `−I/σ²` | gradient_zero, map_matches |
  | reference | none — all 6 pass ✅ |
- **Written strip check:** solution + reference interpretation stripped; title, Allowed-approaches,
  Required-interpretation, Workload retained; 2 `#answer` blocks. ✅

---

## 8. Proposed commit message (this commit)

```
hw14 overhaul: recovery-floor MAP tests + Poisson-derivation rubric (hybrid type-1)

Two separate deliverables (autograded logistic-MAP code + hard-copy Poisson
Newton-Raphson derivation), hw6/hw2 type-1. Inter-component weight 60 code / 40
written -- FLAGGED for ratification. This is HW13's through-line target: the code does
MAP inference on that Bayesian-logistic-regression PGM (the sigma^2->w prior edge).

Code component (internal 55/35/10):
- test_hw.py: replace the pinned post-Newton w==[1.6399,1.9998] with 6 tests
  (Correctness 55 = 10/12/10/9/8/6): logistic properties, gradient_zero_at_map
  (recovery floor: ||grad(w_MAP)||<1e-4 -- the MAP condition), map_matches (rel=1e-3),
  hessian_negative_definite (concave max), map_beats_prior_mean (floor-AND-guard:
  logpost(MAP)>logpost(0), ||w||>1), gradient/hessian shapes. Mutation-tested
  (constant logistic, prior-less gradient, sign-flip, prior-less Hessian all fail);
  6/6 vs reference, 0.05s.
- hw.py: move data load + Newton loop + plots + the probability-contour double loop
  into main() under `if __name__ == "__main__"`. import hw: 0.91s -> 0.037s. SOLUTION
  markers unchanged.
- rubric.md: code Interpretation 35 = CERL (MAP/decision boundary, convergence, prior
  effect); Process 10.

Written component (internal 60/30/10):
- hw.typ: add Allowed-approaches + Required-interpretation prompts (outside #answer)
  and a reference-interpretation #answer (minus-sign while maximizing; negative-definite
  Hessian; prior as regularization + the HW13 sigma^2->w edge). Strip validated.
- rubric.md: per-step Correctness 60 = A/B/C/D/E = 10/16/8/14/12 (B the load-bearing
  chain rule through log(w^T x)); Poisson gradient/Hessian/update verified correct by
  inspection. Interpretation 30 = CERL; Process 10.
- FLAG: a notation inconsistency in the key (several LHS write d p / d w for d log p);
  math is correct, fix is optional/low-priority.

- README.md: 8-part framing + hybrid criteria table; replaces 1/0.5/0.
- make_release: ships rubric.md (sed Python + make without_answers unchanged).
- through-line: hw13 PGM -> hw14 MAP (mode, not hw16's mean) -> hw15 Laplace -> hw16 MCMC.

Reference math verified (code MAP + Poisson derivation). Autograder: 6 tests, 0.05s,
import 0.037s.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
