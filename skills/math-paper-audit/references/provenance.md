# Provenance and adaptation

This seven-skill bundle adapts the review methodology and selected procedural ideas of **Danus**, Copyright 2026 FrenzyMath, distributed under Apache License 2.0. A copy of the upstream license is included in each skill's `LICENSE`; each `NOTICE` identifies the adaptation. Upstream snapshot: branch `codex`, commit `6d92e8d415933ca2ef52fd1a4da73fdfcd418f1c`, inspected 2026-09-30.

Source repository: https://github.com/frenzymath/Danus

## Upstream source map

- Sequential proof review, existence/hypothesis checks: `agents/skills/verify/verify-sequential-statements/SKILL.md`.
- Exact external-statement/definition/quantifier matching: `agents/skills/verify/check-referenced-statements/SKILL.md`.
- Located errors, gaps and repair hints: `agents/skills/verify/synthesize-verification-report/SKILL.md`.
- Explicit intermediate results and dependencies: `agents/skills/worker/verify-proof/SKILL.md` and `agents/contracts/verifier.md`.
- Falsification and simpler cases: `agents/skills/worker/construct-counterexamples/SKILL.md` and `construct-toy-examples/SKILL.md`.
- Citation auditing and primary-source confirmation: `agents/skills/write-paper/roles/REFERENCE_AUDITOR_PROMPT.md` and `REFERENCE_VERIFIER_PROMPT.md`.
- As-written whole-manuscript review: `agents/skills/write-paper/roles/PAPER_MATH_VERIFIER_PROMPT.md`, `.agents/skills/write-paper/SKILL.md`, and `danus/write_paper/server.py`.
- Dependency tracking, revocation and the LLM trust boundary: `ARCHITECTURE.md`, `docs/concepts.md`, `docs/security-and-trust.md`.

Pinned source URLs have the form `https://github.com/frenzymath/Danus/blob/6d92e8d415933ca2ef52fd1a4da73fdfcd418f1c/<path>`.

## Deliberate changes in this adaptation

These files are a substantial rewrite for auditing **existing manuscripts**, not an installation of Danus or its automatic proof-search/writing system. The companion skills execute sequentially under one orchestrator; they require no Danus MCP gateway, graph server, theorem-search service or provider credentials.

- Separate false inference, incomplete proof, unverified reference and incomplete review. A failed search is not proof of nonexistence; a gap does not refute the theorem.
- Explicit source snapshot, coverage inventory, review scope and deterministic accounting, rather than trusting a model-authored pass/fail string.
- Full source-theorem applicability checks even when bibliography metadata is confirmed; the whole-paper reviewer receives actual source statements and conditions.
- Optional bounded exact/symbolic/numerical reproducibility checks, with evidence strength recorded. Danus's text-only computation restriction is not carried over.
- Fresh review plus transparent same-context fallback, without a hard-coded model, unsupported external reviewer requirement or majority-vote acceptance.
- Preserve manuscripts during audit; no automatic theorem weakening, source rewriting, paper publishing or uploads.
- Routine omitted steps can be reconstructed and reported as exposition; genuinely missing mathematical arguments remain gaps. Domain-specific regular-expression rejection rules from past Danus projects are not copied as universal mathematical criteria.
- A digest/inventory/dependency checker certifies only bookkeeping consistency. The audit outcome never claims formal mathematical verification.

The existing local `proof-checker` and `proofreading-kit` skills were consulted to avoid workflow conflicts; they are not runtime dependencies and are not modified by this bundle. There are no mandatory wiki, HTML renderer, cross-family reviewer or LaTeX toolchain dependencies.

Skill packaging follows the standard `SKILL.md` plus optional references/scripts/metadata structure documented at https://developers.openai.com/plugins/build/skills (consulted 2026-09-30).
