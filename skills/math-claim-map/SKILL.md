---
name: math-claim-map
description: Map a mathematical manuscript's claims, definitions, assumptions, citation uses, computations, and proof dependencies before or during a rigorous audit. Use for LaTeX, PDF, or prose manuscripts, including those without named theorems.
---

# Mathematical Claim Map

Build the coverage inventory and dependency graph for stage `map`.
Read the [shared audit contract](../math-paper-audit/references/audit-contract.md) before work.
For attribution and adaptation notes, see [provenance](../math-paper-audit/references/provenance.md).
Preserve the manuscript; an audit request authorizes reports, not rewriting statements or proofs.

## Inputs and scope

Use the fixed manuscript snapshot, its declared input manifest, and the requested scope.
Read actual source and rendered mathematical content where needed; old reviews and author summaries are not substitutes.
Follow the manuscript's mathematical development through appendices, supplementary arguments, and relevant local imports.
Explicit user exclusions remain visible; do not describe a restricted review as full-manuscript coverage.
When used alone, produce a partial specialist report and inventory; a six-stage ledger is unnecessary.
If the companion contract is missing, retain the work and disclose the installation limitation.

## Resolve the document

1. Identify the root manuscript and edition. Follow `\input`, `\include`, bibliography files, local packages, and relevant generated inputs.
2. Read notation-defining macros, theorem wrappers, conditional branches, and redefinitions in their actual scope.
   A search for standard theorem environments is only a navigation aid: custom commands and prose can contain mathematical claims.
3. List included, excluded, missing, unreadable, and ambiguous inputs. Return additions to the orchestrator for hashing; do not edit its shared `audit.json`.
4. If source and PDF disagree, record the mismatch and identify the reviewed version; do not blend versions into a synthetic proof.
5. For PDF-only work, inspect rendered equations, diagrams, superscripts, subscripts, and quantifiers whenever extraction is ambiguous.
   OCR is an aid, not mathematical evidence. A formula whose visual reading remains unresolved is an incomplete check.
6. Anchor each unit to an actual file and line plus label, or PDF page plus equation/result/paragraph locator.
   Use textual locators when needed; never invent line numbers or assume PDF page numbers match printed ones.

## Inventory every mathematical obligation

Read every section, including the abstract, introduction, conclusion, and appendices.
Create stable, unique IDs with the contract's unit fields:

`id`, `kind`, `location`, `statement`, `assumptions`, `depends_on`, `requires_proof`, `is_main`.

Use these kinds according to function:

| Kind | What to inventory |
|---|---|
| `section` | Every section or analogous unsectioned block, with its purpose and coverage locator. |
| `definition` | Definitions, standing conventions, notation, ambient spaces, and substantive changes of meaning. |
| `claim` | Named results and informal assertions, reductions, constructions, estimates, existence claims, equivalences, and conclusions. |
| `citation` | Each mathematical or contextual use of an external source, with its location and the proposition attributed to it. |
| `computation` | Symbolic, numerical, algorithmic, experimental, tabular, or graphical evidence used to support a claim. |

Repeated uses of one bibliography key are separate citation units when their use or hypotheses differ.
Include otherwise unused bibliography entries as citation units labelled bibliographic-only so their identity can be checked without inventing a mathematical application.
Record uncited imported assertions such as “standard compactness gives…” as claim obligations; identify the proposed outside dependency without inventing a citation.
Do not make every algebraic token a unit. Group a routine contiguous derivation as one obligation only if its extent and dependencies remain inspectable.
Do not hide an independent substantive claim inside a large section unit.

For each claim, preserve the stated conclusion and all quantifiers, domains, constants, uniformity, parameter ranges, and exceptional cases.
Distinguish what the paper states, what it assumes, what it attempts to prove, and what remains conjectural.
Set `requires_proof` for obligations whose validity the manuscript asserts or relies on, including informal ones.
A genuine premise or conjecture is not a proved claim, but its later use as an established result must be exposed.
Mark the actual principal contributions as `is_main`; include matching promises in the abstract and conclusion.
A paper without a theorem environment still has sections and may have many proof obligations; `map` is never not applicable.

## Recover actual dependencies

Read each argument, not just its cross-references.
For unit A, `depends_on` lists units B that A actually needs; every target must exist.
Track definitions, local lemmas, external theorem uses, computational premises, and shared construction choices.
Record the step and mathematical reason for each substantive dependency in the stage report.
Separate declared citations from unacknowledged logical dependencies, and repair the inventory rather than treating a missing label as no dependency.
Do not add an edge merely because two units occur together or one appears earlier.

For each result, collect its explicit and inherited assumptions and identify their origin.
Follow changes in hypotheses across lemmas: regularity, compactness, positivity, nonemptiness, dimension, boundary conditions, independence, and parameter restrictions as relevant.
Check that local choices can be made together and that constants or exceptional sets have the stated dependence.
Record missing or silently strengthened assumptions without rewriting the original statement.

Inspect forward references and circular chains, including cycles hidden through definitions, reductions, or imported local results.
Do not delete an edge to make the graph acyclic.
If mutual induction or a simultaneous construction is legitimate, represent it as one joint proof obligation with its well-founded argument and retain the internal structure in the report.
Otherwise retain the cycle, identify the affected results, and add an explained `gap` or `error` finding for the manuscript's circular reasoning.
An accurately recorded manuscript cycle means mathematical issues were found; do not delete true edges merely to clear an accounting check.
An acyclic graph is only a coverage aid; it does not establish the truth of any inference.

## Coverage handoff

Return the unit inventory, assumptions table, dependency explanations, and any findings in the shared shape.
Include a section-by-section coverage table so a reviewer can see what was read and what remains unread.
Give the orchestrator the proposed stage scopes:

- `map` and `whole`: all units.
- `references`: all citation-use units.
- `proof`: all units with `requires_proof: true`.
- `stress`: all main claims and all claims requiring proof.
- `computation`: all computation units.

New obligations discovered in later stages must be added to the inventory and relevant earlier scopes before those stages can remain completed.
Do not treat the number of search matches, parsed environments, or successful file reads as proof of complete coverage.
Reconcile the inventory against the whole text, including unnumbered remarks and claimed consequences.

Return stage status, scoped/reviewed/uncovered IDs, reasons for omissions, substantive evidence, and inventory changes.
Use `completed` only when the entire declared inventory scope has actually been mapped; otherwise use the contract's blocked/partial accounting.
Even a manuscript with obvious errors deserves an accurate map of affected and independent results.
