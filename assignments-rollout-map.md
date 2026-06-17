# INFO 521 — Homework Overhaul Rollout Map (STEP 1)

Enumerates every assignment **not yet overhauled** (all except the three pilots hw3, hw5,
hw16) and assigns each: current grading mechanism, the closest pilot pattern, the resulting
split per the recorded rule, the specific defects to fix, and a recommended overhaul order.

**Recorded split rule** (`rubric.md`, `CHANGELOG.md`): autograded HWs → **55/35/10**;
written/derivation HWs → **60/30/10** (correctness machine- vs human-verified).

**Pilot patterns (reference instances):**
- **code-outcome** = `hw3` — autograded code; outcome/property tests; floor-and-guard; 55/35/10.
- **written-derivation** = `hw5` — pure math derivation; per-step + CERL rubric; 60/30/10.
- **stochastic** = `hw16` — RNG/sampling; distributional recovery + degeneracy guards; seed+tolerance sweep; 55/35/10.
- **hybrid** = code (test_hw.py) **plus** a written/caption part; autograded → 55/35/10, the written sub-part folds into the Interpretation/derivation rubric.

**Marker conventions to preserve** (do not chase the toolchain; author prose as markdown):
- Python: `### SOLUTION START ### / ### SOLUTION END ###` (stripped by `make_release` sed).
- LaTeX `.tex` (hw6/10/11): `%%% Answer START %%% / %%% Answer END %%%`.
- Typst `.typ` (hw7/8/9/12/13): `#answer([...], [])` macro + `make without_answers`
  (`typst compile … --input show_answers=false`). **No `%%% %%%` markers in these.**

---

## The map

| # | Title | Current grading | Closest pilot | Split | Specific defects to fix |
|---|-------|-----------------|---------------|:-----:|--------------------------|
| **hw0** | Python basics + LaTeX onboarding | hybrid: trivial `test_add` + `.tex` checkboxes/calculus; 1/0.5/0 | code-outcome (light) | 55/35/10 | 1/0.5/0 gate; single trivial test; onboarding HW — **non-representative, light touch only** (TILT + drop the gate; don't over-engineer). |
| **hw1** | Simple linear regression (1D least squares) | autograded `test_hw.py`; 1/0.5/0 | code-outcome | 55/35/10 | magic-constant pins (`w0==36.4164…`, `w1==-0.0133…`); **import-time work** (data load, 2D/3D plots, `model.train`, predict+print at module scope); no graded interpretation (worksheet derivation is separate/ungraded); 1/0.5/0. |
| **hw2** | Linear regression, matrix form / polynomial | autograded; 1/0.5/0 | code-outcome | 55/35/10 | magic-constant pins (`w[0]`, `w[1]`, `pred==9.5947…`, 2nd-order coeffs); **import-time work** (loads, fits, plots, prints at module scope); ungraded inline "what are the dimensions of X?"; 1/0.5/0. **Overlaps hw3 (polynomial regression) → consolidation candidate.** |
| **hw4** | Poisson probabilities (PMF) | autograded; 1/0.5/0 | code-outcome | 55/35/10 | 1/0.5/0 gate; only 2 closed-form scalar tests (thin — add property tests: pmf∈[0,1], complement/normalization, floor-and-guard); no interpretation. **No import-time work, no RNG — cleanest code HW.** |
| **hw6** | Monte Carlo approximation of an expectation | hybrid: code `test_hw.py` + `.tex` analytic part; 1/0.5/0 | **stochastic** | 55/35/10 | **pinned-RNG test** (`expectations[0:10]` and `expectations[-1]==17.7139…` pin the running-mean RNG stream); seeded `default_rng(100)` but graded on exact draws; 1/0.5/0; analytic E[X] + plot caption exist but are gate-graded (fold to derivation+CERL). |
| **hw7** | Practice with Jacobians (matrix calculus) | written-only `.typ`; 1/0.5/0 | written-derivation | 60/30/10 | 1/0.5/0 gate; purely mechanical, no interpretation; `#answer()` Typst markers (preserve). |
| **hw8** | Gaussian manipulation (independence, MLE unbiasedness, Beta mean/var) | written-only `.typ`; 1/0.5/0 | written-derivation | 60/30/10 | 1/0.5/0 gate; 4 derivations, no interpretation/"when does it hold"; `#answer()` markers. **Ex. 2 explicitly builds on hw5's MLE (through-line).** |
| **hw9** | Fisher Information for the Bernoulli | written-only `.typ`; 1/0.5/0 | written-derivation | 60/30/10 | 1/0.5/0 gate; single mechanical derivation, no interpretation; `#answer()` markers. **Smallest written HW — cleanest written representative.** |
| **hw10** | Predictive variance (error bars) | hybrid: code + `.tex` captions; 1/0.5/0 | code-outcome (+hybrid) | 55/35/10 | magic-constant pins (`predictive_variance(0.5)==0.03333…`, full `cov_w` matrix); **heavy import-time work** (3 loops writing 12 PDFs to `images/`); 1/0.5/0; captions are the written interp (fold to CERL). Graded quantities are closed-form (deterministic) → keep exact w/ rel headroom + add PSD/property. |
| **hw11** | Exact Bayesian inference (coin game) | hybrid: code + `.tex`; grading already "1 pt for a reasonable explanation" | code-outcome (+hybrid) | 55/35/10 | pins **full 100-element arrays** (`R_POSTERIOR_*`) + scalars (closed-form Beta posteriors); replace with closed-form points + shape/normalization property; explanation currently informally graded → formalize as CERL. **Already `__main__`-guarded (no import-time defect).** |
| **hw12** | Prior on noise variance σ² (Inverse-Gamma conjugacy) | written-only `.typ`; 1/0.5/0 | written-derivation | 60/30/10 | 1/0.5/0 gate; mechanical conjugate-prior derivation, thin interpretation; `#answer()` markers. |
| **hw13** | Drawing probabilistic graphical models (PGM) | written-only `.typ`; 1/0.5/0 | written-derivation (adapted) | 60/30/10 | 1/0.5/0 gate; **not a derivation — a diagramming task**; per-step rubric must be adapted to nodes/edges/plate correctness + a conditional-independence interpretation. **Judgment call flagged.** |
| **hw14** | Bayesian logistic regression — MAP (Newton-Raphson) | autograded + hard-copy written; 1/0.5/0 | code-outcome | 55/35/10 | magic-constant pin on the post-Newton `w==[1.6399,1.9998]` (deterministic optimization → make a recovery floor: `‖grad‖<tol` at MAP and/or `w` within tol **+ beats-prior guard**); **import-time work** (loads, Newton loop, contour plots); 1/0.5/0; no graded interpretation. **Through-line: MAP → Laplace (hw15) → MCMC (hw16).** |
| **hw15** | Laplace approximation | autograded + hard-copy written; 1/0.5/0 | code-outcome (stochastic-adjacent) | 55/35/10 | magic-constant pins (`w_MAP`, `g_cov`) — closed-form, keep exact w/ rel headroom + add symmetric-PSD property; **unseeded RNG at import** (`np.random.multivariate_normal(…,100000)` at module scope, no seed) → reproducibility + budget blowup; import-time plots; 1/0.5/0. |
| **hw17** | Estimating π with Monte Carlo (curse of dimensionality) | autograded only | **stochastic** | 55/35/10 | **`import`-breaking: test imports `estimate_pi_using_sphere` which is not defined in `hw.py`** (ImportError); **unseeded RNG** (`RNG=np.random.default_rng()` — no seed → non-reproducible); **catastrophic import-time budget** (`plot_samples_needed()` runs at module scope ≈ 22M samples + writes `estimates.pdf`); convergence tests are bare thresholds with **no floor-AND-guard** (a function returning the constant π would pass); no interpretation. |

> Pilots already done (not rows above): **hw3** (code-outcome), **hw5** (written-derivation),
> **hw16** (stochastic).

---

## Recommended overhaul order

Lead with the **cleanest representative of each pattern** (proves the pattern with minimal
noise), then batch the rest within each pattern from cleanest to messiest.

**Representatives first (one per pattern):**
1. **hw4** — code-outcome, cleanest: closed-form, no import-time work, no RNG.
2. **hw9** — written-derivation, cleanest: single short derivation.
3. **hw6** — stochastic, cleanest: one pinned-RNG test, an obvious distributional-recovery target (E[X] vs analytic) and degeneracy guard.
4. **hw11** — hybrid/Bayesian, cleanest: closed-form, **already `__main__`-guarded**; exercises formalizing an informal "explanation" grade into CERL.

**Then, by pattern (ascending messiness):**
5. **hw7** → 6. **hw8** → 7. **hw12** → 8. **hw13** *(written cluster; hw13 last — diagram task needs an adapted rubric)*.
9. **hw1** → 10. **hw2** *(code-outcome with import-time work; hw2 pairs with hw3 for consolidation)*.
11. **hw10** *(hybrid, heavy import-time PDF loops)*.
12. **hw14** → 13. **hw15** *(Bayesian through-line into hw16; hw15 has the unseeded-import sampling defect)*.
14. **hw17** *(stochastic, but needs a missing function implemented, seeding added, a floor-AND-guard, and a massive import-time fix — most work)*.
15. **hw0** *(onboarding; light-touch last — drop the gate, add TILT, do not over-engineer)*.

**Rationale for the tail positions:** hw2 deferred next to hw3's pattern so the
polynomial-regression consolidation can be considered together; hw14/hw15 deferred so the
MAP→Laplace→MCMC through-line is overhauled as a unit feeding the finished hw16; hw17 last
among code HWs because it is the only one with a correctness-breaking missing function plus
the worst import-time budget; hw0 last because it is onboarding, not a representative analysis
task.

---

## Cross-cutting notes (apply during STEP 2)

- **Import-time budget** is the most common code defect (hw1, hw2, hw10, hw14, hw15, hw17):
  `__main__`-guard every top-level driver/plot so `import hw` is cheap (the hw16 fix).
- **Magic-constant pins on deterministic quantities** (hw1, hw2, hw10, hw14, hw15) are *not*
  RNG-fragile but are still brittle/all-or-nothing: convert to closed-form-with-rel-headroom
  **plus** independent property tests (shape, PSD, normalization, beats-baseline) for partial
  credit and a guard.
- **True pinned-RNG** appears in hw6 (running-mean stream); hw17 is unseeded (opposite
  problem). Both need the seed + tolerance-sweep + degeneracy-guard treatment.
- **Through-lines to preserve:** hw8-Ex2 → hw5 (MLE); hw14→hw15→hw16 (MAP→Laplace→MCMC).
  Keep reference values consistent (note: hw14/hw15 MAP/mode ≈ `[1.64, 2.00]` is the
  posterior **mode**, distinct from hw16's posterior **mean** — do not conflate).
- **Consolidation candidate:** hw1/hw2/hw3 are all least-squares/polynomial regression; flag
  for the Scope-B consolidation map, not a STEP-2 merge.
- **Written HWs keep their medium**; per the format note, author all prompt/criteria/
  interpretation prose as markdown in `OVERHAUL.md` (and `README.md`), keep `rubric.md` as the
  durable artifact, and do **not** compile `.typ`/`.tex`.
- **classroom.yml / autograder workflow:** for written-only HWs (hw7/8/9/12/13/13) there is no
  `test_hw.py`; neutralize the autograder wiring rather than orphan it (STEP-2 item 5).
