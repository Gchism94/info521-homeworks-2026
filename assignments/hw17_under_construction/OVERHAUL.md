# hw17 — Overhaul draft (HYBRID type-1 · stochastic Monte-Carlo-π code + written derivations)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw17 (estimating π by sampling; the curse of
dimensionality). **Stochastic** code (hw16/hw6 pattern) **plus** a hard-copy written derivation
(`hw.typ`). **Draft only — diffs proposed, not applied.** Directory is `hw17_under_construction`.

> **STEP 0 — classification: HYBRID type-1, stochastic code.** Autograded Monte-Carlo estimators +
> a hard-copy written derivation/interpretation. Inter-component weight **60 code / 40 written**
> (FLAGGED, §2c).

> **⚠️ AUDIT BLOCKER (must fix first).** `test_hw.py` does
> `from hw import (estimate_pi_using_circle, estimate_pi_using_sphere, estimate_pi_using_n_ball)`,
> but **`estimate_pi_using_sphere` is not defined in `hw.py`** → `ImportError` → **the whole suite
> fails to collect**. Additionally `hw.py` does `import mplcursors` (unused, **not in
> requirements.txt** → second ImportError) and calls `plot_samples_needed()` at module scope
> (**~220M samples** = 11 dims × 200 trials × 100000 + a PDF write), which runs *during pytest
> collection* and hangs it. **None of the new tests mean anything until the suite collects** — these
> three fixes are part of the overhaul, not optional.

---

## 0. Reference-correctness audit

**Code:** verified the math of every estimator (seed sweep, 40 seeds, below). The **missing
`estimate_pi_using_sphere`** is implemented as the natural 3-D estimator: a point in `[0,1]³` is
accepted with probability `(1/8)(4/3 π) = π/6`, so `π ≈ 6 · (accepted/total)` — consistent with the
written 3-D derivation (`π = 6 V_oct`). Verified it converges to π. ✅

**Written key:** 3-D `π = 6 V_oct` ✅; n-D `π = (2ⁿ V_o Γ(n/2+1))^(2/n)` ✅. **Two genuine errors:**
1. **Title says "Homework 16"** (line 7) — should be Homework 17. Fix.
2. **2-D quadrant-area formula is wrong** (line 51): it writes the quadrant area as
   `∫∫(x²+y²) dx dy`. The quadrant area is the *measure* of `{x²+y²<1, x,y∈[0,1]}` = `π/4`
   (estimated by the accepted fraction), **not** the integral of `(x²+y²)`. The prose procedure
   right after it is correct; only the formula line is wrong. **Fix** the formula inside `#answer`.
3. (Minor) line 87 "like we did with the sphere" → "circle". Optional.

---

## 1. Prompt rewritten into the 8-part template (markdown → `README.md`)

**1. Context & purpose.** Estimate π by rejection sampling in 2-D, 3-D, and n-D, then watch the
**curse of dimensionality**: the acceptance rate (orthant volume / cube volume) collapses with
dimension, so the same accuracy costs exponentially more samples — all at the universal
`O(1/√N)` Monte-Carlo rate.

**2. Learning objectives** (Bloom + graded row):
- *Code* **A-O1** *Implement* `estimate_pi_using_circle` (2-D). *(Apply — Correctness: circle)*
- *Code* **A-O2** *Implement* `estimate_pi_using_sphere` (3-D). *(Apply — Correctness: sphere)*
- *Code* **A-O3** *Implement* `number_of_orthants` + `estimate_pi_using_n_ball` (running). *(Apply
  — Correctness: orthants, n-ball contract)*
- *Code* **A-O4** *Demonstrate & interpret* the curse of dimensionality. *(Evaluate — Interpretation)*
- *Written* **B-O1…O3** *Derive* the 2-D/3-D/n-D estimators. *(Apply/Analyze — Written Correctness)*
- *Written* **B-O4** *Explain* the log-log convergence plot. *(Evaluate — Written Interpretation)*

**3. The task.** Implement the four estimators; **seed the RNG**; generate the convergence plot.
**Any correct sampler passes** (the tests check convergence + use-of-randomness, not an exact stream).

**4. What you may / may not use.** Any NumPy RNG; **seed it** (`default_rng(seed)`). No hard-coded
π (the tests reject a constant).

**5. How you'll be assessed.** §2 — convergence/property tests with floor-AND-guard (code), per-step
rubric (written).

**6. Required interpretation.** *Code/Written:* describe the log-log MAE-vs-N plot — the common
`−1/2` slope (`O(1/√N)`) and why higher dimensions sit higher (acceptance rate `∝` orthant volume
falls with `n`).

**7. Going further (optional).** Estimate, per dimension, the N needed for `|π̂−π|<0.1`.

**8. Submission & reproducibility.** **Seed `default_rng`.** Autograder imports the four estimators;
`import hw` must be cheap — `plot_samples_needed()` runs **only** under `if __name__ == "__main__"`.

---

## 2. `hw17/rubric.md` — two components at their canon splits

### 2a. Component A — Code (Monte-Carlo π), internal **55 / 35 / 10**

**Correctness (55) — autograded** (validated 6/6; seed-swept 40 seeds, 0 failures; mutation-tested):

| Test | Obj | Pts | Checks |
|------|-----|:---:|--------|
| `test_number_of_orthants` | A-O3 | 6 | `2ⁿ` for `n=1..5` |
| `test_circle_converges` | A-O1 | 10 | `estimate_pi_using_circle(1e5) ≈ π` (`rel=0.02`) |
| `test_circle_is_stochastic_not_constant` | A-O1 | 9 | **guard:** two draws differ, both in (3.0, 3.3) — a hardcoded π fails |
| `test_sphere_converges` | A-O2 | 10 | `estimate_pi_using_sphere(1e5) ≈ π` (`rel=0.02`) |
| `test_n_ball_running_contract` | A-O3 | 10 | length `n_samples−1`; last ≈ π (`rel=0.1`) |
| `test_convergence_improves_with_n` | A-O1 | 10 | **floor-AND-guard:** mean `|err|` at `N=5e4` < at `N=50` and `<0.05` |

**Sum = 55.** The map's "a function returning constant π would pass" hole is closed: the
**stochastic guard** + **convergence-improves** floor-AND-guard both reject a constant (mutation-
verified — see §7). Seeded; the seed sweep confirms the tolerances hold for any seed.

**Interpretation (35) — CERL** on the curse-of-dimensionality reading. PASS = ≥2 each
(Claim: slope ≈ −1/2 / higher-D worse; Evidence: cites the plot/orthant acceptance; Reasoning:
`O(1/√N)` + acceptance `∝ V_o`; Limits: where sampling becomes infeasible).

**Process (10):** **seeded RNG** + `import hw` cheap (no 220M-sample plot at import) (4); plot
labeled, log-log (3); docstrings intact (3).

### 2b. Component B — Written (2-D/3-D/n-D derivations), internal **60 / 30 / 10**

**Correctness (60) — per-step derivation rubric:**

| Step | Obj | Pts | Exemplary |
|------|-----|:---:|-----------|
| **A · 2-D** | B-O1 | 18 | `r=1 ⇒ A=π`; `π = 4 ·` (accepted fraction = quadrant area) |
| **B · 3-D** | B-O2 | 18 | `V=4/3π ⇒ π = 3V/4 = 6 V_oct`; accept `‖x‖<1` in `[0,1]³` |
| **C · n-D** | B-O3 | 24 | `V_n = π^{n/2}/Γ(n/2+1)` ⇒ `π = (2ⁿ V_o Γ(n/2+1))^{2/n}` |

**Sum = 60. C heaviest** (the general orthant inversion). Each step graded on the validity of the
inversion `volume → π`; any valid route full credit.

**Interpretation (30) — CERL** on the curse-of-dimensionality plot (slope, dimension ordering, why).

**Process (10):** notation, `V_o`/orthant defined, legible (incl. the corrected 2-D area).

### 2c. Inter-component weight (FLAGGED) — **Code 60 % / Written 40 %**

Code is the autograded deliverable (and the blocker fix); the written derivations parallel and
motivate it. **Alternative 55/45.** PENDING-RATIFICATION.

---

## 3. Objective → rubric-row map

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| A-O1 2-D estimator | Apply | Correctness: circle_converges, stochastic, convergence_improves | ✅ |
| A-O2 3-D estimator | Apply | Correctness: sphere_converges | ✅ |
| A-O3 orthants + n-ball | Apply | Correctness: orthants, n_ball_contract | ✅ |
| A-O4 curse (demonstrate) | Evaluate | Code Interpretation | ✅ |
| B-O1…O3 derivations | Apply/Analyze | Written Correctness A–C | ✅ |
| B-O4 curse (explain) | Evaluate | Written Interpretation | ✅ |
| *(communication)* | — | Process rows | ✅ |

**Every objective maps to a row; none orphaned.**

---

## 4. Proposed diffs (per file — NOT applied)

### 4a. `hw.py` — BLOCKER fixes + seed + import guard (markers preserved)

```diff
-import mplcursors                      # unused, not in requirements -> ImportError on collection
-from matplotlib import pyplot as plt   # move into plot_samples_needed (only user)
-from tqdm import tqdm                   # move into plot_samples_needed
-RNG = np.random.default_rng()           # UNSEEDED -> non-reproducible
+RNG = np.random.default_rng(521)        # seeded
+
+def estimate_pi_using_sphere(n_samples: int) -> float:
+    """3-D: a point in [0,1]^3 is accepted with prob pi/6, so pi ~ 6 * accepted/total."""
+    ### YOUR CODE HERE ###
+    ### SOLUTION START ###
+    samples = RNG.uniform(0, 1, (3, n_samples))
+    accepted = np.sum(samples**2, axis=0) < 1
+    return 6 * (accepted.sum() / n_samples)
+    ### SOLUTION END ###
@@ end of file @@
-plot_samples_needed()
+if __name__ == "__main__":
+    plot_samples_needed()
```
(Inside `plot_samples_needed`, add `from matplotlib import pyplot as plt` and `from tqdm import
tqdm`.) After the fix the suite **collects and runs**; `import hw` is sub-second.

### 4b. `test_hw.py` — the 6-test convergence/property/guard suite (§2a, validated). Keeps the
existing `estimate_pi_using_sphere` import (now satisfied) and the circle/n-ball imports.

### 4c. `hw.typ` — fix the title `Homework 16 → 17`; fix the 2-D quadrant-area formula inside
`#answer` (`∫∫(x²+y²)dxdy` → the measure of `{x²+y²<1}`, i.e. the accepted-fraction × 1 = π/4); add
Allowed-approaches + Required-interpretation prompts (outside `#answer`).

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
| Code (4 estimators) | +1 (sphere, ~10 min) |
| Code reflection | folded into the existing curse section |
| Written derivations | unchanged (~30 min) |
| Net | within budget; the 220M-sample import is removed (was a multi-minute hang) |

---

## 6. Judgment calls beyond the spec

1. **Blocker fixed three ways** (implement `estimate_pi_using_sphere`; drop the unused
   `mplcursors`; guard `plot_samples_needed()` under `__main__`) — the suite now collects.
2. **`estimate_pi_using_sphere` implemented** (not the import removed): the test, the markdown's
   3-D section, and the written 3-D derivation all expect a 3-D estimator (`π ≈ 6·accepted/total`).
3. **RNG seeded** (`default_rng(521)`); seed-swept to confirm tolerances.
4. **Constant-π hole closed** by the stochastic guard + convergence floor-AND-guard.
5. **Written key fixes:** title `16→17`; the wrong 2-D quadrant-area formula. Math otherwise
   verified correct.
6. **Type-1 hybrid, weight 60/40** (code primary). PENDING-RATIFICATION.
7. **Through-line:** hw16 (MCMC) and hw17 close the stochastic arc; the curse-of-dimensionality
   ties Monte-Carlo error to dimension.

---

## 7. Validation results (against the reference; repo `.venv`)

- **Blocker:** original suite **fails to collect** (`estimate_pi_using_sphere` ImportError +
  `mplcursors` ImportError + the 220M-sample `plot_samples_needed()` at import). After the fix:
  **collects and runs**, `import hw` sub-second. ✅
- **Code key:** `estimate_pi_using_sphere` derived/verified (`π ≈ 6·accepted/total`); all estimators
  converge to π. ✅
- **New suite vs reference:** **6 passed in 0.11 s.** ✅
- **Seed sweep (40 seeds):** `{circle:0, sphere:0, nball:0, converge:0}` failures — tolerances hold
  for any seed. ✅
- **Mutation-tested guards:**
  | Injected | Tests that correctly FAIL |
  |----------|---------------------------|
  | `circle ≡ π` (constant) | `circle_is_stochastic_not_constant`, `convergence_improves_with_n` |
  | `circle ≡ 3.0` | converges, stochastic, convergence_improves |
  | `number_of_orthants ≡ n` | `number_of_orthants`, `n_ball_running_contract` |
  | `circle ≡ 4·0.5` (ignores samples) | converges, stochastic, convergence_improves |
  | `n_ball` wrong length | `n_ball_running_contract` |
  | reference | none — all 6 pass ✅ |
- **Written key:** 3-D/n-D derivations verified; title + 2-D-area errors flagged for fix.

---

## 8. Proposed commit message (this commit)

```
hw17 overhaul: collection-blocker fix + convergence/guard tests for Monte-Carlo pi (stochastic hybrid)

AUDIT BLOCKER FIXED: test_hw.py imported estimate_pi_using_sphere, which hw.py never
defined -> ImportError -> the whole suite failed to collect. Also: `import mplcursors`
(unused, not in requirements -> 2nd ImportError) and a module-scope plot_samples_needed()
call (~220M samples: 11 dims x 200 trials x 100000 + a PDF) that runs during pytest
collection and hangs it. All three fixed -- the suite now collects and runs before any
new test means anything.

Code component (internal 55/35/10, stochastic):
- hw.py: implement estimate_pi_using_sphere (3-D: pi ~ 6*accepted/total, matching the
  written 3-D derivation pi=6 V_oct); drop the unused mplcursors import; move
  matplotlib/tqdm imports into plot_samples_needed; SEED the RNG (default_rng(521),
  was unseeded); guard plot_samples_needed() under `if __name__ == "__main__"`.
  import hw: hang -> sub-second.
- test_hw.py: 6 convergence/property tests (Correctness 55 = 6/10/9/10/10/10):
  number_of_orthants, circle_converges (rel=0.02), circle_is_stochastic_not_constant
  (GUARD: two draws differ -> a hardcoded pi fails), sphere_converges, n_ball running
  contract (length n_samples-1), convergence_improves_with_n (floor-AND-guard: mean
  |err| shrinks with N -> a constant can't). Closes the map's "constant pi would pass"
  hole. Seed sweep (40 seeds) 0 failures; mutation-tested (constant pi, constant 3.0,
  orthants=n, sample-ignoring, wrong length all fail); 6/6 vs reference, 0.11s.
- rubric.md: Interpretation 35 = CERL (curse of dimensionality: O(1/sqrt(N)) slope,
  acceptance falls with dimension); Process 10 (seeded, cheap import).

Written component (internal 60/30/10):
- hw.typ: FIX title "Homework 16" -> 17; FIX the 2-D quadrant-area formula in #answer
  (it wrote the area as the integral of x^2+y^2; the quadrant area is the measure of
  {x^2+y^2<1} = pi/4, the accepted fraction). 3-D (pi=6 V_oct) and n-D
  (pi=(2^n V_o Gamma(n/2+1))^(2/n)) derivations verified correct -> unchanged. Add
  Allowed-approaches + Required-interpretation prompts.
- rubric.md: per-step Correctness 60 = A/B/C = 18/18/24 (C the n-D orthant inversion,
  heaviest); Interpretation 30 = CERL (curse plot); Process 10.

- README.md: 8-part framing + hybrid criteria table; replaces 1/0.5/0.
- make_release: ships rubric.md.

FLAGS: inter-component weight 60/40 pending ratification; directory is
hw17_under_construction.

Reference math verified (estimators + 3-D/n-D derivations). Autograder: 6 tests, 0.11s,
import sub-second (was a hang).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
