# `info521` — Lightweight Course Library: Proposal (DRAFT, uncommitted)

> **Status:** read-only survey for Greg's approval. **No package code written, no unit files
> modified, nothing committed.** This is the boundary + API + packaging proposal only.

## Scope & boundary (enforced)

- **INCLUDE = plumbing only:** seeded-RNG construction, data loaders, shared plotting style,
  path/IO utilities, test-harness helpers.
- **EXCLUDE = anything students are graded on implementing.** Hard rule: **any code inside
  `### SOLUTION ###` / `%%% Answer %%%` / `#answer()` markers is a learning target by
  definition** and never enters the library — plus the derivable/assessed methods even where
  they recur (normal equations, CV, MLE/variance, Bayesian posterior/predictive math, MCMC,
  Laplace, gradient/Hessian, the estimators).
- **When entangled or uncertain → FLAG, don't extract.**

## STEP 1 — Inventory

### INCLUDE / FLAG candidates (plumbing)

| Candidate pattern | Units | ~Freq | Category | Verdict | Why |
|---|---|---|---|---|---|
| `np.random.default_rng(seed)` construction → **`make_rng`** | U1, U3, U4, U5, Cap (qmd+test+hw); U0 (marker) | very high, ~15 sites | reproducibility | **INCLUDE** | One canonical seeded-`Generator` factory. Isolates the exact surface the numpy-2.1 RNG-stream pin guards (see `shared/requirements.txt`, `docs/REVIEW.md` S2/S6) — a future numpy bump touches one function, not 15. |
| module `RNG = default_rng(521)` + `rng = rng or RNG` default | U3 | 6 fns | reproducibility | **FLAG** | Convenience default-arg pattern; fine to standardize, but the `or RNG` fallback is U3-local ergonomics, not core. Offer `make_rng` and let U3 keep its module default if wanted. |
| `seeded_draw(seed, n)` | U0 | 1 | reproducibility | **EXCLUDE** | Inside SOLUTION markers — it **is** the seed-policy learning target. |
| `load_data()` via `np.loadtxt(...)` → per-dataset loaders | U1, U5, Cap | 3 | data | **INCLUDE** | Pure parse-and-return; zero modeling. *Caveat:* `load_data` is the autograder's import surface (`from hw import … load_data`) — see Flag B. |
| relative `"data/…"` path inside loaders | U1, U5, Cap | 3 | io/util | **INCLUDE** | Brittle to CWD (only works when pytest runs from the unit dir). One resolver fixes all three. |
| `generate_synthetic_data` / `true_function` / `sample_dataset` | U4 | 1 | data | **FLAG** | Data generator given as *scaffolding* (outside markers). It's data, not a model — but appears in only one unit and is tied to U4's "recover the truth + gap" setup. Extract only if a second unit reuses it. |
| "U2a Poisson/Bernoulli samplers-as-data" | — | 0 | data | **FLAG (N/A)** | No such sampler exists in code — U2a Part A is `math`-only pmf evaluation. Nothing to extract; noted so the candidate is closed. |
| `plt.subplots(figsize=…)` + axis labels + `tight_layout(); show()` boilerplate | all qmds | ~8 figs | viz | **INCLUDE** | A `set_style()` + sane figure defaults removes the repeated boilerplate. |
| ad-hoc colors (`C0`, `gray`, `k`, `#c0392b`, `#bdc3c7`, `#bbb`) | qmds | ~10 | viz | **INCLUDE** | **No colorblind-safe palette today.** This is *new standardization*, not de-dup — low existing consistency, high value. Ship a `PALETTE` + rcParams. |
| ±2σ predictive-band figure | U4 (`errorbar`), Cap (`fill_between`) | 2 | viz | **FLAG** | The band *style* is plumbing, but the figure plots the **student's own model output**. Provide an axis/style scaffold at most — never compute or plot their results for them. |
| `from pytest import approx` + rel/abs tolerances | all `test_hw.py` | 6 | test-harness | **INCLUDE** | Shared tolerance constants + `approx` re-export. |
| `_rng(seed)` test fixture | U1, U3, U5 | 3 | test-harness | **INCLUDE** | Same construction as `make_rng`; tests import it. |
| PSD+symmetric assert (`cov==cov.T` ∧ `eigvalsh ≥ -tol`) | U4, U5, Cap | 3 | test-harness | **INCLUDE** | `assert_psd(M)`. |
| beats-baseline floor (`rmse ≤ k·baseline`) | U1, Cap | 2 | test-harness | **INCLUDE** | `assert_beats_baseline(...)`. |
| convergence floor-AND-guard (error shrinks with N) | U3 | 2 | test-harness | **INCLUDE** | `assert_converges(...)`. |
| stochastic-not-constant guard (two seeded draws differ) | U0, U3, U5 | 3 | test-harness | **INCLUDE** | `assert_stochastic(a, b)`. |
| fixture prep `_xt` / `_stack` / `_model` / `_fit` / `_chain` | per unit | 5 | test-harness | **EXCLUDE** | These instantiate the **assessed** student objects (call `SimpleLinearModel`, `BayesianModel`, …). Keep in `test_hw.py`; not library. |

### EXCLUDE candidates (assessed methods that recur — see full list in STEP 4)

| Pattern | Units | Verdict | Why |
|---|---|---|---|
| design matrix / polynomial features | U1 (marker), U4, Cap | **EXCLUDE + FLAG** | Graded in U1 (spec C3) but given free in U4/Cap. Library-izing would trivialize U1. **Inconsistency flagged.** |
| normal equations, `scale()`, `run_K_fold_cv`, `compute_mse_loss` | U1 | EXCLUDE | Core assessed methods. |
| `poisson` pmf | U2a | EXCLUDE | Assessed (Part A). |
| `PolynomialRegressionModel`, `predictive_variance`, `compute_cov_w` | U1, U4 | EXCLUDE | Assessed modeling. |
| `B`, `Beta`, `posterior`, `calculate_marginal_likelihood`, `calculate_probability_of_winning` | U4 | EXCLUDE | Assessed Bayesian math. |
| `logistic`, `gradient`, `hessian`, `newton_map`, `laplace_covariance`, `MetropolisSampler` | U5 | EXCLUDE | Assessed (MAP/Laplace/MCMC). |
| `BayesianModel` contract impl | Cap | EXCLUDE | The whole open task. |
| all matrix-calculus / Gaussian / Beta-moment derivations | U2b | EXCLUDE | Written learning targets. |

## STEP 2 — Proposed API (INCLUDE set only)

Minimal surface; only what the inventory justifies.

```
src/info521/
  __init__.py        # version; re-export make_rng, set_style
  rng.py             # reproducibility
  data.py            # loaders (parse-only)
  viz.py             # shared plotting style
  testing.py         # autograder helpers
  paths.py           # data-path resolution (io/util)
  data/              # canonical datasets shipped as package data (see Flag E)
```

**`info521/rng.py`**
```python
DEFAULT_SEED: int = 0
def make_rng(seed: int = DEFAULT_SEED) -> np.random.Generator:
    """The one canonical seeded NumPy Generator. Use everywhere instead of
    calling np.random.default_rng directly (single point to manage the numpy
    RNG-stream pin)."""
```

**`info521/data.py`** (loading/parsing only — never modeling)
```python
def load_olympic_100m() -> tuple[np.ndarray, np.ndarray]:
    """(year, winning_time) — U1 Olympic-100m regression data."""
def load_fcml_classification() -> tuple[np.ndarray, np.ndarray]:
    """(X[N,2], t[N] in {0,1}) — U5 FCML binary-classification data."""
def load_capstone() -> tuple[np.ndarray, np.ndarray]:
    """(x, t) — open Capstone data (gap in [0.5, 2.0])."""
# FLAG (extract only if reused beyond U4):
def make_synthetic_regression(rng, n=40, x_range=(-2, 7), noise_var=6,
                              gap=(2.5, 4.5)) -> tuple[np.ndarray, np.ndarray]:
    """Synthetic cubic regression data with a held-out input gap (U4)."""
```

**`info521/viz.py`** (style/scaffold, not analysis)
```python
PALETTE: dict[str, str]          # colorblind-safe named colors
def set_style() -> None:
    """Apply shared matplotlib rcParams: figure size, fonts, colorblind palette."""
# FLAG (thin scaffold only; student supplies mean/std):
def band_ax(ax, x, mean, std, k=2, label="±2σ"): ...
```

**`info521/testing.py`** (autograder plumbing — not assessed)
```python
REL, ABS = 1e-3, 1e-6            # shared default tolerances
from pytest import approx        # re-export
from .rng import make_rng        # tests use the same factory
def assert_psd(M, tol=1e-8): ...
def assert_beats_baseline(pred, target, frac=0.5): ...   # rmse <= frac * baseline
def assert_converges(err_small, err_large, ceiling): ... # floor-AND-guard
def assert_stochastic(a, b): ...                          # two seeded draws differ
```

**`info521/paths.py`**
```python
def data_path(name: str) -> str:
    """Absolute path to a packaged dataset (CWD-independent)."""
```

### Example usage
```python
from info521.rng import make_rng
from info521.data import load_olympic_100m, load_fcml_classification
from info521.viz import set_style
from info521.testing import assert_psd, assert_beats_baseline

set_style()
rng = make_rng(0)
x, t = load_olympic_100m()
```

## STEP 3 — Packaging

- **Layout:** `src/`-layout, `pyproject.toml` (hatchling or setuptools), `py.typed`.
- **Dependencies (lean):** `numpy==2.1.*` (match the pinned env), `matplotlib`.
  **No scipy** — it's only used by *excluded* modeling code (U4/hw11), so it stays a
  per-unit dep. **No pandas** — every loader uses `np.loadtxt` (confirmed: zero pandas usage).
- **Python:** `requires-python = ">=3.11,<3.14"` — matches `.python-version` (3.11) and the
  `<=3.13` constraint (numpy 2.1.x ships no cp314 wheels).
- **Install:** `pip install -e .` for development.
- **Where it lives — recommendation: in THIS repo**, under `src/info521/`, as a monorepo
  package. Rationale: it co-evolves with the units, the autograder already lives here, and one
  source of truth avoids version-sync drift. Split into its own repo only if another course
  reuses it.
- **Classroom-install constraint (the real packaging question):** the GitHub Classroom
  autograder must be able to `import info521`. Options: (a) publish to PyPI as `info521` and
  add it to each unit's `requirements.txt`; (b) install via `pip install
  "info521 @ git+https://…@<tag>"` pinned per unit; (c) vendor. **Recommend (a) or (b) with a
  pinned tag** so the autograder env is reproducible. (Flag E.)

## STEP 4 — Deliberately excluded (and why) — auditable boundary

Every assessed method seen to recur, kept **out** by the SOLUTION-marker rule:

- **U0** — `seeded_draw` (the seed-policy demonstration itself).
- **U1** — scalar normal equations (`SimpleLinearModel.train`); matrix normal equation
  (`PolynomialRegressionModel.train`); **design matrix / polynomial features**
  (`get_design_matrix_shape`, `fill_design_matrix`); `scale()` to [0,1];
  `run_K_fold_cv`; `compute_mse_loss`.
- **U2a** — `poisson` pmf; Bernoulli MLE derivation; Fisher-information derivation.
- **U2b** — all of it (Jacobian identities; diagonal-Gaussian independence; MLE unbiasedness;
  Beta mean/variance) — written learning targets.
- **U3** — `f(x)`; `monte_carlo_expectation`; `estimate_pi_using_circle/sphere/n_ball`;
  `number_of_orthants`; the analytic-expectation and π-formula derivations.
- **U4** — `compute_cov_w`; `predictive_variance`; `B`; `Beta`; `posterior`;
  `calculate_marginal_likelihood`; `calculate_probability_of_winning`; Inverse-Gamma
  derivation. *(Design-matrix/`PolynomialRegressionModel` also excluded.)*
- **U5** — `logistic`; `gradient`; `hessian`; `newton_map`; `laplace_covariance`;
  `MetropolisSampler` (all methods); the PGM; the Newton/Laplace derivations.
- **Capstone** — the `BayesianModel` contract implementation (the entire open task).

**Entanglement flags (excluded despite looking like plumbing):**
- **Design matrix / polynomial features** — given free in U4 & Capstone, but **graded in U1
  (C3)**. Cannot be library-ized without trivializing U1.
- **±2σ band plot** — plots the student's own results (assessed), so only a style scaffold
  could ever be shared, not the plotting of results.

## Open flags for your decision

- **A. `make_rng` vs U0.** U0 *teaches* `default_rng(seed)`. Recommend U0 keeps writing it raw
  (learn once); `make_rng` is used from U1 on. Alternative: U0 introduces `make_rng` as the
  canonical helper. Your call.
- **B. Loader import surface.** Autograders do `from hw import … load_data`. Cleanest: hw.py
  does `from info521.data import load_olympic_100m as load_data` so the autograder surface is
  unchanged. Confirm you want loaders centralized given this touch to each hw.py.
- **C. `make_synthetic_regression`.** Only U4 uses it today — extract now or leave in U4?
- **D. `testing.py` exposes grading thresholds** to students (they get `test_hw.py` and could
  `pip install info521`). Specs are published anyway, so likely fine — confirm, or keep
  `testing.py` instructor-side.
- **E. Dataset distribution.** Ship CSVs as package data (CWD-independent, recommended) vs.
  keep per-unit `data/` dirs and pass paths. Affects loader signatures.
- **F. `band_ax` viz helper** — include the thin scaffold, or leave plotting entirely to
  students?

---
*No package code, no `src/` tree, no commits — proposal only. Awaiting review.*
