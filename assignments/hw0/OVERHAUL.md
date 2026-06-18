# hw0 — Overhaul draft (ONBOARDING · light touch)

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw0. **hw0 is onboarding, not a representative
analysis task** — the rollout map prescribes a **light touch**: drop the 1/0.5/0 gate, add TILT, do
**not** over-engineer. **Draft only — diffs proposed, not applied.**

> **STEP 0 — classification: ONBOARDING (non-representative).** The graded artifacts are a trivial
> `add(x, y)` + a LaTeX onboarding sheet (a power-rule derivative, embedding an image, syllabus
> checkboxes). This is a *setup/toolchain* exercise, so it is scored **completion / specifications**
> (pass-or-revise per task), **not** the autograded 55/35/10 analytic split. This is the documented
> onboarding exception — **FLAGGED** so it is not mistaken for a mis-classification.

**Defects fixed:** the 1/0.5/0 gate (→ a completion checklist with criteria up front); a single
trivial test (→ a few light cases for partial credit). Nothing else is added — over-engineering an
onboarding HW would defeat its purpose.

---

## 0. Reference-correctness audit

- **Code:** `add(x, y) → x + y`. Trivial; the new light tests pass (2/2). ✅
- **Written key:** `d/dx xⁿ = n xⁿ⁻¹` — verified symbolically (sympy). ✅ (The hw.tex solution is
  shown in-text, not stripped — appropriate for a worked onboarding example.)

---

## 1. Prompt / framing (TILT — light)

**Context & purpose.** Set up your toolchain and workflow: clone the repo, run `pytest`, fill one
function, compile the LaTeX sheet, and commit/push. No course content depends on the difficulty
here — the point is that the pipeline works end-to-end before HW1.

**What you'll do & how it's assessed (criteria up front).** Each onboarding task is **complete /
not-yet** with one revise-and-resubmit:
1. `add` passes `pytest` (the autograder).
2. The LaTeX sheet compiles with: the power-rule derivative, the embedded Mona Lisa image, and the
   three syllabus checkboxes ticked.
3. Submitted via the GitHub Classroom workflow (commit + push; PR left open).

**Submission & reproducibility.** Autograder imports `add` from `hw`; keep the signature. Compile
`hw.tex`. Record your time in the Workload section.

---

## 2. `hw0/rubric.md` — completion checklist (onboarding; NOT 55/35/10)

| Task | Pass when… |
|------|------------|
| **Code** | `pytest` green: `add` returns the sum (the suite includes identity, negatives, commutativity, floats — so a stub that returns a constant fails). |
| **Written / setup** | `hw.tex` compiles; the derivative `n xⁿ⁻¹` is shown; the image is embedded; all three checkboxes ticked. |
| **Workflow** | repo cloned, committed, and pushed via Classroom; PR left open; provided docstrings intact. |

**Specifications grading:** every task is *complete* or gets **one revise-and-resubmit**. No
partial-credit analytic split — onboarding is binary-per-task by design. *(This is the framework's
onboarding exception to the 55/35/10 rule; flagged for ratification.)*

---

## 3. Objective → row map

| Objective | Assessed by | Measurable? |
|-----------|-------------|:-----------:|
| Run the autograder / fill a function | Code task (`pytest`) | ✅ |
| Use the LaTeX toolchain | Written/setup task (compiles, derivative, image, checkboxes) | ✅ |
| Use the Git/Classroom workflow | Workflow task | ✅ |

**Every objective maps to a task; none orphaned.**

---

## 4. Proposed diffs (per file — NOT applied)

### 4a. `test_hw.py` — keep the trivial test; add a few light cases (no over-engineering)

```diff
 import hw

 def test_add():
     assert hw.add(1, 1) == 2
+
+def test_add_properties():
+    """Light extra cases so a constant stub can't pass: identity, negatives, commutativity, floats."""
+    assert hw.add(0, 5) == 5
+    assert hw.add(-3, 3) == 0
+    assert hw.add(2, 7) == hw.add(7, 2)
+    assert hw.add(0.5, 0.25) == 0.75
```

### 4b. `README.md` — replace the 1/0.5/0 gate with the completion checklist (§2) + TILT framing.

```diff
-# Grading
-- 1 point: Homework is complete and correct (passes all automated correctness
-    tests, PR is not merged, existing docstrings have not been edited or deleted,
-    written component has no errors).
-- 0.5 points: Homework is incomplete or has errors.
-- 0 points: Homework was not submitted on time.
+# Grading (onboarding — completion-based; see rubric.md)
+
+Each setup task is complete / not-yet with one revise-and-resubmit: (1) `add` passes pytest;
+(2) hw.tex compiles with the derivative, the embedded image, and the three checkboxes ticked;
+(3) submitted via the Classroom workflow. No points are lost for difficulty — the goal is a
+working pipeline before HW1.
```

### 4c. `make_release` — ship `rubric.md`:
```diff
 cp test_hw.py release
+cp rubric.md release
 cp requirements.txt release
```

### 4d. `rubric.md` — NEW (the §2 checklist; shipped).

`hw.py` and `hw.tex` are **unchanged** (the `add` solution and the derivative are correct; the
SOLUTION markers are preserved).

---

## 5. Judgment calls

1. **Light touch, by design** — onboarding is completion-scored, not the analytic 55/35/10. FLAGGED
   as the documented exception.
2. **Two tests, not one** — enough that a constant stub fails, not so many it becomes a real coding
   exercise.
3. **No interpretation layer** — there is nothing to interpret; adding CERL here would be
   over-engineering (explicitly cautioned against).

---

## 6. Validation

- New `add` tests: **2 passed in 0.01 s.** ✅
- Derivative key `d/dx xⁿ = n xⁿ⁻¹`: sympy-verified. ✅

---

## 7. Proposed commit message (this commit)

```
hw0 overhaul: completion checklist + light add tests for onboarding (light touch)

Onboarding, non-representative -> completion/specifications scoring, NOT the 55/35/10
analytic split (the framework's documented onboarding exception; FLAGGED).

- README.md: replace the 1/0.5/0 gate with a 3-task completion checklist + TILT framing
  (add passes pytest; hw.tex compiles with the derivative/image/checkboxes; submitted via
  the Classroom workflow). One revise-and-resubmit per task.
- test_hw.py: keep test_add, add test_add_properties (identity, negatives, commutativity,
  floats) so a constant stub can't pass -- without over-engineering an onboarding HW. 2/2.
- rubric.md (new): the completion checklist; shipped to students.
- make_release: ships rubric.md.
- hw.py / hw.tex unchanged (add and the power-rule derivative d/dx x^n = n x^(n-1) are
  correct -- sympy-verified; SOLUTION markers preserved).

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
