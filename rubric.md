# Shared analytic rubric (interpretation layer)

The single rubric every assignment references for its **interpretation/reasoning**
component. It replaces the course-wide 1/0.5/0 gate. Each interpretation prompt is scored on
four dimensions, **0–3** each.

| Dim | 3 — Exemplary | 2 — Proficient | 1 — Developing | 0 |
|-----|---------------|----------------|----------------|---|
| **Claim** — answers what was asked, correctly | precise, fully correct | mostly correct, minor gap | partial / partly wrong | missing/incorrect |
| **Evidence** — cites the right numbers/plots/output | specific, well-chosen | adequate | vague or thin | none |
| **Reasoning** — connects result to the underlying theory | correct & insightful | sound | superficial | absent/wrong |
| **Limits & clarity** — assumptions, caveats, when it'd fail; clear writing | names real limitations clearly | states some | minimal | none |

## How it maps to grades

- **Within-assignment weight:** Interpretation is **35%** of code HWs, **30%** of written
  HWs (Correctness 55/60%, Process 10%). See `docs/OVERHAUL_FRAMEWORK.md` §3.
- **Specifications grading (ratified scheme):** "Interpretation = PASS" requires **≥ 2 on
  every dimension of every prompt**; otherwise one **revise-and-resubmit** window.
- **LLM pre-grading** may draft per-dimension scores + one-line justifications, **confirmed
  by a human** who is final — never auto-posted (`docs/OVERHAUL_FRAMEWORK.md` §9).

## Written-derivation HWs (hw5, 7, 8, 9, 12, 13)

The **Correctness** layer is a **per-step derivation rubric** (setup → key move → result),
each step scored 0–3 — the same partial-credit principle applied to math instead of prose.
The interpretation rubric above still applies to the short "why/when does this mislead"
prompt each derivation gains. See `assignments/hw5/OVERHAUL.md` for the template instance.
