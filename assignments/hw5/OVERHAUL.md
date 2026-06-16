# hw5 — Overhaul (Scope A pilot · pure written-derivation template) — APPLIED

Instantiates `docs/OVERHAUL_FRAMEWORK.md` on hw5 (MLE for a Bernoulli parameter). **Applied
to `assignments/hw5/`** (`hw.tex`, `README.md`, new `rubric.md`, `make_release`); the diffs
below record what changed. This is the template for the whole written-derivation cluster
(hw5, 7, 8, 9, 12, 13 → Unit 2): per-step credit replaces the 1 / 0.5 / 0 gate, and a short
interpretation paragraph lifts the ceiling from *derive* to *interpret*.

hw5 is written-only (LaTeX, hard-copy). **There is no autograder / no pytest.** The
"Correctness" layer is therefore a **per-step derivation rubric**, not threshold tests. The
answer markers `%%% Answer START %%%` / `%%% Answer END %%%` and the `make_release` strip are
preserved exactly.

> **Point split (resolved).** This overhaul uses the written/derivation-HW canon
> **Correctness 60 / Interpretation 30 / Process 10**, keyed to the rule that **correctness is
> human-verified** (autograded HWs are 55/35/10; written/derivation HWs are 60/30/10). The
> rule is now recorded in the repo-root `rubric.md` and `CHANGELOG.md`, so the earlier
> 55/35/10-vs-60/30/10 divergence is closed. See §6.

---

## 1. Prompt rewritten into the 8-part template

> Goes into `hw.tex` (the framing wraps the **unchanged** problem statement and the
> marker-preserved solution) and is mirrored in `README.md`. Full LaTeX in the §4 diff.

**1. Context & purpose.** The Bernoulli MLE — "the estimate is just the sample proportion" —
is the simplest instance of a pattern repeated all term: write a likelihood, maximize its
logarithm, read off the estimator. Doing it carefully once makes the Gaussian, Poisson, and
logistic cases mechanical.

**2. Learning objectives** (Bloom verb + the graded row each one is measured by):
- **O1** *Write* the likelihood of an i.i.d. dataset from its per-sample mass function.
  *(Apply — Correctness step A)*
- **O2** *Show* a log-likelihood has a unique maximum. *(Analyze — Correctness step B)*
- **O3** *Derive* the MLE in closed form. *(Analyze — Correctness step C)*
- **O4** *Interpret* the estimator — why it equals the sample mean, when that holds, and when
  it misleads. *(Evaluate — Interpretation rubric)*

**3. The task (outcome, not recipe).** For `N` i.i.d. samples `x₁,…,x_N` from `Bernoulli(r)`
with `P(x|r) = rˣ(1−r)¹⁻ˣ`: (1) write the likelihood `L`; (2) show `L` has a unique maximum;
(3) derive the MLE `r̂`. The required result is `r̂ = (Σxᵢ)/N`; *how* you reach it is open.

**4. Allowed approaches (outcome-based credit — the written analogue of outcome-based tests).**
**Any mathematically valid derivation route to the required result earns full credit; no
single canonical path is privileged.** You may maximize `L` directly *or* maximize `log L`;
you may argue uniqueness by the second-derivative (concavity) test, by a strict-concavity
argument, *or* by showing the score function has a single sign change on `(0,1)`. The one
requirement is that you **show the steps that justify each move** — a bare final answer earns
credit only for the result step, not for the reasoning that should support it.

**5. How you'll be assessed (criteria shown up front).**
- *Correctness (60%)* — the **per-step derivation rubric** in §2 (setup → uniqueness →
  result), each step scored on the **validity of the move**, with full credit for any sound
  alternative route.
- *Interpretation (30%)* — the §6 paragraph, scored Claim / Evidence / Reasoning / Limits
  (0–3 each) on the shared analytic rubric (`rubric.md`).
- *Process (10%)* — clear notation, stated assumptions, legible justification.
- *Specs bundle:* "Derivation = PASS" needs steps A–C each ≥ Proficient and
  "Interpretation = PASS" needs ≥ 2 on every CERL dimension; otherwise one
  revise-and-resubmit.

**6. Required interpretation** (one short paragraph): (a) explain *why*
`r̂ = (1/N)Σxᵢ` is exactly the sample proportion of observed 1's; (b) state the assumptions
under which the estimator is appropriate; (c) give **one** situation where it misleads (e.g.
very small `N`, or all observed outcomes identical so `r̂ ∈ {0,1}`).

**7. Going further (optional, ungraded).** Place a `Beta(a,b)` prior on `r` and find the MAP
estimate; comment on how, for small `N`, the prior pulls the estimate off the boundary and
away from the raw sample proportion.

**8. Submission contract.** LaTeX → PDF, hard-copy as today — **the written cluster keeps its
medium; only the *grading* changes.** Keep the Workload and Acknowledgments sections. There is
no function/return contract to honor (no autograder); the only build contract is that the
`%%% Answer … %%%` block remains intact so `make_release` strips the solution.

---

## 2. `rubric.md` (NEW file — the written-HW instance of the shared analytic rubric)

No pytest. The three layers below are shipped to students (TILT) and are the full content of
the proposed new `hw5/rubric.md` (§4 diff).

### 2a. Correctness (60) — per-step derivation rubric

Enumerate the major logical steps; **each step is scored on the validity of the move, not on
matching the reference's exact algebra.** Any sound alternative route that reaches the same
result earns full credit. Each step gets a 0–3 tier; the tier maps to a fraction of that
step's point weight (3 → 100%, 2 → 80%, 1 → 45%, 0 → 0%). Weights sum to 60.

| Step | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
|------|-----|:---:|---------------|----------------|----------------|---|
| **A · Likelihood** | O1 | 13 | `L = ∏ᵢ rˣⁱ(1−r)¹⁻ˣⁱ`, with independence named as the reason it factorizes | correct product, independence implicit | partial product / wrong exponents / drops a factor | missing or wrong form |
| **B · Unique maximum** | O2 | 24 | a valid objective is set up and uniqueness is *shown* — strict concavity (`∂²log L/∂r² < 0 ∀ r∈(0,1)`), or equivalent concavity / single-sign-change argument | second derivative taken and sign argued, but loosely (e.g. concavity asserted not shown) | first derivative only, or uniqueness asserted without an argument | missing or wrong |
| **C · Closed-form MLE** | O3 | 23 | first-order condition set and algebra carried cleanly to `r̂ = (Σxᵢ)/N = x̄` | right result, minor algebra slip | sets up the stationary condition but can't solve it | missing or wrong |

**Load-bearing vs. independent (required by the overhaul task):**
- **A is load-bearing for the *values* in B and C but not for their *moves*.** If a student
  writes a wrong-but-coherent `L`, grade B and C on whether they correctly manipulate *their
  own* `L` — an error in A caps the final numerical/closed-form correctness of B and C but
  does **not** zero the method credit there.
- **B and C are mutually independent and gradeable in isolation.** A student may skip the
  uniqueness argument (lose B) yet still correctly derive `r̂` (full C), or argue uniqueness
  well (full B) and slip in the final algebra (partial C). Award each on its own merits.
- **Within B, the log-transform is an *enabling* sub-move, not a required one.** Maximizing
  `L` directly is equally valid; do not deduct for skipping logs if the chosen route is sound.

### 2b. Interpretation (30) — Claim / Evidence / Reasoning / Limits

The §6 paragraph, scored on the four shared dimensions, **0–3 each** (12 raw → normalized to
30%). "Interpretation = PASS" requires ≥ 2 on every dimension.

| Dim | 3 | 2 | 1 | 0 |
|-----|---|---|---|---|
| **Claim** | correctly states `r̂` *is* the sample proportion of 1's | mostly right, minor gap | partial / partly wrong | missing |
| **Evidence** | grounds it in the derived form (`Σxᵢ` counts successes; `/N` makes a fraction) and/or a concrete `N` | cites some of the math | vague | none |
| **Reasoning** | links "maximize the likelihood" → "match `r` to the observed success rate" | sound | superficial | absent/wrong |
| **Limits** | names a real failure *and* the assumption it breaks (small `N`; all-identical ⇒ `r̂∈{0,1}`; non-i.i.d.) | one weakly | minimal | none |

### 2c. Process (10) — notation, assumptions, justification clarity

| Sub-dim | Pts | Full credit when… |
|---------|:---:|-------------------|
| **Notation** | 4 | symbols defined/consistent (`N`, `r`, `r̂`, `Σ` ranges), `log` base stated |
| **Stated assumptions** | 3 | i.i.d. given `r`, `xᵢ∈{0,1}`, `r∈(0,1)` made explicit somewhere |
| **Justification clarity** | 3 | each `⟹` follows from the previous line; steps legible and labeled |

---

## 3. Objective → rubric-row map (alignment contract)

| Objective | Bloom | Assessed by | Measurable? |
|-----------|-------|-------------|:-----------:|
| **O1** write the likelihood | Apply | Correctness **step A** | ✅ |
| **O2** show a unique maximum | Analyze | Correctness **step B** | ✅ |
| **O3** derive the MLE | Analyze | Correctness **step C** | ✅ |
| **O4** interpret the estimator | Evaluate | **Interpretation** rubric (CERL) | ✅ |
| *(communication)* | — | **Process** rubric (2c) | ✅ (cross-cutting, not an O#) |

**Every objective maps to a rubric row; none is unmeasurable.** The one row *not* tied to a
content objective is **Process** — it scores the cross-cutting communication competency
(framework's standard 10% layer), not O1–O4. Flagged per the task's "flag any you cannot
measure" instruction: nothing is unmeasurable here; Process is intentionally objective-free.

---

## 4. Proposed unified diffs (per file — NOT applied)

> Apply against the marked regions; LaTeX is valid as written. `@@` line offsets are
> best-effort against the current files. No solution markers are moved; `make_release` still
> strips the `%%% Answer … %%%` block.

### 4a. `hw.tex` — add the 8-part framing + marker-preserving solution polish

```diff
--- a/hw.tex
+++ b/hw.tex
@@ -19,24 +19,75 @@
-\section{MLE for independent samples from Bernoulli distribution}
-
-\emph{(Adapted from FCML Ex. 2.9)}
-
-\bigskip
-
-\noindent The Bernoulli distribution can be used to model events with binary outcomes
+\section{MLE for independent samples from the Bernoulli distribution}
+
+\emph{(Adapted from FCML Ex.~2.9)}
+
+\subsection*{Context \& purpose}
+
+\noindent The Bernoulli MLE---``the estimate is just the sample
+proportion''---is the simplest instance of a pattern you will repeat all term:
+write a likelihood, maximize its logarithm, and read off the estimator. Doing it
+carefully once here makes the Gaussian, Poisson, and logistic cases mechanical.
+
+\subsection*{Learning objectives}
+
+\noindent By the end of this problem you can:
+\begin{itemize}
+    \item \textbf{O1} Write the likelihood of an i.i.d.\ dataset from its
+        per-sample mass function. \emph{(Bloom: Apply --- Correctness step A)}
+    \item \textbf{O2} Show a log-likelihood has a unique maximum. \emph{(Bloom:
+        Analyze --- Correctness step B)}
+    \item \textbf{O3} Derive the maximum-likelihood estimator in closed form.
+        \emph{(Bloom: Analyze --- Correctness step C)}
+    \item \textbf{O4} Interpret the estimator---why it equals the sample mean,
+        when that holds, and when it misleads. \emph{(Bloom: Evaluate ---
+        Interpretation rubric)}
+\end{itemize}
+
+\subsection*{The problem}
+
+\noindent The Bernoulli distribution can be used to model events with binary outcomes
 (e.g., coin tosses). For a random variable $X$ that can take on two values: 0 or
 1, the probability mass function describing the outcome (i.e., the likelihood) is given by
 \begin{align}
 P(x|r) = r^x(1-r)^{1-x}
 \end{align}
 where $r$ is the probability of $X$ taking on the value 1.
 
 \begin{enumerate}
-    \item Suppose you observe $N$ values $x_i, \dots, x_N$ sampled from the
+    \item Suppose you observe $N$ values $x_1, \dots, x_N$ sampled from the
         Bernoulli distribution. Write down the expression for the likelihood
         $L$ of this dataset, assuming that the samples are independent
         conditioned on $r$.
     \item Show that $L$ has a unique maximum.
     \item Now that you have shown that $L$ has a unique maximum, derive an
         expression for the maximum likelihood estimator $\hat{r}$
         for the parameter $r$ in the likelihood $L$.
 \end{enumerate}
+
+\subsection*{What you may and may not use}
+
+\noindent \textbf{Any mathematically valid derivation that reaches the required
+result earns full credit}---there is no privileged path. You may maximize $L$
+directly or maximize $\log L$; you may argue uniqueness by the second-derivative
+(concavity) test, by a strict-concavity argument, or by showing the score
+function has a single sign change on $(0,1)$. You must \emph{show the steps that
+justify each move}: a bare final answer earns credit only for the result step.
+
+\subsection*{How you'll be assessed (criteria shown up front)}
+
+\noindent Grading follows the shared analytic rubric in \texttt{rubric.md}
+(shipped with this assignment), not the old complete/incomplete gate:
+\begin{itemize}
+    \item \textbf{Correctness (60\%)} --- a per-step derivation rubric (setup
+        $\to$ uniqueness $\to$ result); each step earns partial credit on the
+        \emph{validity of the move}, and any sound alternative route to the same
+        result earns full credit.
+    \item \textbf{Interpretation (30\%)} --- the paragraph below, scored
+        Claim / Evidence / Reasoning / Limits (0--3 each).
+    \item \textbf{Process (10\%)} --- clear notation, stated assumptions, and
+        legible justification.
+\end{itemize}
+Under the specifications-grading bundle, ``Derivation = PASS'' requires steps
+A--C each at Proficient or above; otherwise you get one revise-and-resubmit.
+
+\subsection*{Required interpretation}
+
+\noindent After deriving $\hat{r}$, write \textbf{one short paragraph} that:
+(a) explains \emph{why} $\hat{r} = \frac{1}{N}\sum_{i} x_i$ is exactly the
+sample proportion of observed 1's; (b) states the assumptions under which this
+estimator is appropriate; and (c) gives \emph{one} situation where it
+misleads---for example, very small $N$, or all observed outcomes identical so
+that $\hat{r}\in\{0,1\}$.
+
+\subsection*{Going further (optional, ungraded)}
+
+\noindent Place a $\mathrm{Beta}(a,b)$ prior on $r$ and find the MAP estimate.
+Comment on how, for small $N$, the prior pulls the estimate away from the raw
+sample proportion.
@@ -44,28 +95,52 @@
 %%% Answer START %%%
 \ans{
 \subsection*{Solution}
 
+\noindent\textbf{Assumptions and notation.} The $N$ samples are i.i.d.\ given
+$r$, each $x_i \in \{0,1\}$, and $r \in (0,1)$. Here ``$\log$'' is the natural
+logarithm and all sums run over $i = 1,\dots,N$.
+
 \begin{enumerate}
-    \item $L = \prod_{i = 1}^N r^{x_i}(1 - r)^{1 - x_i}$
+    \item Because the samples are independent conditioned on $r$, the joint
+        likelihood factorizes into the product of the per-sample masses:
+        \[ L = \prod_{i = 1}^N r^{x_i}(1 - r)^{1 - x_i}. \]
     \item
+        Maximizing $L$ is equivalent to maximizing $\log L$ (the logarithm is
+        strictly increasing), so we work with the log-likelihood:
         \begin{align}
             \log L &= \sum_{i = 1}^N x_i \log r + (1-x_i) \log(1-r)\\
             \implies \frac{\partial}{\partial r}\log L &= \sum_{i = 1}^N \frac{x_i}{r} - \frac{1 - x_i}{1 - r}\\
             \implies \frac{\partial^2}{\partial r^2}\log L &= \sum_{i = 1}^N -\frac{x_i}{r^2}-\frac{1-x_i}{(1 - r)^2}
         \end{align}
 
-        We can see above that $\frac{\partial^2}{\partial r^2}\log L$ is always
-        negative. Each term in the summation must be negative, as $x_i$ can
-        only be 1 or 0, and $0 \leq r \leq  1$. Thus, $L$ has a unique maximum.
+        Every term of the second derivative is strictly negative for
+        $r\in(0,1)$: since each $x_i\in\{0,1\}$, exactly one of the two
+        fractions in each term is nonzero, and it enters with a negative sign.
+        Hence $\log L$ is strictly concave on $(0,1)$, so it has at most one
+        stationary point and any such point is its unique global maximum;
+        therefore $L$ has a unique maximum.
 
     \item
+        Setting the first derivative to zero at $r = \hat{r}$ and solving:
         \begin{align}
             \left.\frac{\partial \log L}{\partial r}\right|_{r = \hat{r}} &= 0\\
             \implies \sum_{i = 1}^N \frac{x_i}{\hat{r}} - \frac{1 - x_i}{1 - \hat{r}} &= 0\\
             \implies \frac{1}{\hat{r}}\sum_{i} x_i&=\frac{1}{1 - \hat{r}}\sum_i (1 - x_i)\\
             \implies (1 - \hat{r})\sum_i x_i &= \hat{r} \sum_i (1 - x_i)\\
             \implies \sum_i x_i - \hat{r} \sum_i x_i &= N\hat{r} - \hat{r}\sum_i x_i\\
             \implies \hat{r} &= \frac{\sum_i x_i}{N}
         \end{align}
 \end{enumerate}
 
+\medskip
+\noindent\textbf{Interpretation.} The estimator $\hat{r}=\frac{1}{N}\sum_i x_i$
+is the sample proportion of 1's because each $x_i\in\{0,1\}$, so $\sum_i x_i$
+simply counts the observed successes and dividing by $N$ gives their fraction;
+maximizing the Bernoulli likelihood reduces to matching $r$ to the observed
+success rate. This is appropriate when the data really are i.i.d.\ draws from a
+single fixed-$r$ Bernoulli. It misleads when $N$ is very small or when every
+observation is identical: three heads in three tosses give $\hat{r}=1$, asserting
+tails is impossible---an artifact of the tiny sample, not the truth. (A
+$\mathrm{Beta}$ prior / MAP estimate, the optional extension, fixes exactly this
+by pulling the estimate off the boundary.)
+
 }
 %%% Answer END %%%
```

**Why these solution edits (so the reference scores full marks against §2):**
- *Step A* now **names independence** as the reason `L` factorizes → reaches the step-A
  "Exemplary" tier (was Proficient: product correct but independence implicit).
- *Step B* replaces "is always negative … Thus unique maximum" with an explicit
  **strict-concavity ⇒ at-most-one-stationary-point ⇒ unique global max** chain → step-B
  Exemplary (the old text asserted concavity loosely).
- *Step C* is unchanged algebra (already Exemplary) — only a lead-in sentence added for
  Process clarity.
- New **Assumptions and notation** line and **Interpretation** paragraph give the reference
  full **Process (2c)** and full **Interpretation (CERL)** marks, so the answer key models a
  top-scoring submission end-to-end.
- Markers `%%% Answer START/END %%%` untouched; the strip in `make_release` is unaffected.

### 4b. `README.md` — replace the 1/0.5/0 gate with criteria-up-front (TILT)

```diff
--- a/README.md
+++ b/README.md
@@ -1,16 +1,38 @@
-# README
-
-## Instructions
-
-Compile `hw.tex` to a PDF (see the `README.md` file for HW0 for how to do
-this), and complete all the exercises in it.
-
-The solutions to the exercises in `hw.pdf` need to be written up and submitted
-by the beginning of class on the due date. The solutions can be hand-written or
-typeset in LaTeX, whichever you prefer.
-
-# Grading
-
-- 1 point: Homework is complete and correct.
-- 0.5 points: Homework is incomplete or has errors.
-- 0 points: Homework was not submitted on time.
+# HW5 — Maximum Likelihood for a Bernoulli Parameter
+
+> Overhauled (Scope-A pilot, written-derivation template). Grading is **per-step +
+> specifications-based**, not the old complete/incomplete gate. The full rubric ships with
+> the assignment in `rubric.md`.
+
+## Instructions
+
+Compile `hw.tex` to a PDF (see HW0's `README.md` for how), and complete the exercise. Write
+up your solution — hand-written or typeset in LaTeX — and submit a hard copy by the start of
+class on the due date.
+
+## What you'll do
+
+Derive the maximum-likelihood estimator for the parameter `r` of a Bernoulli distribution
+from `N` i.i.d. samples: (1) write the likelihood, (2) show it has a unique maximum, (3)
+derive `r̂`. Then write one short paragraph interpreting the result (see `hw.tex` §"Required
+interpretation").
+
+## Allowed approaches
+
+**Any mathematically valid derivation that reaches `r̂ = (Σxᵢ)/N` earns full credit** — no
+single path is privileged. Maximize `L` or `log L`; argue uniqueness by the second-derivative
+test, strict concavity, or a single sign-change of the score. Just **show the steps**.
+
+## How you'll be assessed (criteria shown up front)
+
+| Bundle | Weight | Pass when… |
+|--------|:------:|------------|
+| **Correctness** | **60%** | per-step derivation rubric (`rubric.md` §2a) — steps A (likelihood), B (unique max), C (closed-form `r̂`) each at **Proficient+**. Any sound route counts. |
+| **Interpretation** | **30%** | the required paragraph reaches **Proficient+** on every Claim/Evidence/Reasoning/Limits dimension (`rubric.md` §2b). |
+| **Process** | **10%** | clear notation, stated assumptions, legible justification (`rubric.md` §2c). |
+
+**Revision:** if a bundle falls short you get **one revise-and-resubmit** in the posted
+window. An LLM may draft per-dimension scores; a human confirms every grade and is final.
```

### 4c. `rubric.md` — NEW file (shipped to students; full content of §2 above)

```diff
--- /dev/null
+++ b/rubric.md
@@ -0,0 +1,62 @@
+# HW5 — Grading rubric (per-step derivation + interpretation)
+
+No autograder: this is a **written** derivation. Grading replaces the old 1/0.5/0 gate with
+per-step partial credit. Criteria are shown here up front (see the repo-root `rubric.md` for
+the shared analytic rubric this instantiates). Weights follow the written/derivation-HW canon
+**60 / 30 / 10** (correctness is human-verified; see the repo-root `rubric.md`).
+
+## §2a · Correctness (60) — per-step derivation rubric
+
+Each step is scored on the **validity of the move**, *not* on matching this key's exact
+algebra. **Any sound alternative route that reaches `r̂ = (Σxᵢ)/N` earns full credit.** Each
+step gets a 0–3 tier (3 → 100% of its points, 2 → 80%, 1 → 45%, 0 → 0%).
+
+| Step | Obj | Pts | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
+|------|-----|:---:|---------------|----------------|----------------|---|
+| **A · Likelihood** | O1 | 13 | `L = ∏ rˣⁱ(1−r)¹⁻ˣⁱ`, independence named | product right, independence implicit | partial / wrong exponents | missing/wrong |
+| **B · Unique max** | O2 | 24 | uniqueness *shown* (strict concavity / `∂²log L/∂r²<0` / single sign-change) | 2nd derivative taken, sign argued loosely | 1st derivative only / asserted | missing/wrong |
+| **C · MLE** | O3 | 23 | clean algebra to `r̂ = (Σxᵢ)/N` | right answer, minor slip | sets up, can't solve | missing/wrong |
+
+**Load-bearing vs. independent.** A is load-bearing for the *values* in B and C but not their
+*moves*: grade B and C on correct manipulation of the student's own `L`; an error in A caps
+final correctness but not method credit. B and C are mutually independent — skipping
+uniqueness (lose B) does not block full credit on C, and vice versa. The log-transform is an
+optional enabling move, never required.
+
+## §2b · Interpretation (30) — Claim / Evidence / Reasoning / Limits
+
+The required paragraph, scored 0–3 on each dimension (12 raw → 30%). PASS = ≥2 each.
+
+| Dim | 3 | 2 | 1 | 0 |
+|-----|---|---|---|---|
+| **Claim** | states `r̂` *is* the sample proportion of 1's | mostly | partial | missing |
+| **Evidence** | grounds it in `Σxᵢ` counting successes, `/N` making a fraction (or a concrete `N`) | some | vague | none |
+| **Reasoning** | links "maximize likelihood" → "match `r` to observed success rate" | sound | superficial | absent |
+| **Limits** | names a real failure + the broken assumption (small `N`; all-identical ⇒ `r̂∈{0,1}`; non-i.i.d.) | one weakly | minimal | none |
+
+## §2c · Process (10) — communication
+
+| Sub-dim | Pts | Full credit when… |
+|---------|:---:|-------------------|
+| Notation | 4 | symbols defined/consistent; `log` base stated |
+| Stated assumptions | 3 | i.i.d. given `r`, `xᵢ∈{0,1}`, `r∈(0,1)` explicit |
+| Justification clarity | 3 | each implication follows; legible |
+
+## Specifications bundle
+
+- **Derivation = PASS:** steps A–C each ≥ Proficient. **Interpretation = PASS:** ≥2 on every
+  CERL dimension. Otherwise **one revise-and-resubmit** in the posted window.
+- An LLM may pre-draft per-dimension scores + one-line reasons; a **human confirms every
+  grade and is final**. (LLM pre-grading is weak on derivations — humans grade A–C; the LLM
+  at most checks the final closed form and drafts the interpretation score.)
```

### 4d. `make_release` — ship `rubric.md` to students (TILT: criteria are visible)

```diff
--- a/make_release
+++ b/make_release
@@ -6,3 +6,4 @@
 sed '/^ *%%% Answer START %%%/,/^ *%%% Answer END %%%/d' hw.tex > release/hw.tex
 
 cp README.md release
+cp rubric.md release
```

> **Optional, not in the diffs:** `requirements.txt` still lists `pytest`/`jupyter`/`numpy`
> etc., which are inert for a pure-written HW. Leaving it untouched keeps the cluster
> uniform; trimming it to nothing (or a comment) is a tidy-up the instructor can opt into.

---

## 5. Effort & budget

| Component | Change vs. current |
|-----------|--------------------|
| Derivation (parts 1–3) | unchanged length (~30–45 min) |
| Interpretation paragraph | **+~10–15 min** (new) |
| Net | within the syllabus 5–6 hrs/week — hw5 is a single short written HW |

**Offset (per task instruction).** The derivation is already minimal (three short steps), so
there is no busywork to trim — the +10–15 min interpretation load is small and absorbed within
budget. If a tighter cap is needed later, the optional Beta/MAP extension (§7) stays ungraded,
adding zero required load. **No derivation trimming required.**

---

## 6. Judgment calls beyond `OVERHAUL_FRAMEWORK.md`

1. **Point split — RESOLVED to 60/30/10.** An earlier draft used 55/35/10 (the first overhaul
   task's instruction); this is now reconciled to the written/derivation-HW canon **60/30/10**,
   keyed to the rule that **correctness is human-verified** (autograded HWs stay 55/35/10). The
   rule is recorded in the repo-root `rubric.md` and `CHANGELOG.md`, matching framework §3/§9.
2. **Process split into 3 named sub-dims (4/3/3).** The task named "notation, stated
   assumptions, justification clarity" for Process 10; I made each an explicit sub-score
   rather than one holistic 10. Reversible to a single holistic tier if preferred.
3. **Correctness as 3 steps (A/B/C), weighted 13/24/23 (sum 60).** Mapped one step per problem
   part / objective (cleaner alignment than 4+ micro-steps). The log-transform is folded into B
   as an optional sub-move rather than its own gradeable step, to avoid privileging the log
   route. Weights are a proposal; any split summing to 60 with B/C heaviest is fine.
4. **`make_release` now copies `rubric.md`.** Framework wants criteria visible to students
   (TILT); the current script ships only `hw.tex` + `README.md`. One-line addition.
5. **Typo fix in the prompt** (`x_i,\dots,x_N` → `x_1,\dots,x_N`). Carried inside the §4a diff;
   noted so it isn't mistaken for scope creep.
6. **No pytest / no `test_hw.py`.** Correct for a pure-written HW; the "Correctness" layer is
   the §2a rubric. Noted so the absence reads as intentional, not an omission.

---

## 7. Commit message

```
hw5 overhaul: 8-part written-derivation prompt, per-step + CERL rubric (S2/S3)

- hw.tex: wrap the unchanged problem in Context/Objectives/Allowed-approaches/
  Criteria/Interpretation/Going-further framing; add an assumptions note, an
  independence + strict-concavity justification, and a reference interpretation
  paragraph, all inside the preserved %%% Answer %%% markers.
- rubric.md (new): per-step derivation rubric (Correctness 60, steps A/B/C
  scored on move-validity, any valid route = full credit) + CERL interpretation
  (30) + Process (10). Shipped to students (TILT).
- README.md: replace the 1/0.5/0 gate with a criteria-up-front specs table.
- make_release: ship rubric.md in the release.

Written-HW split 60/30/10 per repo canon (correctness is human-verified;
autograded HWs are 55/35/10) — rule recorded in repo-root rubric.md + CHANGELOG.
No autograder (pure written). Answer markers + make_release strip preserved.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
