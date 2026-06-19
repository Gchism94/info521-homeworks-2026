# Grading — INFO 521

> **Specifications grading.** There are **no points and no weighted averages** anywhere in
> this course. You meet clear, published standards on each deliverable; where you fall short
> you revise and resubmit; your final letter reflects **how much of the course you complete to
> standard** — not an average of partial scores.

## How grading works in this course

<!-- SYLLABUS EXCERPT START — lift this paragraph into the syllabus verbatim -->
**How grading works in this course.** Every assignment is graded **pass / not-yet**, never
with partial points. Each one comes with a short, explicit list of standards ("specifications")
you can see before you start. If your work meets all of them, it passes. If it doesn't yet, you
get specific feedback and **revise and resubmit** — "not-yet" is a step in the process, not a
penalty. You are never averaged down for an early attempt. Your final letter grade reflects
**how many deliverables you complete to standard**, so the path to the grade you want is simply
to meet the standards on more of the work. Nothing here is curved, weighted, or scored on a
percentage.
<!-- SYLLABUS EXCERPT END -->

## Structure of the course

The course is **8 deliverables**, each graded **PASS / NOT-YET** (revise-and-resubmit), never
partial points:

- **U0 (onboarding)** — a **completion floor**, not a ladder rung. You pass it once; it does not
  by itself raise your letter, but it is required (see the ladder).
- **6 CORE units** — **U1, U2a, U2b, U3, U4, U5.** These are the rungs of the ladder.
- **Capstone** — independent synthesis: choose a model, fit it, quantify uncertainty by a valid
  Bayesian method, and report results + ethics.

### What it takes to pass one unit

A unit **PASSES only when all THREE bundles are met**:

1. **Correctness** — autograded method-validity / outcome specs.
2. **Interpretation (CERL)** — Claim, Evidence, Reasoning, Limits, human-confirmed.
3. **Process** — reproducibility and submission-contract specs.

**Miss any one bundle → the unit is NOT-YET → you revise *that bundle* and resubmit.** You only
redo the bundle that fell short, not the whole unit.

## The ladder

Letter grades are **straight letters (A B C D E), no plus/minus**. **U0 must be passed in every
case above E.**

| Letter | Requirement |
|--------|-------------|
| **A** | all 6 core units **AND** the Capstone |
| **B** | all 6 core units, **OR** 5 core + Capstone |
| **C** | 5 core units, **OR** 4 core + Capstone |
| **D** | 4 core units |
| **E** | 3 or fewer core units, **or** U0 not passed |

**How the Capstone counts.** The Capstone **gates the A** — you cannot reach A without it on top
of full core coverage — and elsewhere it is worth **one core unit of "lift"** at the B/C
boundaries (it can substitute for one missing core unit to reach B or C). That lift is **capped**:
because the A requires *all* six core units regardless, the Capstone can never manufacture an A in
place of missing core work.

## Revise budget

The revise policy is tied to **grading cost**, and that is the whole point of the split:

- **Correctness (autograded): UNLIMITED resubmissions** until each unit's deadline. The autograder
  re-runs at **no human cost**, so there is **no cap** — keep pushing until it passes or the
  deadline closes.
- **Interpretation (CERL) + Process (human-confirmed):** **one** revise-and-resubmit per unit,
  **plus** a **course-wide pool of 3 tokens** for a *second* human-bundle revision on the units a
  student finds hardest. Spend a token where a second human read will help you most.

Dates (filled in by the instructor):

- Per-unit deadline: **[PLACEHOLDER]**
- Post-feedback revision window: **[PLACEHOLDER]**
- Hard end-of-term revision cutoff: **[PLACEHOLDER]**

## Independent-miss threshold

Within a bundle, specs are of two kinds: **MUST-MEET** (load-bearing) and **independent**
(non-load-bearing). The rule:

> A student may miss **at most ONE** independent spec in a bundle; every **MUST-MEET** spec must be
> met. This threshold is **flat (≤ 1) across all units** and is **not scaled by bundle size**.

**Why flat and not scaled.** Because Correctness resubmission is **unlimited until the deadline**,
the threshold only decides whether **this submission** passes — **not** the final grade. A student
who is over the threshold simply resubmits. Scaling the threshold per unit (e.g. allowing more
misses in larger bundles) would add complexity to "fix" something that **resubmission already
handles**, so the policy stays simple: one independent miss, everywhere.

## Instructor / TA operations note

- **Correctness** is checked by **GitHub Classroom on every push** — the autograder runs the unit's
  `test_hw.py` automatically, which is what makes unlimited Correctness resubmission free.
- **Interpretation (CERL) and Process** use an **LLM pre-grade followed by required human
  confirmation** — the model triages, a human confirms the pass/not-yet.
- The **one-revision-per-unit rule plus the 3-token pool** is what **bounds human regrading load**:
  human bundles get at most two reads per unit (and the second only when a token is spent), keeping
  the grading workload predictable across the term.
