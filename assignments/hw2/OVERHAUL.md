# hw2 — Overhaul draft (HYBRID type-1 · code matrix-regression + written matrix-calculus derivations)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw2. **Two separate deliverables** → the **hw6
type-1 hybrid** pattern: an autograded `hw.py` (matrix-form linear regression) **plus** a hard-copy
written derivation in `hw.typ` (four matrix-calculus identities). **Draft only — no hw2 files are
modified; the diffs below are proposed, not applied.**

> **STEP 0 — classification: HYBRID type-1 (separate deliverables).** `test_hw.py` autogrades the
> code; `hw.typ` is a hard-copy derivation submitted on paper. They are *distinct artifacts* (not
> "code + an interpretation of that code" — that would be type-2/hw11). Each component carries its
> own canon split; an **inter-component weight** sits on top (proposed **60 code / 40 written**,
> **flagged for ratification**, §2c).

**Split:** code component → **55/35/10**; written component → **60/30/10** (repo canon).

**Defects fixed:** magic-constant pins (`w`, `winning_time_for_2012`, **the second-order coeffs —
which are numerically meaningless, §0**); import-time work (matplotlib + plots + three `print`s run
on import because the test imports module globals); no graded interpretation in either half; the
1/0.5/0 gate; a display typo in written Identity #1.

---

## 0. Reference-correctness audit (do not assume the key — hw12 had a wrong one)

**Code key** — re-derived independently from `data100m.csv` (N = 27, repo `.venv`):

| Quantity | Pinned | Re-derived | Verdict |
|----------|--------|-----------|---------|
| first-order `w` | `[36.4164559, -0.0133308857]` | `[36.41645590, -0.01333089]` | ✅ exact (= hw1's OLS fit) |
| `winning_time_for_2012` | `9.594713852048779` | `9.5947138520481` | ✅ exact |
| second-order `w_second_order` | `[455.597856, -0.443160486, 0.000110151552]` | `[455.597857, -0.443160486, 0.000110151552]` | ⚠️ **numerically unsafe — see below** |

**The second-order coefficient pins are a real defect.** `cond(X₂ᵀX₂) = 2.09e20` (a Vandermonde on
raw years, `x² ≈ 4e6`). The normal-equation residual on the `x²` column is **`1.35`, not ≈ 0** —
i.e. `inv(X₂ᵀX₂)` does not actually solve the system to full precision. A student who uses the
*more* stable `np.linalg.solve` or `np.linalg.lstsq` (exactly what the notebook's own appendix
recommends) can get **different** coefficients and fail a 9-sig-fig pin. The fit itself is fine —
the **MSE (0.03796)** and the **predictions** are the unique projection and are method-independent;
only the *coordinates* are unstable. **Fix:** test the second-order fit by its MSE and its
improvement over the line, not by pinned coefficients (§2a). Flagged in §6.

**Written key** — all four identities verified symbolically (sympy), symmetric `C`:

| Identity | Claim | Verdict |
|----------|-------|---------|
| #1 `∇ wᵀx` | `x` | ✅ |
| #2 `∇ xᵀw` | `x` | ✅ |
| #3 `∇ wᵀw` | `2w` | ✅ |
| #4 `∇ wᵀCw` | `2Cw` (sym `C`) | ✅ (general `C` → `(C+Cᵀ)w`; the symmetry step is load-bearing) |

One **display typo** in the Identity #1 reference: the `∂/∂w_N` line reads
`(w_N x_N + … + w_N x_N)` but should expand the *same* full sum `(w_1 x_1 + … + w_N x_N)`. The
result `x` is correct; the intermediate line is mis-typeset. **Fix:** one-token correction inside
`#answer` (§4c). Flagged.

---

## 1. Prompt rewritten into the 8-part template (markdown)

**1. Context & purpose.** Re-fit hw1's line using the **matrix normal equation**
`ŵ = (XᵀX)⁻¹Xᵀt`, then a quadratic — and, on paper, **derive the gradient identities that
equation rests on**. The two halves are coupled: the written math *proves* why the code's formula
minimizes the loss.

**2. Learning objectives** (Bloom + graded row):
- *Code* **A-O1** *Implement* the design matrix + normal equation. *(Apply — Code Correctness:
  first-order)*
- *Code* **A-O2** *Predict* a new year. *(Apply — Code Correctness: prediction)*
- *Code* **A-O3** *Fit & compare* a second-order model. *(Analyze — Code Correctness: second-order
  MSE/improvement)*
- *Code* **A-O4** *Interpret* first vs. second order and the numerical stability of the fit.
  *(Evaluate — Code Interpretation)*
- *Written* **B-O1…O4** *Derive* the four matrix-calculus identities. *(Apply/Analyze — Written
  Correctness: per-step Id1–4)*
- *Written* **B-O5** *Connect* the identities to the least-squares gradient/normal equation; locate
  the symmetry assumption. *(Evaluate — Written Interpretation)*

**3. The task (outcome, not recipe).** Code: complete `hw.py` so the module exposes the first-order
fit `w`, `winning_time_for_2012`, and the second-order fit `w_second_order`. **Any method that
yields the least-squares fit earns full credit** (`inv`, `solve`, `lstsq`, `polyfit`). Written:
derive the four identities for symmetric `C`, by either route shown.

**4. What you may / may not use.** Code: any NumPy linear-algebra routine. Written: explicit
multiplication or the Kronecker-delta component form (or any justified derivation); Identity #4
**must** invoke `C = Cᵀ`. You may **not** hard-code the autograded values.

**5. How you'll be assessed (criteria up front).** See §2 — each half has its own bundle table
(autograded thresholds for code; per-step rubric for the derivation), and an inter-component weight.

**6. Required interpretation.** *Code* (markdown cell, ~5–8 sentences): does the quadratic
meaningfully improve the fit, and what does extrapolating it risk? Why are the second-order
**coefficients** numerically touchy here, and how does that motivate `np.linalg.solve`/`lstsq` over
`inv` (the appendix)? *Written* (one paragraph): which identity gives the least-squares gradient,
how setting it to zero gives the normal equation, and **where** symmetry is used.

**7. Going further (optional).** Center/scale the years (`(x-x̄)/s`) and refit the quadratic;
compare the coefficient stability and `cond(X₂ᵀX₂)`.

**8. Submission & reproducibility.** Deterministic (no RNG). The autograder imports module globals
`w, winning_time_for_2012, w_second_order` from `hw` — keep those names; `import hw` must be cheap
(display/IO under `if __name__ == "__main__"`). Written half = hard copy; keep the solution inside
the `#answer([…], [])` first argument so `make without_answers` strips it.

---

## 2. `hw2/rubric.md` — two components, each at its canon split

### 2a. Component A — Code (matrix regression), internal **55 / 35 / 10**

**Correctness (55) — independent autograded tests** (validated 6/6 vs reference; mutation-tested):

| Test | Obj | Pts | Checks | Method-independent? |
|------|-----|:---:|--------|:--:|
| `test_first_order_normal_equations` | A-O1 | 10 | `Xᵀ(t − Xw) ≈ 0` (both columns) | ✅ defining OLS property |
| `test_first_order_matches_hw1` | A-O1 | 10 | `w ≈ [36.4165, −0.013331]` (`rel=1e-3`) | ✅ closed-form (= hw1 fit) |
| `test_prediction_2012` | A-O2 | 8 | `≈ 9.5947` **and** `= w·[1,2012]` | ✅ closed-form + consistency |
| `test_second_order_improves` | A-O3 | 12 | `MSE₂ ≤ 0.9·MSE₁` | ✅ **floor-AND-guard** |
| `test_second_order_min_mse` | A-O3 | 10 | `MSE₂ ≈ 0.0380` (`rel=2e-2`) | ✅ unique projection error |
| `test_second_order_shape` | A-O3 | 5 | three parameters | ✅ structural |

**Sum = 55.** No second-order **coefficient** pin (cond ≈ 1e20). Floor-AND-guard =
`test_second_order_improves`, paired with `min_mse` so a degenerate quadratic (a padded line) is
caught (mutation-verified).

**Interpretation (35) — CERL** on the §6 code reflection. PASS = ≥2 each.

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | states whether the quadratic helps and the extrapolation risk, correctly | mostly | partial | missing |
| **Evidence** | cites MSE₁≈0.050 vs MSE₂≈0.038, and/or `cond(X₂ᵀX₂)` / unstable coeffs | some | vague | none |
| **Reasoning** | links ill-conditioning → why `solve`/`lstsq` beats `inv` (the appendix) | sound | superficial | absent |
| **Limits** | a real limit: overfitting, extrapolation, conditioning, no error bars | one weakly | minimal | none |

**Process (10):** runs clean + `import hw` cheap (4); figures labeled (3); docstrings intact / no
hard-coded answers (3).

### 2b. Component B — Written (four matrix-calculus identities), internal **60 / 30 / 10**

**Correctness (60) — per-step derivation rubric.** Each identity scored on validity of the move,
any valid route (explicit / Kronecker) full credit. Tiers 3/2/1/0 → 100/80/45/0% of its points.

| Identity | Obj | Pts | 3 — Exemplary | 2 | 1 | 0 |
|----------|-----|:---:|---------------|---|---|---|
| **Id1 · `∇ wᵀx = x`** | B-O1 | 14 | componentwise `∂/∂w_k Σ wᵢxᵢ = x_k`, assembles `x` | minor slip | sets up, incomplete | missing |
| **Id2 · `∇ xᵀw = x`** | B-O2 | 8 | commutes inner product, cites Id1 | states result loosely | asserts | missing |
| **Id3 · `∇ wᵀw = 2w`** | B-O3 | 14 | `∂/∂w_k Σ wᵢ² = 2w_k`, assembles `2w` | minor slip | partial | missing |
| **Id4 · `∇ wᵀCw = 2Cw`** | B-O4 | 24 | double sum + product rule + Kronecker → `Σ(C_{ik}+C_{ki})wᵢ`, **then `C=Cᵀ` ⇒ `2Cw`** | result with one slip | reaches `(C+Cᵀ)w`, no symmetry step | missing |

**Sum = 60. Id4 heaviest** (the only non-trivial one). **Load-bearing step in Id4 = the symmetry
invocation** `C_{ik} = C_{ki}` collapsing `(C+Cᵀ)w` to `2Cw`; award the rest even if that step is
missed (cap at the `(C+Cᵀ)w` line). Id1/Id3 are independent; Id2 may legitimately depend on Id1.

**Interpretation (30) — CERL** on the §6 written paragraph (identities → normal equation; symmetry
located). PASS = ≥2 each. (Claim: the gradient of `L` uses Id2 + Id4 ⇒ `XᵀXw = Xᵀt`. Evidence:
expands `L`, names `C = XᵀX`. Reasoning: setting `∇L=0` gives the code's formula. Limits: needs
`XᵀX` symmetric/invertible — both hold here by construction.)

**Process (10):** notation/Kronecker stated (4); symmetry assumption explicit (3); legible (3).

### 2c. Inter-component weight (FLAGGED for ratification)

**Proposed: Code 60 % / Written 40 %.** Rationale (recorded hybrid rule — effort-proportional,
Bloom-checked, primary-objective dominant, rounded to 5s): the unit's **primary objective is
matrix-form regression** (the code), and the code carries the autograded outcome; the written half
is substantial (four derivations, comparable to the standalone hw7) but supporting. Effort is
roughly balanced (~45 min each), which is why this is **not** 70/30. **Alternative 55/45** is
defensible if you weight the derivation as co-equal. **Please ratify.**

---

## 3. Objective → rubric-row map (alignment contract)

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| A-O1 normal equation | Apply | Code: first-order tests | ✅ |
| A-O2 predict | Apply | Code: `test_prediction_2012` | ✅ |
| A-O3 second-order fit/compare | Analyze | Code: `test_second_order_improves`/`min_mse`/`shape` | ✅ |
| A-O4 interpret fit + stability | Evaluate | Code: Interpretation (CERL) | ✅ |
| B-O1…O4 four identities | Apply/Analyze | Written: per-step Id1–Id4 | ✅ |
| B-O5 identities → normal eqn; symmetry | Evaluate | Written: Interpretation (CERL) | ✅ |
| *(communication, both halves)* | — | Process rows | ✅ (cross-cutting) |

**Every objective maps to a row; none orphaned.**

---

## 4. Proposed diffs (per file — NOT applied)

### 4a. `hw.py` — `__main__`-guard the display/IO; keep graded globals at module scope (markers preserved)

The SOLUTION blocks (data load, `ones_vec`/`X`/`w`, `predict` body, `X_2`/`w_second_order`) are
**unchanged**. The graded globals (`w`, `winning_time_for_2012`, `w_second_order`) stay at module
scope (cheap solves) so the autograder can import them; the matplotlib import, the plotting, and the
three `print`s move into `main()` under `if __name__ == "__main__"`.

```diff
@@ (the plotting cell + the print cells + the appendix solve/print) @@
+def main():
+    from matplotlib import pyplot as plt
+    plt.style.use("ggplot")
+    test_x = np.linspace(1896, 2012, 100)
+    test_X = np.column_stack((np.ones_like(test_x), test_x))
+    plt.plot(x, t, 'o'); plt.plot(test_x, test_X @ w)
+    plt.xlabel("Year"); plt.ylabel("Winning time (s)")
+    print(winning_time_for_2012)
+    print(w_second_order)
+    print(np.linalg.solve(X.T @ X, X.T @ t))   # appendix: stable alternative to inv
+
+
+if __name__ == "__main__":
+    main()
```
(`import hw` measured **0.46 s → 0.040 s**; stdout no longer spams during collection.)

### 4b. `test_hw.py` — replace the three pinned-value tests with the 6-test property suite

```diff
-from hw import w, winning_time_for_2012, w_second_order
-def test_model_params():
-    assert w[0] == approx(36.4164559)
-    assert w[1] == approx(-0.0133308857)
-def test_prediction():
-    assert winning_time_for_2012 == approx(9.594713852048779)
-def test_second_order_fit():
-    assert w_second_order[0] == approx(455.597856)
-    assert w_second_order[1] == approx(-0.443160486)
-    assert w_second_order[2] == approx(0.000110151552)
+from hw import w, winning_time_for_2012, w_second_order
+def _design():
+    x, t = np.loadtxt("data100m.csv", delimiter=",", skiprows=1, unpack=True)
+    ones = np.ones_like(x)
+    return x, t, np.column_stack((ones, x)), np.column_stack((ones, x, x**2))
+def test_first_order_normal_equations():
+    x, t, X, _ = _design()
+    assert np.allclose(X.T @ (t - X @ w), 0.0, atol=1e-4)
+def test_first_order_matches_hw1():
+    assert w[0] == approx(36.41645590250286, rel=1e-3)
+    assert w[1] == approx(-0.013330885710960602, rel=1e-3)
+def test_prediction_2012():
+    assert winning_time_for_2012 == approx(9.594713852048779, rel=1e-4)
+    assert winning_time_for_2012 == approx(w @ np.array([1, 2012]))
+def test_second_order_improves():
+    x, t, X, X2 = _design()
+    assert np.mean((t - X2 @ w_second_order)**2) <= 0.9 * np.mean((t - X @ w)**2)
+def test_second_order_min_mse():
+    x, t, _, X2 = _design()
+    assert np.mean((t - X2 @ w_second_order)**2) == approx(0.03796, rel=2e-2)
+def test_second_order_shape():
+    assert np.asarray(w_second_order).shape == (3,)
```

### 4c. `hw.typ` — fix the Id1 typo (inside `#answer`); add Allowed-approaches + Required-interpretation (outside)

```diff
@@ Identity #1 reference (inside #answer) @@
-      dvp(, w_N) (w_N x_N + dots.c + w_N x_N),
+      dvp(, w_N) (w_1 x_1 + dots.c + w_N x_N),
@@ after the Kronecker property `sum_j delta_(i j) w_j = w_i` (outside #answer) @@
+#strong[Allowed approaches.] Either route in @tab:matrix_calc_identities earns full
+credit — explicit multiplication or the Kronecker-delta component form — as does any
+other valid derivation, provided each step is justified. For Identity #4 you must use
+the symmetry of $bold(C)$; say where. A bare final answer earns only the result step.
+Grading criteria are in #emph[rubric.md].
@@ after the solution #answer, before "= Workload" @@
+= Interpretation
+#strong[Required interpretation.] After the four derivations, add one short paragraph
+(no new algebra): which identity gives the gradient of the least-squares loss
+L = (t − Xw)ᵀ(t − Xw), and how setting that gradient to zero yields the normal equation
+ŵ = (XᵀX)⁻¹Xᵀt you implemented in the lab? State where Identity #4's symmetry assumption
+is satisfied here.
+#answer([ <reference paragraph: ∇L uses Id2 + Id4 with C = XᵀX (symmetric) ⇒ XᵀXw = Xᵀt> ], [])
```

### 4d. `README.md` — replace the 1/0.5/0 gate with the hybrid criteria table (both components + inter-weight); 8-part framing above the instructions.

### 4e. `make_release` — ship `rubric.md` (markers already preserved)

```diff
 cp test_hw.py release
 cp README.md release
+cp rubric.md release
```
(Existing `sed` solution-strip + `make without_answers` unchanged; the `main()` guard and the Id1
fix ship correctly — guard is outside markers, Id1 fix is inside `#answer` so it stays the key.)

### 4f. `rubric.md` — NEW file: §2a + §2b + §2c verbatim, prefaced with the splits and specs policy.

---

## 5. Effort & budget

| Component | Change |
|-----------|--------|
| Code lab | unchanged (~30–40 min) |
| Code reflection | **+~15 min** (new) |
| Written derivations | unchanged (~40–50 min) |
| Written interpretation | **+~10 min** (new) |
| Net | within 5–6 hrs/week; import-time fix speeds the autograder |

---

## 6. Judgment calls beyond the spec

1. **Second-order coefficient pins removed** (the key defect): `cond(X₂ᵀX₂) ≈ 2.1e20`, residual
   `1.35` on the `x²` column — pinning 9 sig figs tests LAPACK rounding and penalizes the *more*
   stable `solve`/`lstsq` the appendix recommends. Replaced with the method-independent MSE +
   improvement tests. **Flagged.**
2. **Id1 display typo fixed** inside `#answer` (the `∂/∂w_N` line); result was already correct.
3. **Import-time work guarded** via `main()`, keeping the graded globals at module scope (the test
   contract is module globals, not functions — preserved to minimize churn).
4. **Inter-component weight 60/40 flagged** for ratification (alt 55/45).
5. **Through-lines:** first-order `w` **= hw1's** OLS fit (a test enforces it); the written
   identities **prove the code's normal equation** (the interpretation couples the halves); the four
   identities **overlap hw7's Jacobian identities** (`∇ Cw`) — a Scope-B consolidation candidate
   alongside hw1/hw2/hw3.
6. **Interpretation as a markdown cell** (code) + one paragraph (written), per framework default.

---

## 7. Validation results (against the reference; repo `.venv`)

- **Code key re-derived:** first-order `w` and `winning_time_for_2012` reproduce the pins exactly;
  second-order coeffs reproduce but **`cond=2.09e20`**, residual `1.35` on `x²` → coeff pin unsafe;
  MSE₂ = 0.03796 and MSE₂ < MSE₁ (0.0380 < 0.0503) are stable. ✅
- **Written key:** all four identities verified symbolically (sympy); Id4 = `2Cw` for symmetric `C`
  (general `(C+Cᵀ)w`); Id1 intermediate line mis-typeset (fixed). ✅
- **New code suite vs reference:** **6 passed in 0.04 s.** ✅
- **Import-time fix:** `import hw` **0.46 s → 0.040 s**; globals still importable. ✅
- **Mutation-tested guards:**
  | Injected model | Tests that correctly FAIL |
  |----------------|---------------------------|
  | quadratic = padded line `[w0,w1,0]` | `second_order_improves`, `second_order_min_mse` |
  | intercept-only first-order | `first_order_matches_hw1`, `prediction_2012`, `first_order_normal_equations` |
  | wrong 2012 prediction | `prediction_2012` |
  | reference (correct) | none — all 6 pass ✅ |
- **Written strip check** (bracket-depth simulator, no compile): solution + reference interpretation
  stripped; title, Allowed-approaches, Required-interpretation, Workload, Acknowledgments retained;
  Id1 typo fixed; 2 `#answer` blocks. ✅

---

## 8. Proposed commit message (when applied — do NOT commit now)

```
hw2 overhaul: property tests + reflections for matrix regression & matrix-calc derivations (hybrid type-1)

Two separate deliverables (autograded code + hard-copy written derivation), hw6
type-1 pattern. Inter-component weight 60 code / 40 written — FLAGGED for ratification.

Code component (internal 55/35/10):
- test_hw.py: replace 3 pinned-value tests with 6 independent property/outcome tests
  (Correctness 55 = 10/10/8/12/10/5): first-order normal equations, matches-hw1
  closed form (rel=1e-3), 2012 prediction (value + consistency), second_order_improves
  (floor-AND-guard), second_order_min_mse, shape. REMOVES the second-order COEFFICIENT
  pins: cond(X2^T X2)=2.1e20, residual 1.35 on the x^2 column — the pins tested LAPACK
  rounding and penalized the more-stable solve/lstsq the appendix recommends; MSE and
  predictions are the method-independent invariants. Mutation-tested; 6/6 vs reference,
  0.04s.
- hw.py: move matplotlib + plotting + the three prints into main() under
  `if __name__ == "__main__"`; graded globals (w, winning_time_for_2012,
  w_second_order) stay at module scope (the autograder imports globals). SOLUTION
  markers unchanged. import hw: 0.46s -> 0.040s.
- rubric.md: code Interpretation 35 = CERL (does the quadratic help; conditioning ->
  why solve/lstsq over inv); Process 10.

Written component (internal 60/30/10):
- hw.typ: fix an Identity #1 display-typo (d/dw_N line expanded the wrong sum; result
  unchanged) inside #answer; add Allowed-approaches + Required-interpretation prompts
  outside #answer and a reference-interpretation #answer block. Strip validated.
- rubric.md: per-step Correctness 60 = Id1/Id2/Id3/Id4 = 14/8/14/24 (Id4 heaviest;
  load-bearing step = the C=C^T symmetry collapse (C+C^T)w -> 2Cw). All four identities
  verified symbolically. Interpretation 30 = CERL (identities -> normal equation;
  locate symmetry); Process 10.

- README.md: 8-part framing + hybrid criteria table; replaces 1/0.5/0.
- make_release: also ships rubric.md (sed strip + make without_answers unchanged).
- through-lines: first-order w == hw1 OLS fit (enforced by a test); the written
  identities prove the code's normal equation (interpretation couples the halves);
  the 4 identities overlap hw7's Jacobians (Scope-B consolidation candidate).

Reference math verified (code + 4 identities). Autograder: 6 tests, 0.04s, import 0.040s.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
