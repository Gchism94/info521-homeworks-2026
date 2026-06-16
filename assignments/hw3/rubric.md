# HW3 — Interpretation rubric

Each of prompts **I1–I3** (see `README.md` §6) is scored on four dimensions, **0–3**.
"Interpretation = PASS" requires **≥ 2 on every dimension of every prompt**; otherwise one
revise-and-resubmit in the posted window. (Shared analytic rubric; see the repo-root
`rubric.md`.)

| Dim | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
|-----|---------------|----------------|----------------|---|
| **Claim** | names the CV-selected order / the overfitting signal / a real failure mode correctly | mostly right, minor gap | partial | missing/wrong |
| **Evidence** | cites the CV-curve minimum and the train-vs-CV gap from *your* plot | cites some numbers | vague | none |
| **Reasoning** | ties it to variance rising with model complexity (bias–variance) | sound | superficial | absent/wrong |
| **Limits** | names a real caveat (tiny N, leakage, non-i.i.d.) | states one weakly | minimal | none |

**Exemplar for I2.** Cites the CV curve's minimum and the widening train-vs-CV gap
(Evidence), explains it as variance growing with polynomial order (Reasoning), and notes the
conclusion is specific to this dataset / sample size (Limits).

**LLM pre-grading.** An LLM may propose pass/revise + a one-line reason per dimension; a
human confirms every grade and is final. Students are told an LLM assists grading.
