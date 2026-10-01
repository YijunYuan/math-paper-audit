---
name: math-proof-audit
description: Review the logical validity of mathematical manuscript proofs, including quantifiers, hidden assumptions, lemma applications, and dependencies. Use for proof checking, proof verification, or a scoped proof audit; reports defects and proposed repairs without changing the manuscript by default.
---

# Mathematical proof audit

Check every proof obligation in the assigned scope against the actual manuscript. Distinguish a false mathematical step, a missing justification, and a concise but valid argument. This is a specialist review, not a formal correctness certificate.

## Contract and scope

Read the [shared audit contract](../math-paper-audit/references/audit-contract.md) before reviewing. Use stage ID `proof` and its finding schema. In a coordinated audit, receive the frozen input list, unit IDs, dependencies, and report destination; return a stage report without editing the orchestrator's `audit.json`.

For a standalone request, identify the requested statement, proof, definitions, and necessary dependencies. Assign local unit IDs and report a **partial specialist review**; a six-stage ledger is unnecessary. If the shared contract is missing, retain useful work and state the installation limitation.

- Include all assigned `requires_proof` units, including informal assertions and appendix arguments. Do not silently select only the most important theorem.
- Record newly discovered obligations or dependency changes for the inventory and earlier-stage review. A sentence being outside a theorem environment does not exempt it.
- Read definitions, local conventions, macros, and relevant surrounding text before judging a step. For ambiguous PDF extraction, verify the displayed formula visually.
- Review only. Suggest repairs with their mathematical consequences; edit the source only when the user has authorized repairs. Never silently change a hypothesis or conclusion.

## Review method

1. Restate each claim faithfully for internal checking: object types, domains, all hypotheses, quantifier order, conclusion, and stated parameter ranges. Separate assumptions from conclusions used later as premises.
2. Trace its dependency chain. Read the actual predecessor statement and the relevant proof when within scope. Identify circular reasoning, forward references, and induction obligations; a legitimate joint induction needs a well-founded argument.
3. Read the proof in its own order, also tracking which facts are available at each step. Break it into meaningful obligations rather than mechanically creating a record for every sentence.
4. For each nontrivial inference, identify its premises and derive the asserted conclusion. Test substitutions, inequality direction, signs, exceptional cases, quantifier scope, and the existence and properties of introduced objects.
5. For every local or external lemma application, map source hypotheses to the objects at the point of use. Check the exact conclusion obtained, including topology, regularity, constants, and dependence on parameters. A source title or familiar theorem name is insufficient evidence for an unchecked variant.
6. Track changes in ambient assumptions through cases, contradiction arguments, localization, approximation, and limiting steps. Verify that the proof eventually establishes the stated conclusion for every allowed case.
7. Inspect important omitted steps by reconstructing them. Accept routine concise exposition when the reconstruction is valid. Record a load-bearing missing argument as `gap`; do not reject prose merely for saying “standard” or “similarly.”
8. Recheck each candidate finding against the full definitions and nearby arguments. Give a derivation or counterexample for a claimed false step; explain why an unavailable justification remains a gap or unverified reference instead.

Use the relevant parts of [the proof checklist](references/proof-checklist.md) for domain-specific steps. It is a routing aid, not a requirement to test unrelated mathematical domains.

## Decision rules

- A false intermediate assertion can invalidate the supplied proof without disproving the theorem. State that distinction and identify downstream uses.
- A missing hypothesis at a lemma application is a gap unless it can be derived from the manuscript; a counterexample must satisfy the theorem's full assumptions before it refutes that theorem.
- An apparently unused hypothesis is a prompt to inspect the argument. It is not by itself an error: it may be redundant or belong to a deliberately stronger statement.
- If an imported result cannot be inspected, record `unverified_reference` with the exact application still needing verification. Continue checking the paper's internal reasoning that does not depend on resolving it.
- Do not make up source theorems or treat agreement between agents as proof. Use inherited model settings and available tools; there is no mandatory external verifier or plugin.
- A proposed repair may require a new lemma, stronger assumptions, or a weaker conclusion. Say which, and propagate the consequences. A proposal is not a resolved finding.

## Stage report

Return the following, using actual source or page locators:

1. `proof` stage status, scope IDs, reviewed IDs, and uncovered IDs with reasons.
2. For each obligation, the argument checked and the relevant premise-to-conclusion reasoning. Include substantive checks that passed, especially fragile limit, existence, and theorem-application steps.
3. Findings in the shared shape, with evidence, precise reasoning, affected units, and a concrete suggested action. Merge duplicate manifestations of one defect without losing affected locations.
4. New units, corrected dependency edges, and any imported assumptions requiring another stage's attention.

`completed` means all scoped obligations were examined, including those found defective; it does not mean they were accepted. Mark unfinished obligations `blocked` with partial coverage and the specific missing evidence. Use `not_applicable` only for an empty proof scope justified by reading the supplied material. Lack of tools, time, or understanding is not non-applicability.

Credit: adapted in part from Danus sequential verification and worker proof-review ideas; see [shared provenance](../math-paper-audit/references/provenance.md). Danus runtime instructions and correctness-authority claims are not part of this skill.
