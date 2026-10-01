---
name: math-stress-test
description: Stress-test mathematical claims with verified examples, boundary cases, and counterexample searches. Use for counterexample checking, counterexample searches, testing theorem sharpness, or the counterexample stage of a manuscript audit; distinguishes a refutation from an unsuccessful search.
---

# Mathematical stress testing

Probe the stated claims and fragile proof steps with examples that expose where the hypotheses matter. A failed search is not a proof; an example violating a hypothesis is not a refutation of the original claim.

## Contract and scope

Read the [shared audit contract](../math-paper-audit/references/audit-contract.md). Use stage ID `stress`, the common finding schema, and the assigned input snapshot and report destination. Do not concurrently edit the orchestrator's `audit.json`.

In a coordinated audit, scope all main claims and all claims requiring proof, with deeper attention to fragile ones. Audit every assigned unit; record new target claims or dependencies for the inventory. Read the exact statements, definitions, and relevant proof before constructing tests.

In standalone mode, identify the requested claims and their assumptions, assign local unit IDs, and label the output a **partial specialist review**. Do not imply coverage of the whole manuscript. If the companion contract is unavailable, keep the work and explain the installation limitation.

This is review-only unless the user authorizes manuscript changes. Proposed corrections, stronger hypotheses, and restricted statements remain proposals.

## Build the tests

1. Translate each target into its exact logical assertion, including quantifier order, admissible object classes, parameter ranges, and dependencies of constants. Write what would negate that assertion.
2. Identify the mechanism most likely to fail: an endpoint, missing compactness or integrability, a nonuniform estimate, a noncommuting limit, an exceptional algebraic case, or a local-to-global step.
3. Choose simple examples first: extremal or degenerate objects, low dimensions, constant or explicit solutions, finite sets, and exactly computable instances. Check whether the hypotheses are jointly satisfiable, rather than assuming a nonempty class.
4. Use the relevant families in [the stress checklist](references/stress-checklist.md). Search bounded, purposeful families and adapt to evidence instead of collecting random examples.
5. For every serious candidate, explicitly verify **all** hypotheses, including definitions and standing assumptions outside the theorem. Evaluate the conclusion in the same sense and topology as stated.
6. If the candidate fails a hypothesis, discard it as a refutation. It may still illustrate sharpness or motivate a separate claim with weaker assumptions; label that different target explicitly.
7. If an experiment suggests failure, turn it into an exact derivation or a certified argument when possible. Keep floating-point anomalies and unproved pathological constructions as candidates, not established counterexamples.
8. Recheck a proposed refutation against the manuscript's conventions and proof. Determine whether it refutes the theorem, only a stronger intermediate assertion, or a particular proof route.

## Interpret results precisely

Use a descriptive result for each attempted family, separate from the common stage status:

- `refuted`: a concrete admissible example and rigorous demonstration of the failed conclusion. Create an `error` finding and identify affected uses.
- `no_refutation_found`: the specified family was meaningfully checked and gave no counterexample. Record its bounds and limitations; make no inference of general validity.
- `candidate_unresolved`: a candidate has an unverified hypothesis or conclusion. State the missing argument. An unresolved item needed for the assigned review remains incomplete.
- `illustrative_only`: a correct toy example or sharpness example for a modified statement. Explain its limited relevance.

For quantified statements, a refutation must contradict the actual quantifiers. For example, one failed choice does not refute an existence claim, and one large value does not refute an unspecified uniform bound without a family proving unboundedness.

Toy examples can clarify the argument but do not discharge proof obligations. Do not “repair” a theorem by dropping the difficult cases without identifying a changed statement.

## Tools and stopping

Use direct mathematics and available tools. Small exact computations or controlled numerical searches can guide candidates; coordinate reproducible calculations with `math-computation-audit` when available, without requiring it. Use inherited model settings, with no required verifier service or plugin.

Define a meaningful search family and stopping condition for each target. Exhaustion of that declared search can complete a stress check, but cannot prove the theorem. Lack of access, unreadable formulas, unfinished required checks, or an unexplored target must remain visible as incomplete coverage. Continue independent targets when another is blocked.

Do not execute supplied manuscript code merely to generate examples. For computational probes use inspected, narrowly scoped calculations and preserve inputs, settings, and outputs that support the report.

## Stage report

Return stage status, scope/reviewed IDs, uncovered IDs with reasons, and for each target:

1. Exact target and its logical negation.
2. Chosen example families, reason for selection, parameter/search bounds, and actual checks.
3. Candidate constructions, hypothesis-by-hypothesis verification, and conclusion evaluation.
4. Result labels above, common-schema findings, downstream impact, and proposed next action.

Include failed attempts when they constrain interpretation or prevent repeated work; do not fill the report with uninformative abandoned guesses. Mark `completed` only when each assigned target received substantive testing. `not_applicable` requires an empty applicable scope justified from the text; a hard search or unavailable tool is not a reason for it.

Credit: adapted in part from Danus counterexample and toy-example workflows; see [shared provenance](../math-paper-audit/references/provenance.md). No Danus memory service or runtime is required.
