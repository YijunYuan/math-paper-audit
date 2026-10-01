---
name: math-manuscript-audit
description: Independently review a mathematical manuscript as written, from definitions and proofs through its main conclusions, using a fresh context and verified external statements. Use for a whole-paper mathematical review, not a summary or editing pass.
---

# Whole-Manuscript Mathematical Audit

Perform stage `whole`: determine what the manuscript's actual argument establishes when read as one document.
Read the [shared audit contract](../math-paper-audit/references/audit-contract.md) before work.
For attribution and adaptation notes, see [provenance](../math-paper-audit/references/provenance.md).
Preserve the manuscript. A possible repair is not part of the argument being reviewed until incorporated and rechecked.

## Fresh reviewer boundary

Use a fresh review context with no earlier critiques, proposed repairs, stage verdicts, or expected answer.
Provide the complete raw manuscript snapshot, include/macro/bibliography files, relevant supplied original data/code, a neutral file manifest, and verified external statement evidence.
Neutral location-to-ID mappings may support coverage; do not provide an earlier interpreted proof graph as a substitute for reconstructing the argument.
The external evidence packet must contain source identity/version, precise statement, definitions, hypotheses, and source locators, not just a reference ledger's confidence labels.
Do not give the reviewer a fact graph, research notebook, private intended proof, author assurance, or prior review to fill omissions in the paper.

If you have already seen previous critique or conclusions, arrange a fresh-context reviewer using available delegation tools without inheriting that conversation.
Use available models and record the actual method; do not invent model names or claim different-family review from a fresh context alone.
If a fresh reviewer is unavailable, perform useful direct review, disclose the limitation, and leave the independent-review requirement incomplete.
Do not claim a blind review after erasing only the visible verdict while retaining the earlier reasoning.
The orchestrator records independent-review status and owns `audit.json`; the reviewer returns a separate report.

When invoked alone, label the deliverable a partial specialist review even if its scope is the entire manuscript: it is not the complete six-stage audit.
If the companion contract is missing, retain the work and explain that installation limitation.
No proprietary fact service, paid account, particular plugin, or guessed model is a prerequisite.

## Read the document as written

Read the abstract, introduction, definitions, statements, proofs, remarks, appendices, and conclusion in manuscript order.
Follow local includes and scoped macro definitions so the mathematical reading matches the actual source.
For PDF work, inspect rendered formulas or diagrams whenever text extraction/OCR could change the meaning.
If source and supplied PDF disagree, identify the reviewed snapshot and record the disagreement rather than combining them.
Mark unreadable content as uncovered; do not judge a garbled formula as an error before inspecting it visually.

Reconstruct the assumptions and conclusion of every result, including assertions made without theorem environments.
Check that definitions are meaningful and consistent when first used; track changes in notation and ambient hypotheses.
Identify the paper's main promised results independently from earlier stage summaries.
For each argument, establish which statements it actually uses and whether those premises have been justified or explicitly assumed.
Read forward references through their eventual proofs and check for circular support.
An assumption may be legitimate when stated as a premise; using an unproved conditional result unconditionally is a different obligation.

## Check mathematical closure

For every substantive inference, explain why it follows or identify the exact unresolved obligation.
Pay attention to construction before use, existence of selected objects, simultaneous choices, and well-founded induction.
Track quantifiers, parameter regimes, dependence of constants, exceptional sets, and uniformity across intermediate results.
Check interfaces: the output of one lemma must meet the next result's hypotheses with compatible definitions and notation.
Verify reductions in the necessary direction and ensure all cases, endpoints, degenerate situations, and boundary terms relevant to the stated claim are covered.
Check limits, interchanges, convergence modes, extremizers, equality cases, and computational premises where used.
Do not fill a missing load-bearing step with an intended result from outside the manuscript.

Reconstruct routine omitted steps to assess them; record the reconstruction when it is needed to justify an exposition-only note.
Classify a substantive missing argument as a `gap`, even when a plausible repair is easy to imagine.
A demonstrated invalid inference is an `error`; inability to follow a step without a completed check is not itself proof of falsity.
Do not use a reader's educational level as a correctness criterion or invent findings to demonstrate effort.
Record difficult checks that passed so the report shows the mathematical work behind its conclusion.

## External results remain conditional on their hypotheses

Accept established external theorems without reproving the literature only when the supplied evidence identifies their actual statements and definitions.
A ledger marked “verified,” a matching title, or publication metadata does not supply that evidence.
Independently check each application against the source statement, the manuscript's definitions, and hypotheses established at the use site.
Inspect primary sources through available tools when the packet is insufficient; do not rely on secondary summaries for technical support.
Distinguish unavailable source content (`unverified_reference`) from an unsupported hypothesis (`gap`) and a demonstrated wrong implication (`error`).
If tools or source access are unavailable, state the unresolved import and its downstream effect; do not silently promote it to a valid premise.
Search failure alone does not establish that a source or theorem is nonexistent.
When source versions differ, retain the cited version's claim and identify any correction or proposed replacement separately.

## Long manuscripts

Divide reading by complete results or coherent result clusters, retaining the definitions, assumptions, proof, and cited interfaces needed to judge each cluster.
Do not declare arbitrary page/token slices independently verified when the proof crosses those boundaries.
Maintain neutral coverage and interface records tied to locations; include every section and informal load-bearing claim.
After cluster reviews, conduct an explicit cross-part closure pass through every dependency path supporting each main claim.
At each interface, compare the producer's proved conclusion with the consumer's required premise, including quantifiers and standing assumptions.
Inspect claims outside main-result paths too; a supplementary false assertion is still part of full-manuscript scope.
Reconcile collective definitions, notation, parameter choices, and exceptions across the entire manuscript.
A set of individually completed cluster reviews does not by itself complete this whole-manuscript stage.

## Match promises to results

Compare abstract and introduction promises with formal theorem statements, what the proofs establish, and the conclusion's claims.
Distinguish unconditional results from conditional ones, general results from restricted regimes, proofs from numerical evidence, and conjectures from established statements.
Identify overclaims, missing qualifications, unsupported corollaries, and conclusions stronger than the proven intermediate facts.
Do not silently strengthen hypotheses or weaken conclusions to manufacture agreement.
A repaired statement may be proposed with its implications, but the original claim keeps its finding until the repair is authorized, incorporated, and rechecked.

## Report and handoff

Return a stage report containing:

- Snapshot/scope and the actual independence method, including any unavailable resources.
- Covered and uncovered unit IDs, section/claim coverage, and the independently recovered dependency/interface structure.
- Substantive reasoning for the main results and difficult successful checks, including the cross-part closure pass.
- Findings in the shared shape: exact location/text, reasoning, affected results, category/severity, and specific proposed action.
- Newly discovered units or dependency changes for the orchestrator to reconcile into all affected stages.

Keep missing proof, false inference, reference uncertainty, unfinished work, and presentation notes distinct.
Do not close a finding merely because another reviewer disagrees; resolving it requires mathematical evidence and downstream rechecking.
The orchestrator may compare reports only after this fresh report is complete and preserved.
If later evidence changes the conclusion, record the subsequent reconciliation separately instead of rewriting the history of the blind pass.

`whole` always applies and its scope is all units, including sections, definitions, citation uses, and computations.
Use `completed` only when all scoped content and cross-part interfaces have been checked; an examined defect still counts as reviewed.
Unread material or an unexamined essential import remains uncovered, even if no other defect was found.
Report what is established and what is unresolved; do not issue a proof certificate or equate an empty findings list with complete coverage.
