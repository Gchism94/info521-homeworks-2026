# Scope B — Consolidation Map (v2 proposal)

A blueprint for folding the 18 fragmented assignments into ~6 richer units plus a small
capstone, with through-line datasets. **This is a planning proposal, not a committed
schedule** — it changes pacing, the gradebook, and GitHub Classroom deployment, so it
needs your sign-off on sequencing before any consolidation is built. It ships as **v2,
after** the Scope A pilots (hw3, hw5, hw16) prove the template + rubric + outcome-tests.

Design intent: less fragmentation, authentic multi-step work, and two narrative
through-lines so students carry one dataset and one model across several skills (which
is itself a transfer aid).

## Current inventory (topic, format, what it measures)

| HW | Topic | Format |
|----|-------|--------|
| hw0 | Tooling: GitHub Classroom, pytest, LaTeX | code + written |
| hw1 | Simple linear model, scalar normal equations | code |
| hw2 | Normal equations in matrix/vector form (+ identities) | code + written |
| hw3 | Polynomial regression, cross-validation, scaling, seeding | code + written |
| hw4 | Poisson probabilities | code |
| hw5 | MLE for a Bernoulli parameter | written |
| hw6 | Expectations: analytic vs Monte-Carlo | code + written |
| hw7 | Jacobians | written |
| hw8 | Multivariate normals; MLE unbiasedness; Beta moments | written |
| hw9 | Fisher information of a Bernoulli parameter | written |
| hw10 | Predictive variance | code + written |
| hw11 | Exact Bayesian inference (coin game) | code + written |
| hw12 | Inverse-Gamma conjugate prior on noise variance | written |
| hw13 | Probabilistic graphical model for Bayesian logistic regression | written |
| hw14 | MAP via Newton-Raphson (+ NR for Poisson regression) | code + written |
| hw15 | Laplace approximation (+ Laplace for Beta/Binomial) | code + written |
| hw16 | Metropolis-Hastings MCMC for Bayesian logistic regression | code |
| hw17 | Estimating pi by sampling (2-D/3-D/n-D) | code + written |

## Two through-lines

- **Regression line — the Olympic 100m dataset** (already shared by hw1/hw2/hw3, and
  the noise-variance prior in hw12): linear model → matrix normal equations → polynomial
  features + cross-validation → Bayesian treatment of the noise variance. One dataset,
  one model, deepening.
- **Bayesian-classification line — the FCML binary-classification dataset** (already
  shared by hw13/hw16, and the natural target for hw11/hw14/hw15): exact/conjugate
  inference → graphical model → MAP (Newton) → Laplace approximation → MCMC, all
  recovering the *same* posterior by different methods. hw16's chain can be checked
  against hw15's Laplace posterior (the audit already notes this), which is exactly the
  kind of cross-method "recover the same truth" the test design rewards.

## Proposed units (~18 → 6 + capstone)

**Unit 0 — Tooling & reproducibility** (from hw0)
Keep small. GitHub Classroom, pytest, seeding, the submission/markdown-reflection
contract. Add the seed policy as a graded process item so reproducibility is taught once
and assumed thereafter.

**Unit 1 — Linear models & model selection** (folds hw1 + hw2 + hw3; touches hw12 later)
Through-line: Olympic 100m. Implement → fit by least squares (any method: normal
equations, `lstsq`, `polyfit`) → polynomial features + scaling → cross-validation for
model order. Interpretation: bias-variance from their own CV curve; leakage; when CV
misleads. This is where the hw3 pilot's tests and rubric live; hw1/hw2 become its early
sub-parts (so their exact-coefficient pins retire into property/closed-form checks).

**Unit 2 — Probability & estimation foundations** (folds hw4 + hw5 + hw7 + hw8 + hw9)
The written-derivation cluster, now per-step graded: distributions (Poisson, Bernoulli,
multivariate normal, Beta), MLE and why it equals the sample mean, unbiasedness,
Jacobians, Fisher information. Add one short interpretation part per derivation ("why
does this estimator behave this way; when is it misleading"). The hw5 pilot's per-step
rubric is the template for the whole unit.

**Unit 3 — Monte-Carlo & estimators** (folds hw6 + hw17)
Analytic vs Monte-Carlo expectations; estimating constants (pi) by sampling in n-D;
convergence/variance of estimators. All stochastic checks are distributional/convergence
(within X% of truth), never pinned draws. Interpretation: estimator variance vs sample
size; the curse of dimensionality from their own n-D pi results.

**Unit 4 — Bayesian inference, exact & conjugate** (folds hw10 + hw11 + hw12)
Predictive variance; exact posterior for the coin game; Inverse-Gamma conjugacy for the
regression noise variance. Through-line: connect the conjugate noise-variance prior back
to Unit 1's Olympic regression. Interpretation: prior sensitivity; what conjugacy buys
and where it stops.

**Unit 5 — Approximate Bayesian inference** (folds hw13 + hw14 + hw15 + hw16)
Through-line: the FCML binary-classification dataset and one Bayesian logistic model.
Graphical model/factorization → MAP via Newton → Laplace approximation → MCMC. The unit's
spine is "four ways to the same posterior": tests check each method recovers the same
posterior mode/covariance within tolerance (method-agnostic, convergence-based). This is
the hw16 pilot generalized. Interpretation: compare the four methods (cost, accuracy,
when each fails); mixing/acceptance for MCMC.

**Capstone — open modeling + inference + interpretation** (new; optional fold of hw17's
open spirit)
A small open-ended task on a provided dataset: choose a model, fit it by any sound
method, quantify uncertainty by one Bayesian method from Unit 4/5, and write a short
report (claim/evidence/reasoning/limits + a one-paragraph impact/ethics note). Graded
mostly by the analytic rubric with a couple of outcome floors. This is the
"analyze/evaluate/create" ceiling the current set never reaches.

## Mapping (nothing lost)

Every current HW lands in exactly one unit: hw0→U0; hw1,hw2,hw3→U1; hw4,hw5,hw7,hw8,hw9→U2;
hw6,hw17→U3; hw10,hw11,hw12→U4; hw13,hw14,hw15,hw16→U5; plus the new capstone.

## Risks / decisions before building B

- **Pacing & gradebook.** 6 units + capstone vs 18 HWs changes due-date cadence and
  GitHub Classroom repo count; specs-grading bundles must be redefined per unit. Needs a
  schedule pass.
- **Bigger submissions, higher stakes per unit.** Mitigate with the specs
  revise-and-resubmit policy so a single unit cannot tank a grade.
- **Effort budget.** Each unit must still fit ~5-6 hrs/week; consolidation must *trim*
  redundant computation (e.g. hw1/hw2's repeated coefficient pinning) rather than stack
  it. Each unit draft will carry an effort estimate.
- **Written derivations stay individually gradable.** Folding hw4/5/7/8/9 into Unit 2
  must keep per-derivation per-step rubric rows so partial credit survives the merge.
- **Topics to re-confirm at build time.** hw12 (Inverse-Gamma noise-variance posterior)
  and hw13 (graphical model factorization) were read only at the section-title level for
  this map; confirm scope when consolidating Unit 4/5.
- **Sequencing dependency.** Unit 5 leans on Unit 4 (same model, increasing
  approximation); Unit 1's Bayesian tail (hw12) assumes Unit 2's estimation basics. The
  unit order above respects these.

## Build order for v2 (after pilots)

1. Unit 1 (reuses the hw3 pilot directly — lowest risk, proves a fold).
2. Unit 2 (reuses the hw5 pilot's per-step rubric across the derivation cluster).
3. Unit 5 (reuses the hw16 pilot's convergence/recovery tests; highest pedagogical payoff).
4. Units 3, 4, then Unit 0 and the capstone.
