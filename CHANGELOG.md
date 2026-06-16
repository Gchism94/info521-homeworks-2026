# Changelog

Provenance and changes relative to the original
`…/INFO_521/2026_spring/homeworks` (read-only canonical fallback).

## [unreleased]

### Commit 1 — Baseline (faithful carry-over, pre-overhaul)
- Copied all 18 assignments (hw0–hw17) verbatim from the original repo, **keeping data
  files** (`*.csv`, `data/`) and excluding only build artifacts (`build/`, `release/`,
  `_site/`, `.quarto/`, `__pycache__/`, `*_files/`, `.ipynb_checkpoints/`, `.DS_Store`).
- Carried over shared machinery unmodified: `shared/common.typ`, `shared/equations.typ`,
  `shared/classroom.yml` (autograder workflow).
- Carried the planning docs into `docs/`: `OVERHAUL_FRAMEWORK.md`, `REVIEW.md` (the audit),
  `OVERHAUL_CONSOLIDATION_MAP.md`.
- No assignment content was altered in this commit — it exists so the STEP-2 overhaul diff
  is reviewable.

### Commit 2 — Repo machinery
- Added top-level `README.md`, `LICENSE` (**placeholder — choose a license**),
  `.gitignore`, and the shared analytic `rubric.md` (retires the 1/0.5/0 grading gate).
- Added `scripts/make_template_repo.sh` — stamps an assignment into a standalone,
  publishable GitHub Classroom template repo under `build/`.
- Added `shared/requirements.txt` (deps superset) and **pinned `numpy`** there and in each
  `assignments/*/requirements.txt` to `numpy==2.1.*` — removes the cross-version RNG-stream
  risk the audit flagged. *TODO: freeze to the exact CI patch version once chosen.*
- Added `shared/make_release` (hardened): calls `make without_answers` **by name** instead
  of relying on it being the first Makefile target (audit finding S5), and an explicit
  `release:`-style flow.
- Added `shared/gitignore` (the `.gitignore` injected into generated template repos).

### STEP 2 — Overhaul (gated; not yet applied)
- Per-assignment overhauls land here as they are approved, pilots first (hw3, hw5, hw16),
  each as its own commit with the diff reviewed and `test_hw.py` run against the reference
  `hw.py`.

## Notes
- GitHub org slug `info521-sp26` is a placeholder from the original `settings.env`; confirm
  the real 2026 course org before publishing.
- Typst assignments import shared assets via `--root ../../` in the monorepo; standalone
  template repos need the shared `.typ` files bundled and the `--root` adjusted — handled by
  `scripts/make_template_repo.sh` (see its header notes).
