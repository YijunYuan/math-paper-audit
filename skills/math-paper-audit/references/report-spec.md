# Consolidated report specification

Use the manuscript's language, following the [shared report-language rule](audit-contract.md#report-language), and the user's requested format. Translate the headings and explanatory text below into that language when composing the report. Default to a readable report plus the machine-readable `audit.json`; do not create several overlapping final reports. Preserve detailed stage evidence as supporting files.

## Essential content

1. **Outcome and exact scope.** Identify the manuscript/version, input hashes or link to them, the helper-derived outcome, whether the review covers the whole manuscript, exclusions and review independence. State that mathematical acceptance is an LLM review judgment. If coverage is incomplete and errors were also found, state both.
2. **Coverage table.** Stage; result/section scope; reviewed count vs scoped count; completed/not applicable/blocked; concise evidence or limitation. Include unreviewed units by ID and location, rather than a vague percentage. Note unresolved extraction or missing-source problems.
3. **Mathematical and reference issues.** For each issue: ID, category/severity, precise location, manuscript statement, why it fails or lacks support, a derivation or checked counterexample, affected downstream results, and a concrete proposed repair. A critical claim deserves enough mathematics to reproduce the objection. Do not paste raw TeX macros the reader cannot understand.
4. **Unresolved verification.** Separate inaccessible sources, unavailable computations, unresolved reviewer disagreement and unreviewed material from established mathematical errors. An unverified citation can prevent confidence without proving the cited claim false.
5. **Editorial notes.** Keep notation, readily reconstructible omitted steps, typos and cross-reference problems separate. For typographic issues prioritize rendered-visible mistakes; source indentation is not a correctness finding.
6. **Checked difficult points.** Briefly identify the most consequential arguments checked successfully and the evidence. No exhaustive praise, invented checks or assurance percentages.
7. **Repair impact when applicable.** Distinguish proposed fixes from applied fixes, exact hypothesis/conclusion changes, and the rechecks actually performed. Include remaining open issues. Link the detailed reports and reproducible calculations.

## Wording discipline

- `error`: explain the invalid inference or a counterexample satisfying all hypotheses. A proof error alone does not establish that the theorem is false.
- `gap`: name the exact missing obligation and why the existing text/citation does not discharge it; avoid generic requests for more detail.
- `unverified_reference`: record what was searched/read and what remains unconfirmed. Do not say nonexistent merely because retrieval failed.
- `incomplete_check`: name the inaccessible material or unperformed test and its potential scope, without speculating that it must be wrong.
- `exposition`: provide the valid short reconstruction that distinguishes it from a mathematical gap.
- Never describe numerical success on samples, a compiled PDF, repeated reviewer agreement, or an empty issue list as a proof certificate.

For a single theorem or standalone specialist request, scale the report down while keeping exact scope, evidence and limitations. For a full manuscript, no source section should silently disappear from the coverage table.
