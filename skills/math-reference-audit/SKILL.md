---
name: math-reference-audit
description: Verify mathematical citations against authoritative source statements and check each application, including definitions, hypotheses, theorem versions, and derived conclusions. Use for citation and imported-result audits, not bibliography formatting alone.
---

# Mathematical Reference Audit

Perform stage `references`: verify what each source actually establishes and whether the manuscript may use it here.
Read the [shared audit contract](../math-paper-audit/references/audit-contract.md) before work.
For attribution and adaptation notes, see [provenance](../math-paper-audit/references/provenance.md).
Preserve manuscript and bibliography; corrections are proposals unless the user requested edits.

## Scope and available evidence

Receive the fixed snapshot, all scoped citation-use units, relevant definitions/proof passages, and an output path.
Use the actual manuscript to detect missing citation uses; one bibliography entry can support several materially different applications.
Read enough surrounding argument to know the conclusion being imported, not just the text inside `\cite`.
Inspect custom citation macros, prose attributions, appendices, and assertions described as standard or classical.
Check bibliography-only entries for identity and broken/inconsistent metadata as well. Add a citation unit labelled bibliographic-only for an otherwise unused entry; it has no mathematical application to discharge. Flag missing cited entries and unresolved keys, but do not invent an application for an uncited source.
Return newly discovered units and scope changes to the orchestrator; never edit its shared `audit.json` concurrently.

When used alone, label the result a partial specialist review and define exactly which citation uses were checked.
If the companion contract is missing, keep the work and disclose the installation limitation.
No Danus service, special theorem-search connector, paid account, plugin, or particular model is required.
Use available file and web tools. If an essential source cannot be accessed, retain an unverified outcome and continue other checks.

## Separate identity from mathematical support

For every citation use, establish two distinct facts:

1. **Source identity:** the cited authors, title, version/edition, publication status, and locator refer to the source actually consulted.
2. **Application validity:** the source's exact result, definitions, and hypotheses justify the manuscript's asserted consequence.

A matching title, DOI landing page, abstract, bibliography row, or “verified” ledger label establishes neither theorem content nor applicability by itself.
Operator assertions and earlier verification reports may help locate evidence; they are not substitutes for checking it.
A real source can be cited incorrectly; a bibliographic typo can coexist with a valid mathematical application.
Keep these outcomes separate instead of assigning a single undifferentiated “verified” badge.

## Locate authoritative evidence

Prefer the cited primary source: publisher-hosted paper, author manuscript, official preprint repository, or the cited book/edition.
Use authoritative bibliographic records to establish metadata only; use actual source text for mathematical statements.
Use targeted public queries containing the title, authors, theorem locator, or a concise mathematical phrase.
Do not upload an unpublished manuscript or its complete text to an external service.
Search results and secondary summaries are navigation aids; the final mathematical comparison must rely on primary sources.

Open the relevant theorem and its surrounding definitions, assumptions, conventions, and qualifications.
Record the exact source URL or local supplied-source path, access date, version/edition, and page/result locator.
When versions differ, inspect the cited version and any relevant correction; report changes in numbering, hypotheses, or conclusion.
Do not silently substitute a stronger theorem from another paper or a later version.
If a replacement source would repair the argument, report it as a proposed repair and separately assess the original application.

For source PDFs, visually verify ambiguous mathematical extraction before comparing formulas.
Resolve notation through the source's own definitions; source and manuscript may use identical words for different properties.
If content is paywalled, missing, or unreadable, try accessible primary versions or supplied copies without treating search failure as evidence of fabrication.
After reasonable targeted attempts fail, record exactly what was searched and what evidence is missing.
Do not claim a theorem nonexistent merely because no search result was found.

## Compare the actual application

For each use, write an application record with:

- Citation unit ID and precise manuscript location.
- The manuscript's imported assertion and the conclusion it draws from it.
- Source identity/version and exact theorem, proposition, lemma, or definition locator.
- A faithful statement of the necessary source hypotheses and conclusion, with exact formulas and quantifiers where decisive.
- Source-to-manuscript notation and definition correspondence.
- Evidence for each required hypothesis at the point of use, including the local result or assumption supplying it.
- The specialization, transformation, or derivation from the source conclusion to the claimed consequence.
- Separate metadata and mathematical outcomes, with unresolved evidence stated explicitly.

Check the direction of implications and the scope of each quantifier.
Compare ambient categories/spaces, topology, regularity, integrability, finiteness, boundary conditions, parameter restrictions, and exceptional cases as relevant.
Check whether the source provides existence, uniqueness, effective bounds, uniformity, rates, or a stronger mode of convergence than the manuscript actually needs.
Track dependence of constants and choices; pointwise conclusions do not automatically supply uniform ones.
Verify hypotheses using the paper's established premises, not a desired downstream conclusion.
If the application has several steps, verify the transition as well as the cited theorem itself.

An exact match of theorem language still requires hypothesis discharge and compatible definitions.
A source proves only a conditional statement when its premise remains conditional; do not promote it to an unconditional fact through a citation chain.
Follow relevant chains to a precise established result when the cited passage merely delegates the needed assertion elsewhere.
Do not demand reproving a verified imported theorem; examine its use and unresolved conditions.
For contextual or historical citations with no proof role, record that role and verify the attributed claim to the extent it affects the audit.

## Classify evidence honestly

Apply the common categories rather than Danus-specific verdicts:

- A demonstrated mismatch that invalidates the inference is an `error`, with the failed implication or a verified counterexample explained.
- A required hypothesis or transition that the manuscript has not established is a `gap`; do not claim the final theorem false without evidence.
- An unavailable source, unresolved theorem locator, or unconfirmed version is an `unverified_reference`.
- Work that has not actually been performed is an `incomplete_check`.
- A purely bibliographic or locator defect may be `typo` or `exposition` when actual support and applicability have been checked.

A vague citation is not automatically harmless: assess whether the needed statement can be identified and whether ambiguity affects the argument.
A bare absence of citation is not automatically a false claim; record a valid reconstruction if routine, or identify the missing load-bearing argument.
Do not silently add hypotheses or replace a cited result and then mark the original use correct.
Retain evidence of valid difficult applications as well as defects.

## Stage handoff

Return one application record per scoped use, findings in the contract shape, covered/uncovered IDs, source-access limitations, and inventory additions.
Provide the verified external statement evidence as a separate neutral packet suitable for a blind whole-manuscript reviewer.
That packet includes source statements, definitions, exact locators, and provenance; exclude earlier critiques, application verdicts, and suggested repairs.
Metadata-only evidence must be labelled as such and must not become a verified mathematical premise.

Stage completion requires every scoped citation use to have been substantively checked.
An inaccessible essential statement leaves that use uncovered and the stage blocked with an `unverified_reference`; metadata verification alone does not close it.
If the actual manuscript has no citation uses, `not_applicable` needs an empty scope and a concrete reason based on reading, not a failed search.
Report conditional downstream conclusions where unresolved imports remain; never equate an empty findings list with verified references unless the coverage record supports it.
