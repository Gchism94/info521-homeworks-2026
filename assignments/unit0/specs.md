# Unit 0 — Specifications (onboarding exception: completion-based, NOT the analytic split)

> **TEMPLATE-FIT NOTE — onboarding exception (pre-ratified, documented).** Unit 0 is tooling, not
> an analysis task, so it uses **completion / specifications grading** rather than the
> Correctness-gateway / Interpretation / Process bundle structure of the analysis units. This is the
> framework's documented onboarding exception (established in the hw0 overhaul and the ratified
> map) — not a new structural change. Per-HW weights are moot; there is no Interpretation bundle
> (nothing to interpret) and no analytic gateway. The one carry-forward is the **seed policy as a
> graded Process spec**, which the analysis units (U3, U5) then assume.

## Completion checklist (each task: met / one revise-and-resubmit)

| Spec | Verified by | Met when… |
|------|-------------|-----------|
| **C1** `add` passes pytest | autograder | `test_add`, `test_add_properties` (a constant stub fails) |
| **P1** seed policy reproducible | autograder | `test_seed_policy_reproducible` — same seed → same draw; the seed matters |
| **W1** LaTeX/onboarding done | human | derivative `n xⁿ⁻¹` shown; the three checkboxes ticked |
| **W2** workflow | human | repo cloned, committed, pushed via Classroom; SOLUTION markers intact |

**Unit PASS = all four met.** No partial-credit analytic split — onboarding is binary-per-task by
design. *An LLM may pre-check the written items; a human confirms and is final.*

## Objective → spec coverage

| Onboarding objective | Spec |
|----------------------|------|
| run the autograder / fill a function | C1 |
| reproducibility (the seed policy) | P1 |
| LaTeX toolchain (derivative, checkboxes) | W1 |
| Git/Classroom workflow | W2 |

**Every onboarding objective maps to a spec.** The seed policy (P1) is the reproducibility
through-line assumed by every later unit.
