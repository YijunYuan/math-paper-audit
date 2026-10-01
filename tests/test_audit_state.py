"""Behavioral regression checks for deterministic mathematical-audit bookkeeping."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = (Path(__file__).resolve().parent.parent / "skills" /
          "math-paper-audit" / "scripts" / "audit_state.py")
SPEC = importlib.util.spec_from_file_location("audit_state", str(SCRIPT))
audit_state = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_state)


def unit(identifier, kind="claim", requires_proof=True, is_main=True, depends_on=None):
    return {"id": identifier, "kind": kind, "location": "paper.tex:3 ({})".format(identifier),
            "statement": "For each real x, x*x is nonnegative.", "assumptions": ["x is real"],
            "depends_on": depends_on or [], "requires_proof": requires_proof, "is_main": is_main}


def finding(category="gap", severity="major"):
    return {"id": "F1", "stage": "proof", "category": category, "severity": severity,
            "location": "paper.tex:3 (T)", "target_ids": ["T"],
            "evidence": "The step from A to B has no supporting argument in the declared proof.",
            "reasoning": "A alone does not entail B: the missing hypothesis is needed for the inference.",
            "suggested_action": "Supply the missing inference and recheck its downstream uses.",
            "status": "open", "resolution_evidence": ""}


def complete_stages(audit):
    checker = audit_state.AuditChecker(audit)
    checker.units = {item["id"]: item for item in audit["units"]}
    for name in audit_state.STAGES:
        identifiers = sorted(checker.required_scope(name))
        audit["stages"][name] = {
            "status": "completed" if identifiers else "not_applicable",
            "scope_ids": identifiers, "reviewed_ids": identifiers[:],
            "evidence": ["stages/{}: checked the actual declared obligations.".format(name)] if identifiers else [],
            "reason": "The fully read manuscript has no applicable {} obligations.".format(name) if not identifiers else "",
        }


class AuditStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.paper = self.root / "paper"
        self.paper.mkdir()
        self.source = self.paper / "paper.tex"
        self.source.write_text("A paper with a stated proof.\n", encoding="utf-8")
        self.bib = self.paper / "references.bib"
        self.bib.write_text("A referenced source.\n", encoding="utf-8")
        self.audit_dir = self.root / "review"
        self.ledger = audit_state.initialize_audit(self.paper, self.audit_dir, ["paper.tex", "references.bib"])
        self.audit = audit_state.load_json(self.ledger)
        self.audit["scope"]["inventory_complete"] = True
        for item in self.audit["input_files"]:
            item["reviewed"] = True
        self.audit["units"] = [
            unit("D", "definition", False, False),
            unit("S", "section", False, False),
            unit("C", "citation", False, False),
            unit("T", depends_on=["D", "C"]),
            unit("K", "computation", False, False, ["T"]),
        ]
        complete_stages(self.audit)
        self.audit["independent_review"] = {
            "status": "completed", "method": "Fresh-context review using the same model family.",
            "evidence": "Independent reasoning checked T and its use in K; no unresolved disagreement.",
        }

    def tearDown(self):
        self.temp.cleanup()

    def result(self, expected, audit=None):
        result = audit_state.check_audit(self.audit if audit is None else audit)
        self.assertEqual(expected, result["verdict"], result)
        return result

    def write_ledger(self, audit=None):
        self.ledger.write_text(json.dumps(self.audit if audit is None else audit), encoding="utf-8")

    def cli(self, *args):
        run = subprocess.run([sys.executable, str(SCRIPT)] + list(args),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)
        self.assertEqual("", run.stderr, run.stderr)
        return run.returncode, json.loads(run.stdout)

    def test_valid_complete_review_is_clear_and_does_not_mutate(self):
        before = copy.deepcopy(self.audit)
        result = self.result("NO_ISSUES_FOUND")
        self.assertTrue(result["coverage_complete"])
        self.assertEqual([], result["errors"])
        self.assertEqual([], result["blockers"])
        self.assertEqual(self.audit, before)
        self.assertIn("does not", result["assessment_limit"])

    def test_open_errors_and_gaps_override_all_severity_labels(self):
        for category in ("error", "gap"):
            for severity in audit_state.SEVERITIES:
                with self.subTest(category=category, severity=severity):
                    self.audit["findings"] = [finding(category, severity)]
                    result = self.result("ISSUES_FOUND")
                    self.assertTrue(result["coverage_complete"])
                    self.assertEqual(1, result["open_finding_counts"][category])

    def test_known_gap_and_incomplete_coverage_remain_separate(self):
        self.audit["findings"] = [finding("gap", "minor")]
        self.audit["stages"]["whole"]["status"] = "pending"
        result = self.result("ISSUES_FOUND")
        self.assertFalse(result["coverage_complete"])

    def test_unverified_reference_and_incomplete_check_prevent_clear(self):
        for category in ("unverified_reference", "incomplete_check"):
            with self.subTest(category=category):
                self.audit["findings"] = [finding(category, "minor")]
                result = self.result("INCOMPLETE")
                self.assertEqual(1, result["open_finding_counts"][category])

    def test_only_exposition_and_typo_findings_are_notes(self):
        self.audit["findings"] = [finding("exposition"), finding("typo", "minor")]
        self.audit["findings"][1]["id"] = "F2"
        self.result("NOTES_ONLY")

    def test_resolved_and_dismissed_require_nonempty_evidence(self):
        for status in ("resolved", "dismissed"):
            with self.subTest(status=status):
                record = finding()
                record["status"] = status
                self.audit["findings"] = [record]
                self.result("INVALID_AUDIT")
                record["resolution_evidence"] = "  "
                self.result("INVALID_AUDIT")
                record["resolution_evidence"] = "The corrected inference at T was checked and its use in K rechecked."
                self.result("NO_ISSUES_FOUND")

    def test_unread_input_blocks_coverage(self):
        self.audit["input_files"][1]["reviewed"] = False
        result = self.result("INCOMPLETE")
        self.assertFalse(result["coverage_complete"])

    def test_inventory_and_independent_review_block_coverage(self):
        for field, value in (("inventory", False), ("independent", "pending"), ("independent", "unavailable")):
            with self.subTest(field=field, value=value):
                candidate = copy.deepcopy(self.audit)
                if field == "inventory":
                    candidate["scope"]["inventory_complete"] = value
                else:
                    candidate["independent_review"]["status"] = value
                result = self.result("INCOMPLETE", candidate)
                self.assertFalse(result["coverage_complete"])

    def test_completed_independent_review_needs_method_and_evidence(self):
        for field in ("method", "evidence"):
            candidate = copy.deepcopy(self.audit)
            candidate["independent_review"][field] = ""
            self.result("INVALID_AUDIT", candidate)

    def test_source_change_precedes_known_gap(self):
        self.audit["findings"] = [finding()]
        self.source.write_text("Changed manuscript\n", encoding="utf-8")
        result = self.result("STALE")
        self.assertEqual("hash_changed", result["stale_inputs"][0]["reason"])
        self.assertFalse(result["coverage_complete"])

    def test_missing_source_is_stale(self):
        self.bib.unlink()
        result = self.result("STALE")
        self.assertEqual("missing_or_unreadable", result["stale_inputs"][0]["reason"])
        self.assertFalse(result["coverage_complete"])

    def test_every_input_is_hashed_even_when_not_reviewed(self):
        self.audit["input_files"][1]["reviewed"] = False
        self.bib.write_text("Changed bibliography", encoding="utf-8")
        result = self.result("STALE")
        self.assertFalse(result["coverage_complete"])

    def test_unknown_dependency_is_invalid(self):
        self.audit["units"][3]["depends_on"].append("absent")
        self.result("INVALID_AUDIT")

    def test_real_cycle_is_an_issue_and_excludes_downstream_only_nodes(self):
        self.audit["units"][0]["depends_on"] = ["T"]
        result = self.result("ISSUES_FOUND")
        self.assertEqual([["D", "T"]], result["dependency_cycles"])
        self.assertTrue(result["coverage_complete"])
        self.assertEqual([], result["errors"])

    def test_self_dependency_is_a_cycle(self):
        self.audit["units"][3]["depends_on"] = ["T"]
        result = self.result("ISSUES_FOUND")
        self.assertEqual([["T"]], result["dependency_cycles"])

    def test_deep_graph_does_not_recurse(self):
        self.audit["units"] = [unit("T{}".format(index), depends_on=["T{}".format(index - 1)] if index else [])
                               for index in range(2500)]
        complete_stages(self.audit)
        self.result("NO_ISSUES_FOUND")
        self.audit["units"][0]["depends_on"] = ["T2499"]
        result = self.result("ISSUES_FOUND")
        self.assertEqual(2500, len(result["dependency_cycles"][0]))

    def test_duplicate_unit_finding_input_and_dependency_ids_are_invalid(self):
        mutations = (
            lambda a: a["units"].append(copy.deepcopy(a["units"][0])),
            lambda a: a["input_files"].append(copy.deepcopy(a["input_files"][0])),
            lambda a: a["units"][3]["depends_on"].append("D"),
            lambda a: a["stages"]["proof"]["scope_ids"].append("T"),
        )
        for change in mutations:
            candidate = copy.deepcopy(self.audit)
            change(candidate)
            self.result("INVALID_AUDIT", candidate)
        self.audit["findings"] = [finding(), finding()]
        self.result("INVALID_AUDIT")

    def test_canonical_input_path_alias_is_duplicate(self):
        alias = copy.deepcopy(self.audit["input_files"][0])
        alias["path"] = str(self.paper / ".." / "paper" / "paper.tex")
        self.audit["input_files"].append(alias)
        self.result("INVALID_AUDIT")

    def test_unknown_stage_and_finding_references_are_invalid(self):
        for field in ("scope_ids", "reviewed_ids"):
            candidate = copy.deepcopy(self.audit)
            candidate["stages"]["proof"][field].append("absent")
            self.result("INVALID_AUDIT", candidate)
        self.audit["findings"] = [finding()]
        self.audit["findings"][0]["target_ids"] = ["absent"]
        self.result("INVALID_AUDIT")

    def test_every_required_stage_scope_is_enforced(self):
        omitted = {"map": "S", "whole": "D", "proof": "T", "stress": "T",
                   "references": "C", "computation": "K"}
        for name, identifier in omitted.items():
            with self.subTest(stage=name):
                candidate = copy.deepcopy(self.audit)
                candidate["stages"][name]["scope_ids"].remove(identifier)
                candidate["stages"][name]["reviewed_ids"].remove(identifier)
                self.result("INVALID_AUDIT", candidate)

    def test_stress_includes_main_claim_even_when_no_proof_required(self):
        self.audit["units"].append(unit("Main", requires_proof=False, is_main=True))
        complete_stages(self.audit)
        self.result("NO_ISSUES_FOUND")
        self.audit["stages"]["stress"]["scope_ids"].remove("Main")
        self.audit["stages"]["stress"]["reviewed_ids"].remove("Main")
        self.result("INVALID_AUDIT")

    def test_extra_applicable_scope_must_be_reviewed_too(self):
        self.audit["stages"]["proof"]["scope_ids"].append("D")
        self.result("INVALID_AUDIT")
        self.audit["stages"]["proof"]["reviewed_ids"].append("D")
        self.result("NO_ISSUES_FOUND")

    def test_reviewed_ids_may_not_hide_outside_scope(self):
        self.audit["stages"]["proof"]["reviewed_ids"].append("D")
        self.result("INVALID_AUDIT")

    def test_completed_stage_needs_review_and_evidence(self):
        for field in ("reviewed_ids", "evidence"):
            candidate = copy.deepcopy(self.audit)
            candidate["stages"]["proof"][field] = []
            self.result("INVALID_AUDIT", candidate)

    def test_pending_and_blocked_stage_cannot_complete_audit(self):
        for status in ("pending", "blocked"):
            self.audit["stages"]["proof"]["status"] = status
            self.audit["stages"]["proof"]["reason"] = "This proof could not be fully examined."
            self.audit["stages"]["proof"]["reviewed_ids"] = []
            self.result("INCOMPLETE")
        self.audit["stages"]["proof"]["reason"] = ""
        self.result("INVALID_AUDIT")

    def test_no_named_theorems_still_has_prose_scope_and_valid_na(self):
        self.audit["units"] = [unit("S", "section", False, False)]
        complete_stages(self.audit)
        result = self.result("NO_ISSUES_FOUND")
        self.assertTrue(result["coverage_complete"])
        for name in ("references", "proof", "stress", "computation"):
            self.assertEqual("not_applicable", self.audit["stages"][name]["status"])

    def test_empty_completed_inventory_is_invalid_even_without_theorems(self):
        self.audit["units"] = []
        complete_stages(self.audit)
        self.result("INVALID_AUDIT")

    def test_not_applicable_cannot_bypass_required_work(self):
        for name in audit_state.STAGES:
            candidate = copy.deepcopy(self.audit)
            candidate["stages"][name] = {"status": "not_applicable", "scope_ids": [], "reviewed_ids": [],
                                          "evidence": [], "reason": "No time to review."}
            self.result("INVALID_AUDIT", candidate)

    def test_not_applicable_requires_empty_scope_and_reason(self):
        self.audit["units"] = [unit("S", "section", False, False)]
        complete_stages(self.audit)
        self.audit["stages"]["proof"]["reason"] = ""
        self.result("INVALID_AUDIT")
        self.audit["stages"]["proof"]["reason"] = "No proof obligations in the fully read prose."
        self.audit["stages"]["proof"]["scope_ids"] = ["S"]
        self.result("INVALID_AUDIT")

    def test_missing_or_extra_stage_is_invalid(self):
        del self.audit["stages"]["whole"]
        self.result("INVALID_AUDIT")
        complete_stages(self.audit)
        self.audit["stages"]["other"] = copy.deepcopy(self.audit["stages"]["whole"])
        self.result("INVALID_AUDIT")

    def test_restricted_scope_is_visible_in_clear_diagnostic(self):
        self.audit["scope"]["full_manuscript"] = False
        self.audit["scope"]["description"] = "Only Section 1 as requested."
        self.audit["scope"]["exclusions"] = ["Appendix excluded by the user."]
        result = self.result("NO_ISSUES_FOUND")
        self.assertEqual(self.audit["scope"], result["scope"])

    def test_hand_set_verdict_is_rejected(self):
        for field in ("verdict", "final_verdict", "coverage_complete"):
            candidate = copy.deepcopy(self.audit)
            candidate[field] = "NO_ISSUES_FOUND"
            self.result("INVALID_AUDIT", candidate)

    def test_boolean_and_type_confusion_is_invalid_without_crashing(self):
        mutations = (
            lambda a: a.update(schema_version=True),
            lambda a: a["input_files"][0].update(reviewed=1),
            lambda a: a["scope"].update(inventory_complete="true"),
            lambda a: a["units"][0].update(requires_proof=0),
            lambda a: a["units"][0].update(depends_on="T"),
            lambda a: a["stages"]["proof"].update(evidence="report.md"),
            lambda a: a.update(findings=None),
            lambda a: a["input_files"][0].update(sha256="bad"),
            lambda a: a["input_files"][0].update(path="relative.tex"),
            lambda a: a.update(units=[None]),
            lambda a: a.update(independent_review=[]),
        )
        for change in mutations:
            candidate = copy.deepcopy(self.audit)
            change(candidate)
            self.result("INVALID_AUDIT", candidate)

    def test_required_fields_cannot_be_omitted(self):
        for field in ("schema_version", "paper_root", "input_files", "scope", "units", "stages", "findings", "independent_review"):
            candidate = copy.deepcopy(self.audit)
            del candidate[field]
            self.result("INVALID_AUDIT", candidate)

    def test_initial_snapshot_is_incomplete_with_all_pending_stages(self):
        initial = audit_state.load_json(self.ledger)
        result = self.result("INCOMPLETE", initial)
        self.assertFalse(result["coverage_complete"])
        self.assertFalse(initial["scope"]["inventory_complete"])
        self.assertEqual(list(audit_state.STAGES), list(initial["stages"]))
        self.assertTrue(all(value["status"] == "pending" for value in initial["stages"].values()))
        self.assertEqual(str(self.source.resolve()), initial["input_files"][0]["path"])
        self.assertEqual(audit_state.sha256_file(self.source), initial["input_files"][0]["sha256"])

    def test_initializer_never_overwrites_a_ledger_or_sources(self):
        before = self.ledger.read_bytes()
        source_before = self.source.read_bytes()
        with self.assertRaises(ValueError):
            audit_state.initialize_audit(self.paper, self.audit_dir, ["paper.tex"])
        self.assertEqual(before, self.ledger.read_bytes())
        self.assertEqual(source_before, self.source.read_bytes())

    def test_initializer_requires_existing_explicit_unique_files(self):
        for files in ([], ["absent.tex"], ["paper.tex", str(self.source)], ["."]):
            with self.subTest(files=files):
                new_dir = self.root / "unused"
                with self.assertRaises(ValueError):
                    audit_state.initialize_audit(self.paper, new_dir, files)
                self.assertFalse((new_dir / "audit.json").exists())

    def test_cli_clear_notes_issues_and_incomplete_exit_codes(self):
        for category, expected, code in ((None, "NO_ISSUES_FOUND", 0), ("typo", "NOTES_ONLY", 0),
                                         ("gap", "ISSUES_FOUND", 1), ("unverified_reference", "INCOMPLETE", 1)):
            self.audit["findings"] = [] if category is None else [finding(category)]
            self.write_ledger()
            actual_code, output = self.cli("check", str(self.ledger))
            self.assertEqual(code, actual_code)
            self.assertEqual(expected, output["verdict"])

    def test_cli_malformed_json_and_duplicate_keys_have_machine_readable_errors(self):
        for text in ("{", "[]", "null", '{"schema_version": 1, "schema_version": 1}', '{"bad": NaN}'):
            self.ledger.write_text(text, encoding="utf-8")
            code, output = self.cli("check", str(self.ledger))
            self.assertEqual(2, code)
            self.assertEqual("INVALID_AUDIT", output["verdict"])
            self.assertTrue(output["errors"])

    def test_cli_missing_input_json_has_error_exit(self):
        code, output = self.cli("check", str(self.root / "absent.json"))
        self.assertEqual(2, code)
        self.assertEqual("INVALID_AUDIT", output["verdict"])

    def test_cli_output_is_created_but_never_overwrites_ledger_or_manuscript(self):
        self.write_ledger()
        target = self.audit_dir / "diagnostic.json"
        code, output = self.cli("check", str(self.ledger), "--output", str(target))
        self.assertEqual(0, code)
        self.assertEqual(output, audit_state.load_json(target))
        for protected in (self.ledger, self.source, target):
            before = protected.read_bytes()
            code, output = self.cli("check", str(self.ledger), "--output", str(protected))
            self.assertEqual(2, code)
            self.assertEqual("INVALID_AUDIT", output["verdict"])
            self.assertEqual(before, protected.read_bytes())

    def test_cli_ascii_console_preserves_unicode_in_saved_diagnostic(self):
        description = "Expectation \U0001d53c is defined in this scope."
        self.audit["scope"]["description"] = description
        self.write_ledger()
        target = self.audit_dir / "unicode-diagnostic.json"
        environment = dict(os.environ, PYTHONIOENCODING="ascii")
        run = subprocess.run([sys.executable, str(SCRIPT), "check", str(self.ledger),
                              "--output", str(target)], env=environment,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(0, run.returncode, run.stderr)
        self.assertEqual(b"", run.stderr)
        output = json.loads(run.stdout.decode("ascii"))
        self.assertEqual(description, output["scope"]["description"])
        self.assertIn(description, target.read_text(encoding="utf-8"))
        self.assertEqual(output, audit_state.load_json(target))

    def test_cli_initializer_reports_error_on_existing_snapshot(self):
        code, output = self.cli("init", "--paper-root", str(self.paper), "--audit-dir", str(self.audit_dir),
                                "--files", "paper.tex")
        self.assertEqual(2, code)
        self.assertIn("overwrite", output["errors"][0])


if __name__ == "__main__":
    unittest.main()
