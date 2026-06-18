# INFO 521 Homeworks — 2026 Overhaul

Source-of-truth workspace for the **overhauled** INFO 521 (Intro to Machine Learning)
homework set. This repo is a clean-start migration: the original assignments in
`…/INFO_521/2026_spring/homeworks` are **never modified** and remain the canonical fallback
so the old and new courses can run in parallel.

> **Org placeholder:** docs and the publish command below use `info521-sp26` (from the
> original `settings.env`) as the GitHub org. **Confirm/replace** with the actual
> 2026 course org slug before publishing.

## What this is

The overhaul makes every assignment (1) solvable by **multiple valid approaches** that all
earn full autograded credit, and (2) require **interpretation** scored by a shared rubric
rather than a 1/0.5/0 gate. The design spec is `docs/OVERHAUL_FRAMEWORK.md`; the audit that
motivated it is `docs/REVIEW.md`; the (v2) consolidation plan is
`docs/OVERHAUL_CONSOLIDATION_MAP.md`.

## Repo model — per-assignment template repos

GitHub Classroom's native model is "one template repo per assignment." This workspace is the
**single source of truth**; `scripts/make_template_repo.sh <hw>` stamps each assignment into a
standalone, publishable template repo under `build/` (git-ignored).

```
info521-homeworks-2026/
├── assignments/        # source of truth: hw0 … hw17 (starter + solution, with markers)
├── shared/             # machinery reused by every assignment
│   ├── common.typ, equations.typ   # Typst shared assets
│   ├── classroom.yml               # GitHub Classroom autograder workflow
│   ├── requirements.txt            # pinned deps baseline (numpy pinned)
│   ├── make_release                # solution-stripping release builder (hardened, S5)
│   └── gitignore                   # .gitignore for generated template repos
├── scripts/make_template_repo.sh   # generator: assignment → standalone template repo
├── docs/               # OVERHAUL_FRAMEWORK, REVIEW, CONSOLIDATION_MAP (provenance)
├── rubric.md           # the shared analytic rubric (retires 1/0.5/0)
└── CHANGELOG.md
```

## Publishing an assignment (your steps — touch accounts/access)

The agent scaffolds and commits **locally only**. Creating remotes, pushing, and wiring
Classroom are yours:

```bash
# 1) generate a standalone template repo from the source of truth
./scripts/make_template_repo.sh hw3            # -> build/hw3/ (its own git repo)

# 2) create the remote and push (replace the org)
gh repo create info521-sp26/hw3 --public --source=build/hw3 --remote=origin --push

# 3) in GitHub Classroom: new assignment -> use info521-sp26/hw3 as the template repo
```

Keep both the old and new repos live until the pilots pass; cut Classroom over per
assignment.

## Autograding & integrity (carried over)

- **Python version:** this repo requires **Python ≤ 3.13** (`.python-version` pins **3.11**).
  The pinned `numpy==2.1.*` has no Python-3.14 wheels; running it on 3.14 triggers C-ABI
  undefined behaviour (memory corruption in array math). `shared/classroom.yml` pins the CI
  runner to 3.11 via `actions/setup-python` so the autograder can't reproduce it on students.
- Tests run via `classroom-resources/autograding-python-grader` (`shared/classroom.yml`),
  `pip install -r requirements.txt`, 10s timeout — same as the original.
- `make_release` strips solutions between `### SOLUTION START/END ###` (Python) and
  `%%% Answer START/END %%%` (LaTeX), and ships the answer-free Typst PDF + `test_hw.py`.
- Per the overhaul, `test_hw.py` tests **invariants/outcomes**, not pinned coefficients or
  RNG draws; `requirements.txt` pins `numpy` to remove the last cross-version risk.

## Status

- **STEP 1 (this commit set):** scaffold + faithful baseline + machinery. No content
  overhaul applied yet.
- **STEP 2 (gated):** per-assignment overhauls, pilots first (hw3, hw5, hw16). Each
  assignment's draft lives at `assignments/<hw>/OVERHAUL.md`; edits are applied one HW at a
  time behind a review gate, then `test_hw.py` is run against the reference `hw.py`.
