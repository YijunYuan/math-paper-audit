# Mathematical Paper Audit

Seven agent skills for reviewing the correctness and rigor of mathematical manuscripts. One orchestrator runs six specialist reviews in sequence, tracks coverage and proof dependencies, and consolidates findings with precise locations and mathematical evidence.

Adapted from [Danus](https://github.com/frenzymath/Danus), with a focus on auditing existing manuscripts. No Danus service, API key, or particular model is required.

## Review workflow

Invoke **`math-paper-audit`** to run the complete workflow:

| Order | Skill | Review scope |
|---|---|---|
| 1 | [`math-claim-map`](skills/math-claim-map/SKILL.md) | Claims, definitions, assumptions, citations, and proof dependencies |
| 2 | [`math-reference-audit`](skills/math-reference-audit/SKILL.md) | Exact source statements, hypotheses, and each citation's applicability |
| 3 | [`math-proof-audit`](skills/math-proof-audit/SKILL.md) | Logical steps, quantifiers, hidden assumptions, and proof gaps |
| 4 | [`math-stress-test`](skills/math-stress-test/SKILL.md) | Counterexamples, boundary cases, degeneracies, and sharpness |
| 5 | [`math-computation-audit`](skills/math-computation-audit/SKILL.md) | Formulas, estimates, asymptotics, and computational evidence |
| 6 | [`math-manuscript-audit`](skills/math-manuscript-audit/SKILL.md) | Independent review of whether the full manuscript establishes its main conclusions |

The orchestrator executes every stage, saves its evidence, and reconciles findings after the independent review. A specialist can also be invoked separately for a scoped review.

The manuscript is preserved unless repairs are requested. All skill instructions are in English; **reports follow the manuscript's language**, regardless of the conversation language.

## Install

Clone this repository or download its source archive:

```sh
git clone https://github.com/YijunYuan/math-paper-audit.git
```

Copy **all seven directories inside `skills/`** into one of the skill directories supported by your harness. Keep them as siblings, including their references, scripts, notices, and licenses; copying only `SKILL.md` or only the orchestrator breaks the shared references.

| Harness | Personal installation | Project installation |
|---|---|---|
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` |

These locations follow the current [Codex](https://developers.openai.com/codex/skills), [Claude Code](https://code.claude.com/docs/en/skills), and [OpenCode](https://opencode.ai/docs/skills) documentation. An existing Codex installation may also expose personal skills through `$CODEX_HOME/skills`; use the location configured by your installation and avoid duplicate copies of the same skills.

For example, after cloning, a fresh Claude Code installation should contain:

```text
~/.claude/skills/
  math-paper-audit/
  math-claim-map/
  math-reference-audit/
  math-proof-audit/
  math-stress-test/
  math-computation-audit/
  math-manuscript-audit/
```

Review any existing directories with these names before replacing them. Reload or restart your harness if the new skills do not appear.

## Use

In Codex:

```text
Use $math-paper-audit to audit this manuscript's correctness and rigor.
Execute all six specialist reviews in sequence, preserve the manuscript,
and produce one consolidated report in the manuscript's language.
Include precise locations, mathematical evidence, affected results,
proposed repairs, and everything that could not be verified.
```

In Claude Code:

```text
/math-paper-audit Audit the manuscript at /path/to/main.tex.
```

In OpenCode, ask the agent to load and execute the `math-paper-audit` skill on your manuscript using its native skill tool. The `$skill-name` spelling in Codex prompts is not a universal command syntax.

Supply the current LaTeX source and includes when available, or a readable PDF. Add appendices, bibliography files, and computation inputs relevant to the claims. Request LaTeX or another report format explicitly if needed.

## Harness compatibility

The core instructions use the shared `SKILL.md` format, relative file references, and standard-library Python. Their format matches the documented skill interfaces of Codex, Claude Code, and OpenCode. The complete workflow has been exercised in Codex; an end-to-end run in Claude Code or OpenCode has **not** yet been validated.

- Use the host's native skill-loading, file-reading, shell, browsing, and subagent tools. Tool names are not hard-coded into the review workflow.
- `agents/openai.yaml` supplies optional Codex interface metadata. Other harnesses can use the core skills without interpreting it.
- The bookkeeping helper requires Python 3.7 or later; a currently supported Python release is recommended. No third-party Python package is required for it or its tests.
- A fresh subagent is used for the final independent pass when available. Without one, the workflow records that independent review was unavailable and continues with a disclosed same-context review.
- External references need accessible source texts or retrieval tools. Missing tools or sources become explicit verification limits.
- Built-in document editors and compilers are optional. Use the document tools available in the host environment when a particular output format is requested.

Skill files define a procedure; they are not an executable workflow engine. The harness and model must actually follow the stages and preserve the required evidence.

## Outputs and limits

The default deliverables are one consolidated report, an `audit.json` ledger, detailed stage evidence, and any calculation files needed to reproduce executed checks. Findings distinguish mathematical errors, proof gaps, unverified references, incomplete checks, exposition, and typos.

The helper detects inconsistent accounting, missing declared coverage, dependency cycles, and changes to the reviewed files. It does **not** establish mathematical truth. A clean report means no issue was found within the declared scope and available evidence; it is not a formal proof certificate.

See the [orchestrator](skills/math-paper-audit/SKILL.md), [shared contract](skills/math-paper-audit/references/audit-contract.md), and [report specification](skills/math-paper-audit/references/report-spec.md) for the complete procedure.

## Validation

Run the included bookkeeping regression tests from the repository root:

```sh
python -m unittest discover -s tests -q
```

The bundle includes 43 behavioral tests and records a small blind trial with seeded mathematical defects. See [validation notes](VALIDATION.txt) for what was checked and the limits of those results.

## License and provenance

Distributed under [Apache-2.0](LICENSE). Danus's copyright and attribution are retained in [NOTICE](NOTICE) and in each skill directory. This is a substantially modified adaptation, not an official Danus release. The [provenance map](skills/math-paper-audit/references/provenance.md) identifies the exact upstream snapshot and the design changes.
