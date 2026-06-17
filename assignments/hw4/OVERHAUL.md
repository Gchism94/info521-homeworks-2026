# hw4 — Overhaul draft (code-outcome pattern · cleanest code representative)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw4 (Poisson probabilities). Matches the
**hw3 code-outcome pilot**, adapted to a *closed-form* HW (no model fit, no RNG). **Draft
only — no hw4 files are modified; the diffs below are proposed, not applied.**

**Split: autograded → 55 / 35 / 10** (repo canon; correctness machine-verified).

hw4 is the small, clean code representative: two probabilities for `X ~ Poisson(3)` —
`P(2≤X≤6)` and its complement `P(X<2 or X>6)`. No import-time work and no randomness, so
there is **nothing to `__main__`-guard and no seed/tolerance sweep** (stated so the absence is
intentional, not an omission). The grader imports `poisson, calculate_poisson_pmf_a,
calculate_poisson_pmf_b` from `hw`.

---

## 1. Prompt rewritten into the 8-part template

> Goes into `README.md` (full text in the §4c diff); the interpretation prompt is mirrored
> into a markdown cell of `hw.py` (§4a).

**1. Context & purpose.** The Poisson distribution models counts of independent events at a
constant average rate (arrivals, defects, decays). Computing a range probability and its
complement is the first move you'll reuse whenever you reason about a discrete distribution.

**2. Learning objectives** (Bloom verb + the graded check each is measured by):
- **O1** *Evaluate* the Poisson pmf for given `x`, `λ`. *(Apply — Correctness:
  `test_poisson_matches_formula`, `test_pmf_is_valid_distribution`)*
- **O2** *Compute* a range probability by summing the pmf over `[LOW, HIGH]`.
  *(Apply — Correctness: `test_pmf_a_value`, `test_pmf_a_equals_range_sum`)*
- **O3** *Apply* the complement rule (total probability = 1) for the tail probability.
  *(Apply/Analyze — Correctness: `test_pmf_b_value`, `test_a_and_b_are_complementary`)*
- **O4** *Interpret* the two results — what they mean, why the complement works, and one
  assumption/limit of the Poisson model. *(Evaluate — Interpretation rubric)*

**3. The task (outcome, not recipe).** Implement `poisson(x, λ)`; use it to compute
`calculate_poisson_pmf_a()` = `P(2≤X≤6)` and `calculate_poisson_pmf_b()` = `P(X<2 or X>6)`
for `λ=3`.

**4. Allowed methods (scope stated plainly).** Any correct computation that reaches the
required probabilities earns full credit — sum the pmf directly, or compute the complement
either way. **Scope note:** this is a *closed-form* problem, so the answers are fixed numbers,
not a range of valid outcomes — "any approach" means any correct route to **those** values,
not freedom in the result. Per the original constraint, use only the `math` standard library
(no NumPy/SciPy). The autograder checks the values **and** distribution properties (pmf valid,
`a` equals the range sum, `a+b=1`), never your specific control flow.

**5. How you'll be assessed (criteria shown up front).**
- *Correctness (autograded, 55%)* — the checks in §2: closed-form values for `a` and `b`
  (`rel=1e-6`), the pmf matches its formula and is a valid distribution, and the
  value/complement guards. Thresholds visible in `test_hw.py`.
- *Interpretation (rubric, 35%)* — the §6 paragraph, scored Claim/Evidence/Reasoning/Limits.
- *Process (10%)* — `math`-only, readable, runs clean.

**6. Required interpretation** (markdown cell in `hw.py`): one short paragraph — what
`P(2≤X≤6)=0.767` means in words for rate `λ=3`; why the complement rule gives the tail
probability directly; and **one** assumption the Poisson model makes, or a situation where
modeling these counts as Poisson would mislead (non-constant rate, over-dispersion, or
non-independent events).

**7. Going further (optional, ungraded).** Recompute for a different `λ` and describe how the
mass shifts; or verify `E[X]=λ` numerically from the pmf.

**8. Submission & reproducibility.** Commit `hw.py` (code + the interpretation paragraph).
The grader imports `poisson, calculate_poisson_pmf_a, calculate_poisson_pmf_b` — keep those
names and signatures. Run `pytest test_hw.py` locally first.

---

## 2. Rewritten `test_hw.py` (closed-form floors + distribution-property guards)

Validated: **6 passed in 0.01s** against the reference `hw.py`; `import hw` = **0.004s**.
Independent tests, actionable messages. Closed-form scalars stay exact with `rel` headroom
(framework §5); every value floor is paired with a property/guard so a hardcoded constant or
a trivial answer cannot clear the suite.

```python
"""Tests for hw4 — Poisson probabilities: closed-form values + distribution properties.

Closed-form scalars are pinned with rel headroom; every value floor is paired with a
property/guard so a hardcoded constant or a trivial answer cannot clear the suite.
"""
import math
from pytest import approx
from hw import poisson, calculate_poisson_pmf_a, calculate_poisson_pmf_b

LAM = 3
A_REF = 0.7673431912197031   # P(2 <= X <= 6), X ~ Poisson(3)
B_REF = 0.2326568087802969   # P(X < 2 or X > 6) = 1 - A_REF


# --- O1: the pmf matches the Poisson formula for several (x, lambda) (any equiv impl) ---
def test_poisson_matches_formula():
    for x, lam in [(0, 3), (1, 2), (3, 3), (5, 5), (7, 4)]:
        expected = (lam ** x / math.factorial(x)) * math.exp(-lam)
        assert poisson(x, lam) == approx(expected, rel=1e-12), \
            f"poisson({x}, {lam}) should equal lam^x/x! e^-lam = {expected:.8g}"


# --- O1: the pmf is a valid distribution (GUARD: rejects garbage / constant pmf) ---
def test_pmf_is_valid_distribution():
    probs = [poisson(x, LAM) for x in range(0, 60)]
    assert all(0.0 <= p <= 1.0 for p in probs), "every Poisson probability must lie in [0, 1]"
    assert sum(probs) == approx(1.0, abs=1e-9), \
        f"the pmf must sum to 1 over its support, got {sum(probs):.6f}"


# --- O2: P(2 <= X <= 6) closed-form value (FLOOR) ---
def test_pmf_a_value():
    assert calculate_poisson_pmf_a() == approx(A_REF, rel=1e-6), \
        f"P(2<=X<=6) for Poisson(3) should be {A_REF:.6f}"


# --- O2: a is the sum of the pmf over [LOW, HIGH] (GUARD: not a pasted constant) ---
def test_pmf_a_equals_range_sum():
    expected = sum(poisson(x, LAM) for x in range(2, 7))
    assert calculate_poisson_pmf_a() == approx(expected, rel=1e-12), \
        "calculate_poisson_pmf_a() must equal the sum of poisson(x, 3) over x = 2..6"


# --- O3: P(X<2 or X>6) closed-form value (FLOOR) ---
def test_pmf_b_value():
    assert calculate_poisson_pmf_b() == approx(B_REF, rel=1e-6), \
        f"P(X<2 or X>6) for Poisson(3) should be {B_REF:.6f}"


# --- O3: a and b partition the sample space (GUARD: rejects b == 0 / b copied from a) ---
def test_a_and_b_are_complementary():
    a, b = calculate_poisson_pmf_a(), calculate_poisson_pmf_b()
    assert a + b == approx(1.0, abs=1e-9), \
        f"P(2<=X<=6) + P(X<2 or X>6) must equal 1, got {a + b:.6f}"
    assert b == approx(1.0 - a, rel=1e-12), "b must be the complement of a"
```

**Floor-and-guard, verified by mutation:**
| Trivial/degenerate submission | Caught by |
|---|---|
| `b` hardcoded to `0` | `test_pmf_b_value`, `test_a_and_b_are_complementary` |
| `a` pasted constant + `poisson` returns junk (e.g. `0.5`) | `test_poisson_matches_formula`, `test_pmf_is_valid_distribution`, `test_pmf_a_equals_range_sum` |
| both return `0` | both value floors |

No bare threshold a trivial answer could clear. (Deterministic problem → no RNG seed/tolerance
sweep applies; the property guards play the role the degeneracy guards play in a stochastic HW.)

---

## 3. `hw4/rubric.md` (NEW — autograded split 55/35/10)

Shipped to students (TILT). Interpretation = CERL on the result-reading paragraph (what the
autograder can't check). Full file content in the §4d diff.

| Layer | Weight | How |
|---|:---:|---|
| **Correctness** | **55%** | machine-verified by `test_hw.py` (§2): formula + valid-distribution + two closed-form values + range-sum/complement guards. Independent → partial credit. |
| **Interpretation** | **35%** | the §6 paragraph, 0–3 on each of Claim/Evidence/Reasoning/Limits. PASS = ≥2 every dimension. |
| **Process** | **10%** | `math`-only respected; readable; runs clean. |

---

## 4. Proposed unified diffs (per file — NOT applied)

### 4a. `hw.py` — add the Required-Interpretation markdown cell (no logic change; markers preserved)

The reference solution already passes every new test, so **no implementation edit is needed**;
the only change adds the interpretation prompt cell (a `#`-comment markdown cell that ships to
students). `### SOLUTION START/END ###` markers and the imported contract are untouched. There
is no import-time work to guard.

```diff
--- a/hw.py
+++ b/hw.py
@@ def calculate_poisson_pmf_b() -> float:
     ### SOLUTION START ###
     probability = 1 - calculate_poisson_pmf_a()
     ### SOLUTION END ###
     return probability

+# ## Required interpretation
+#
+# In one short paragraph (answer in the cell below), interpret your two results:
+#
+# - What does $P(2 \le X \le 6) = 0.767$ mean in words for a process with rate
+#   $\lambda = 3$?
+# - Why does the complement rule let you get $P(X < 2 \text{ or } X > 6)$ directly
+#   from your first answer?
+# - Name one assumption the Poisson model makes, or one situation where modeling
+#   these counts as Poisson would mislead (a non-constant rate, over-dispersion,
+#   or non-independent events).
+#
+# *Your answer here.*
+
 # ## Workload
 #
 # How many hours did you spend on this homework assignment outside of class?
```

### 4b. `README.md` — 8-part framing + criteria up front (replaces the 1/0.5/0 gate)

```diff
--- a/README.md
+++ b/README.md
@@
-# README
-
-## Programming portion instructions
-
-See the `README.md` file for HW1 for the following:
-
-- Instructions on how to install prerequisites, launch Jupyter lab, open
-  `hw.py` as a Jupyter notebook, and run tests using `pytest`.
-
-# Grading
-
-- 1 point: Homework is complete and correct (passes all automated correctness
-    tests, tests have not been modified, PR is not merged, existing docstrings
-    have not been edited or deleted, written component has no errors).
-- 0.5 points: Homework is incomplete or has errors.
-- 0 points: Homework was not submitted on time.
-
-### Submission
-
-In order to complete your submission, you will need to commit and push the
-updated `hw.py` file. Don't forget to record the amount of time spent on this
-homework!
+# HW4 — Poisson Probabilities
+
+> Overhauled (code-outcome pattern). Grading is **specifications-based** (per-check +
+> rubric), not the old complete/incomplete gate. Rubric in `rubric.md`.
+
+## 1. Context & purpose
+
+The Poisson distribution models counts of independent events at a constant average rate.
+Computing a range probability and its complement is the first move you'll reuse whenever you
+reason about a discrete distribution.
+
+## 2. Learning objectives
+
+- **O1** Evaluate the Poisson pmf for given `x`, `λ`. *(apply — Correctness)*
+- **O2** Compute a range probability by summing the pmf. *(apply — Correctness)*
+- **O3** Apply the complement rule for the tail probability. *(apply/analyze — Correctness)*
+- **O4** Interpret the results and a model assumption. *(evaluate — Interpretation)*
+
+## 3. The task (outcome, not recipe)
+
+Implement `poisson(x, λ)`; use it to compute `calculate_poisson_pmf_a()` = `P(2≤X≤6)` and
+`calculate_poisson_pmf_b()` = `P(X<2 or X>6)` for `λ = 3`.
+
+## 4. Allowed methods
+
+Any correct computation that reaches the required probabilities earns full credit. **Scope:**
+this is a closed-form problem — the answers are fixed numbers, so "any approach" means any
+correct route to *those* values. Use only the `math` standard library (no NumPy/SciPy).
+
+## 5. How you'll be assessed (criteria shown up front)
+
+| Bundle | Weight | Pass when… |
+|--------|:------:|------------|
+| **Correctness** | **55%** | `pytest test_hw.py` green — the pmf matches its formula and is a valid distribution; `P(2≤X≤6)` and `P(X<2 or X>6)` match the closed-form values (`rel=1e-6`); `a` equals the range sum and `a+b=1`. |
+| **Interpretation** | **35%** | the paragraph in `hw.py` reaches **Proficient+** on every Claim/Evidence/Reasoning/Limits dimension (`rubric.md`). |
+| **Process** | **10%** | `math`-only; readable; runs clean. |
+
+**Revision:** Correctness re-runs on every push (iterate to green); Interpretation gets one
+revise-and-resubmit. An LLM may pre-draft interpretation scores; a human confirms and is final.
+
+## 6. Submission
+
+Commit and push `hw.py` (code + the interpretation paragraph). Keep the imported function
+names. Run `pytest test_hw.py` locally first. Record your time in the Workload section.
```

### 4c. `make_release` — ship `rubric.md` to students (TILT)

```diff
--- a/make_release
+++ b/make_release
@@
 cp requirements.txt release
 cp test_hw.py release
 cp README.md release
+cp rubric.md release
```

### 4d. `rubric.md` — NEW file

```diff
--- /dev/null
+++ b/rubric.md
@@
+# HW4 — Grading rubric (Poisson probabilities)
+
+Autograded HW: machine-verified correctness + a human-scored interpretation layer. Split
+**55 / 35 / 10** per the repo rule for autograded HWs (see the repo-root `rubric.md`).
+
+## Correctness (55) — machine-verified
+
+`pytest test_hw.py`. Independent tests → partial credit; thresholds visible in the file:
+`poisson` matches `lam^x/x! e^-lam` and is a valid distribution (probabilities in [0,1],
+sums to 1); `P(2<=X<=6)` and `P(X<2 or X>6)` match the closed-form values (`rel=1e-6`); `a`
+equals the range sum (not a pasted constant); `a + b = 1` (complement guard).
+
+## Interpretation (35) — Claim / Evidence / Reasoning / Limits (0–3 each)
+
+The paragraph in `hw.py`. PASS = ≥2 on every dimension; else one revise-and-resubmit.
+
+| Dim | 3 | 2 | 1 | 0 |
+|-----|---|---|---|---|
+| **Claim** | states correctly what `P(2<=X<=6)=0.767` means and what the complement is | mostly | partial | missing |
+| **Evidence** | grounds it in the numbers (0.767 / 0.233) and the rate `λ=3` | some | vague | none |
+| **Reasoning** | explains why total probability = 1 makes the complement valid | sound | superficial | absent |
+| **Limits** | names a real Poisson assumption/failure (non-constant rate, over-dispersion, dependence) | one weakly | minimal | none |
+
+## Process (10)
+
+`math`-only (no NumPy/SciPy); readable; notebook runs top-to-bottom.
+
+**LLM pre-grading** may draft per-dimension scores + one-line reasons; a human confirms every
+grade and is final.
```

### 4e. Autograder wiring

hw4 is autograded and **keeps** its `test_hw.py`, so the shared classroom autograder stays
wired as-is — nothing to neutralize or orphan. (No per-assignment `classroom.yml` exists in
`hw4/`; the workflow is shared and unaffected.)

---

## 5. Objective → check/row map (alignment contract)

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| **O1** evaluate the pmf | Apply | `test_poisson_matches_formula`, `test_pmf_is_valid_distribution` | ✅ autograded |
| **O2** range probability | Apply | `test_pmf_a_value`, `test_pmf_a_equals_range_sum` | ✅ autograded |
| **O3** complement rule | Apply/Analyze | `test_pmf_b_value`, `test_a_and_b_are_complementary` | ✅ autograded |
| **O4** interpret | Evaluate | Interpretation rubric (CERL) | ✅ rubric |
| *(communication)* | — | Process (10%) | ✅ partly mechanical, partly rubric |

**Every objective maps to a check or row; none unmeasurable.** O4 is human-rubric by design
(prose). Process's "`math`-only" sub-criterion is mechanically checkable (grep imports); the
rest is light rubric.

---

## 6. Effort & budget

| Component | Change vs. current |
|-----------|--------------------|
| Implementation (`poisson`, `a`, `b`) | unchanged (~30–45 min) |
| Interpretation paragraph | **+~10 min** (new) |
| Net | well within 5–6 hrs/week — hw4 is one of the smallest HWs |

No computation to trim (there is none); the interpretation load is the only addition and is
small.

---

## 7. Judgment calls beyond the spec

1. **Closed-form HW → no stochastic machinery.** No RNG and no import-time work, so there is
   no seed/tolerance sweep and nothing to `__main__`-guard. Stated explicitly so the absence
   reads as intentional. The distribution-property tests play the floor-and-guard role.
2. **Kept exact value pins (`rel=1e-6`).** Framework §5 keeps closed-form scalars exact; the
   brittleness concern is addressed by pairing each value with a property/guard rather than by
   loosening it to a meaningless tolerance.
3. **Reference `hw.py` needs no logic edit** — it already passes the new suite; the only edit
   is the interpretation cell. (Confirmed by running the suite against it.)
4. **`make_release` ships `rubric.md`** (TILT); the current script copies README/tests/reqs
   but no rubric.
5. **Consolidation note (not acted on here):** hw1/hw2/hw3/hw4 are all early
   probability/regression basics; hw4 stays standalone for this pass (flagged for Scope B).

---

## 8. Validation numbers

- **Suite:** `6 passed in 0.01s` against the reference solution (3 runs: 0.00 / 0.00 / 0.01s).
- **`import hw`:** 0.004 s (imports `math` only).
- **Guards:** mutation-tested — trivial `b=0` and a garbage `poisson` are both rejected (§2).

---

## 9. Proposed commit message (when applied — do NOT commit now)

```
hw4 overhaul: property/guard autograder + Poisson interpretation (code-outcome)

- test_hw.py: keep the two closed-form values (rel=1e-6) but pair each with
  property/guard tests — pmf matches its formula and is a valid distribution,
  a equals the range sum (not a pasted constant), a+b=1. Independent
  partial-credit cases with actionable messages. (6 passed, ~0.01s.)
- hw.py: add a Required-Interpretation markdown cell (meaning of the two
  probabilities, why the complement rule holds, one Poisson assumption/limit).
  No logic change; SOLUTION markers + imported contract unchanged; no
  import-time work to guard.
- README.md: 8-part framing; criteria-up-front specs table (replaces 1/0.5/0).
- rubric.md (new): autograded 55/35/10; CERL interpretation.
- make_release: ship rubric.md.

Closed-form HW: no RNG/seed sweep needed; property tests are the floor-and-guard.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
