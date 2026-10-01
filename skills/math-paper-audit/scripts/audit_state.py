#!/usr/bin/env python3
"""Deterministic bookkeeping for a fixed-snapshot mathematical paper review.

Python 3.7+; standard library only. This checks records, not mathematics. It
cannot discover omitted claims, verify reasoning, or establish that resolution
evidence really contains an incorporated fix and downstream recheck.

Exit codes: 0 = NO_ISSUES_FOUND / NOTES_ONLY (or successful initialization);
1 = ISSUES_FOUND / INCOMPLETE / STALE; 2 = INVALID_AUDIT / input or output error.
``check`` always derives its verdict. No command approves findings or edits an
existing audit. ``--output`` writes a new diagnostic file and never overwrites.
Coverage means completion of the declared inventory, input reading, six stages,
and independent review. Finding categories and freshness additionally govern the
verdict. A completed restricted scope remains explicitly visible in diagnostics.
"""

import argparse
from collections import deque
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys


STAGES = ("map", "references", "proof", "stress", "computation", "whole")
KINDS = ("claim", "definition", "section", "citation", "computation")
CATEGORIES = ("error", "gap", "unverified_reference", "incomplete_check", "exposition", "typo")
SEVERITIES = ("critical", "major", "minor")
ASSESSMENT_LIMIT = (
    "Bookkeeping check of the declared snapshot and scope only; this does not "
    "validate mathematical reasoning or certify mathematical correctness."
)


def canonical_path(value):
    # Path.resolve also expands Windows 8.3 aliases on Python 3.7, where
    # os.path.realpath alone leaves them unchanged.
    return os.path.normcase(str(Path(value).resolve()))


def sha256_file(path):
    digest = hashlib.sha256()
    with open(str(path), "rb") as source:
        while True:
            block = source.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object key: {!r}".format(key))
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("Non-finite JSON number: {}".format(value))


def load_json(path):
    with open(str(path), "r", encoding="utf-8-sig") as source:
        return json.load(source, object_pairs_hook=reject_duplicate_keys,
                         parse_constant=reject_constant)


def error_diagnostic(message):
    return {
        "verdict": "INVALID_AUDIT", "coverage_complete": False,
        "blockers": ["The audit record could not be checked."],
        "open_finding_counts": {category: 0 for category in CATEGORIES},
        "errors": [message], "stale_inputs": [], "dependency_cycles": [], "scope": None,
        "assessment_limit": ASSESSMENT_LIMIT,
    }


class AuditChecker:
    def __init__(self, audit):
        self.audit = audit
        self.errors = []
        self.coverage_blockers = []
        self.stale_inputs = []
        self.cycles = []
        self.units = {}
        self.counts = {category: 0 for category in CATEGORIES}

    def error(self, where, message):
        self.errors.append("{}: {}".format(where, message))

    def object(self, value, where, fields):
        if not isinstance(value, dict):
            self.error(where, "must be an object")
            return False
        for field in fields:
            if field not in value:
                self.error(where, "missing required field {!r}".format(field))
        return True

    def string(self, value, where, nonempty=False):
        if not isinstance(value, str) or (nonempty and not value.strip()):
            self.error(where, "must be {}string".format("a nonempty " if nonempty else "a "))
            return False
        return True

    def boolean(self, value, where):
        if type(value) is not bool:
            self.error(where, "must be a boolean")
            return False
        return True

    def choice(self, value, where, choices):
        if not isinstance(value, str) or value not in choices:
            self.error(where, "must be one of {}".format(", ".join(choices)))
            return False
        return True

    def string_list(self, value, where, unique=False, nonempty=False):
        if not isinstance(value, list):
            self.error(where, "must be a list")
            return []
        if nonempty and not value:
            self.error(where, "must not be empty")
        valid = []
        seen = set()
        for index, item in enumerate(value):
            if self.string(item, "{}[{}]".format(where, index), nonempty=True):
                if unique and item in seen:
                    self.error(where, "duplicate value {!r}".format(item))
                seen.add(item)
                valid.append(item)
        return valid

    def known_ids(self, value, where, nonempty=False):
        identifiers = self.string_list(value, where, unique=True, nonempty=nonempty)
        for identifier in identifiers:
            if identifier not in self.units:
                self.error(where, "unknown unit ID {!r}".format(identifier))
        return set(identifiers)

    def check_inputs(self):
        inputs = self.audit.get("input_files")
        if not isinstance(inputs, list) or not inputs:
            self.error("input_files", "must be a nonempty list")
            self.coverage_blockers.append("The declared input snapshot is empty or invalid.")
            return
        seen = set()
        for index, item in enumerate(inputs):
            where = "input_files[{}]".format(index)
            if not self.object(item, where, ("path", "sha256", "reviewed")):
                continue
            path = item.get("path")
            path_valid = self.string(path, where + ".path", nonempty=True)
            if path_valid and not os.path.isabs(path):
                self.error(where + ".path", "must be an absolute path")
                path_valid = False
            expected = item.get("sha256")
            hash_valid = (isinstance(expected, str) and
                          re.fullmatch(r"[0-9a-fA-F]{64}", expected) is not None)
            if not hash_valid:
                self.error(where + ".sha256", "must contain exactly 64 hexadecimal digits")
            self.boolean(item.get("reviewed"), where + ".reviewed")
            if item.get("reviewed") is not True:
                self.coverage_blockers.append("Input has not been fully reviewed: {}".format(path))
            if not path_valid:
                continue
            try:
                canonical = canonical_path(path)
                if canonical in seen:
                    self.error(where + ".path", "duplicate input path")
                seen.add(canonical)
                actual = sha256_file(path)
            except (OSError, ValueError) as exc:
                self.stale_inputs.append({"path": path, "reason": "missing_or_unreadable",
                                          "detail": str(exc)})
                continue
            if hash_valid and actual.lower() != expected.lower():
                self.stale_inputs.append({"path": path, "reason": "hash_changed",
                                          "expected_sha256": expected.lower(),
                                          "actual_sha256": actual})

    def check_scope(self):
        scope = self.audit.get("scope")
        if not self.object(scope, "scope", ("description", "full_manuscript", "inventory_complete", "exclusions")):
            return
        self.string(scope.get("description"), "scope.description")
        self.boolean(scope.get("full_manuscript"), "scope.full_manuscript")
        self.boolean(scope.get("inventory_complete"), "scope.inventory_complete")
        self.string_list(scope.get("exclusions"), "scope.exclusions", unique=True)
        if scope.get("inventory_complete") is not True:
            self.coverage_blockers.append("The manuscript inventory is unfinished.")

    def check_units(self):
        units = self.audit.get("units")
        if not isinstance(units, list):
            self.error("units", "must be a list")
            return
        # An empty initial inventory is a legitimate unfinished ledger, never a
        # completed audit. This allows init -> check to report INCOMPLETE.
        if not units:
            self.coverage_blockers.append("No review units have been inventoried (including prose claims).")
            scope = self.audit.get("scope")
            if isinstance(scope, dict) and scope.get("inventory_complete") is True:
                self.error("units", "a completed inventory must contain at least one unit")
        required = ("id", "kind", "location", "statement", "assumptions", "depends_on", "requires_proof", "is_main")
        for index, unit in enumerate(units):
            where = "units[{}]".format(index)
            if not self.object(unit, where, required):
                continue
            identifier = unit.get("id")
            if self.string(identifier, where + ".id", nonempty=True):
                if identifier in self.units:
                    self.error(where + ".id", "duplicate unit ID {!r}".format(identifier))
                else:
                    self.units[identifier] = unit
            self.choice(unit.get("kind"), where + ".kind", KINDS)
            self.string(unit.get("location"), where + ".location", nonempty=True)
            self.string(unit.get("statement"), where + ".statement", nonempty=True)
            self.string_list(unit.get("assumptions"), where + ".assumptions")
            self.boolean(unit.get("requires_proof"), where + ".requires_proof")
            self.boolean(unit.get("is_main"), where + ".is_main")
        # All IDs are known before resolving dependencies. Iterative Kosaraju
        # traversal finds the actual cycle members (not downstream users) and
        # handles deep declared graphs without recursive DFS.
        dependents = {identifier: [] for identifier in self.units}
        graph = {}
        for identifier, unit in self.units.items():
            dependencies = self.known_ids(unit.get("depends_on"),
                                          "unit {!r}.depends_on".format(identifier))
            graph[identifier] = []
            for dependency in sorted(dependencies):
                if dependency in self.units:
                    graph[identifier].append(dependency)
                    dependents[dependency].append(identifier)
        visited = set()
        finish_order = []
        for start in graph:
            if start in visited:
                continue
            stack = [(start, False)]
            while stack:
                identifier, finished = stack.pop()
                if finished:
                    finish_order.append(identifier)
                    continue
                if identifier in visited:
                    continue
                visited.add(identifier)
                stack.append((identifier, True))
                for dependency in reversed(graph[identifier]):
                    if dependency not in visited:
                        stack.append((dependency, False))
        assigned = set()
        for start in reversed(finish_order):
            if start in assigned:
                continue
            component = []
            assigned.add(start)
            ready = deque([start])
            while ready:
                identifier = ready.popleft()
                component.append(identifier)
                for dependent in dependents[identifier]:
                    if dependent not in assigned:
                        assigned.add(dependent)
                        ready.append(dependent)
            if len(component) > 1 or start in graph[start]:
                self.cycles.append(sorted(component))
        self.cycles.sort()

    def required_scope(self, stage):
        if stage in ("map", "whole"):
            return set(self.units)
        if stage == "proof":
            return {key for key, unit in self.units.items() if unit.get("requires_proof") is True}
        if stage == "stress":
            return {key for key, unit in self.units.items()
                    if unit.get("kind") == "claim" and
                    (unit.get("requires_proof") is True or unit.get("is_main") is True)}
        kind = "citation" if stage == "references" else "computation"
        return {key for key, unit in self.units.items() if unit.get("kind") == kind}

    def check_stages(self):
        stages = self.audit.get("stages")
        if not self.object(stages, "stages", STAGES):
            return
        for key in sorted(set(stages) - set(STAGES)):
            self.error("stages", "unknown stage {!r}".format(key))
        for name in STAGES:
            if name not in stages:
                continue
            where = "stages." + name
            stage = stages[name]
            if not self.object(stage, where, ("status", "scope_ids", "reviewed_ids", "evidence", "reason")):
                continue
            status = stage.get("status")
            self.choice(status, where + ".status", ("pending", "completed", "not_applicable", "blocked"))
            scope = self.known_ids(stage.get("scope_ids"), where + ".scope_ids")
            reviewed = self.known_ids(stage.get("reviewed_ids"), where + ".reviewed_ids")
            evidence = self.string_list(stage.get("evidence"), where + ".evidence")
            reason_valid = self.string(stage.get("reason"), where + ".reason")
            if reviewed - scope:
                self.error(where, "reviewed IDs are outside the declared scope: {}".format(", ".join(sorted(reviewed - scope))))
            required = self.required_scope(name)
            missing_scope = required - scope
            if missing_scope:
                self.error(where + ".scope_ids", "omits required units: {}".format(", ".join(sorted(missing_scope))))
            if status == "completed":
                if not scope:
                    self.error(where, "completed stage requires nonempty scope")
                if scope - reviewed:
                    self.error(where, "completed stage has unreviewed units: {}".format(", ".join(sorted(scope - reviewed))))
                if not evidence:
                    self.error(where + ".evidence", "completed stage requires substantive evidence")
            elif status == "not_applicable":
                if name in ("map", "whole") or required or scope or reviewed:
                    self.error(where, "not_applicable is invalid for required work or nonempty scope/review IDs")
                if not reason_valid or not stage.get("reason", "").strip():
                    self.error(where + ".reason", "not_applicable requires a concrete reason")
            else:
                self.coverage_blockers.append("Stage {} is {}.".format(name, status))
                if status == "blocked" and (not reason_valid or not stage.get("reason", "").strip()):
                    self.error(where + ".reason", "blocked stage requires a reason")

    def check_findings(self):
        findings = self.audit.get("findings")
        if not isinstance(findings, list):
            self.error("findings", "must be a list")
            return
        seen = set()
        required = ("id", "stage", "category", "severity", "location", "target_ids", "evidence", "reasoning", "suggested_action", "status", "resolution_evidence")
        for index, finding in enumerate(findings):
            where = "findings[{}]".format(index)
            if not self.object(finding, where, required):
                continue
            identifier = finding.get("id")
            if self.string(identifier, where + ".id", nonempty=True):
                if identifier in seen:
                    self.error(where + ".id", "duplicate finding ID {!r}".format(identifier))
                seen.add(identifier)
            self.choice(finding.get("stage"), where + ".stage", STAGES)
            category_valid = self.choice(finding.get("category"), where + ".category", CATEGORIES)
            self.choice(finding.get("severity"), where + ".severity", SEVERITIES)
            self.known_ids(finding.get("target_ids"), where + ".target_ids", nonempty=True)
            for field in ("location", "evidence", "reasoning", "suggested_action"):
                self.string(finding.get(field), where + "." + field, nonempty=True)
            status = finding.get("status")
            self.choice(status, where + ".status", ("open", "resolved", "dismissed"))
            self.string(finding.get("resolution_evidence"), where + ".resolution_evidence",
                        nonempty=status in ("resolved", "dismissed"))
            if status == "open" and category_valid:
                self.counts[finding["category"]] += 1

    def check_independent_review(self):
        review = self.audit.get("independent_review")
        if not self.object(review, "independent_review", ("status", "method", "evidence")):
            return
        status = review.get("status")
        self.choice(status, "independent_review.status", ("completed", "unavailable", "pending"))
        self.string(review.get("method"), "independent_review.method", nonempty=status == "completed")
        self.string(review.get("evidence"), "independent_review.evidence", nonempty=status == "completed")
        if status != "completed":
            self.coverage_blockers.append("Independent review is {}.".format(status))

    def run(self):
        required = ("schema_version", "paper_root", "input_files", "scope", "units", "stages", "findings", "independent_review")
        if not self.object(self.audit, "audit", required):
            return error_diagnostic(self.errors[0])
        version = self.audit.get("schema_version")
        if type(version) is not int or version != 1:
            self.error("schema_version", "must be integer 1")
        root = self.audit.get("paper_root")
        if self.string(root, "paper_root", nonempty=True) and not os.path.isabs(root):
            self.error("paper_root", "must be an absolute path")
        for field in ("verdict", "final_verdict", "coverage_complete"):
            if field in self.audit:
                self.error(field, "is derived by check and must not be hand-set in audit.json")
        self.check_inputs()
        self.check_scope()
        self.check_units()
        self.check_stages()
        self.check_findings()
        self.check_independent_review()
        coverage_complete = not self.errors and not self.coverage_blockers and not self.stale_inputs
        blockers = list(self.coverage_blockers)
        if self.errors:
            blockers.insert(0, "The audit record contains invalid or contradictory accounting.")
        if self.stale_inputs:
            blockers.append("One or more declared input files changed, disappeared, or became unreadable.")
        if self.counts["error"] or self.counts["gap"]:
            blockers.append("Open mathematical error or gap findings remain, regardless of severity.")
        if self.cycles:
            blockers.append("The declared proof-dependency graph contains a circular dependency.")
        if self.counts["unverified_reference"] or self.counts["incomplete_check"]:
            blockers.append("Open unverified-reference or incomplete-check findings remain.")
        if self.errors:
            verdict = "INVALID_AUDIT"
        elif self.stale_inputs:
            verdict = "STALE"
        elif self.counts["error"] or self.counts["gap"] or self.cycles:
            verdict = "ISSUES_FOUND"
        elif not coverage_complete or self.counts["unverified_reference"] or self.counts["incomplete_check"]:
            verdict = "INCOMPLETE"
        elif self.counts["exposition"] or self.counts["typo"]:
            verdict = "NOTES_ONLY"
        else:
            verdict = "NO_ISSUES_FOUND"
        return {"verdict": verdict, "coverage_complete": coverage_complete,
                "blockers": blockers, "open_finding_counts": self.counts,
                "errors": self.errors, "stale_inputs": self.stale_inputs,
                "dependency_cycles": self.cycles,
                "scope": self.audit.get("scope"), "assessment_limit": ASSESSMENT_LIMIT}


def check_audit(audit):
    """Derive accounting diagnostics from a decoded audit without modifying it."""
    return AuditChecker(audit).run()


def initialize_audit(paper_root, audit_dir, files):
    root = Path(paper_root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("paper_root must be an existing directory: {}".format(root))
    target = Path(audit_dir).expanduser().resolve() / "audit.json"
    if target.exists():
        raise ValueError("Refusing to overwrite existing audit: {}".format(target))
    if not files:
        raise ValueError("Supply the full explicitly discovered input-file set with --files")
    inputs = []
    seen = set()
    for filename in files:
        path = Path(filename).expanduser()
        if not path.is_absolute():
            path = root / path
        path = path.resolve()
        if not path.is_file():
            raise ValueError("Input must be an existing readable file: {}".format(path))
        canonical = canonical_path(path)
        if canonical in seen:
            raise ValueError("Duplicate input path: {}".format(path))
        if canonical == canonical_path(target):
            raise ValueError("audit.json cannot be a manuscript input")
        seen.add(canonical)
        inputs.append({"path": str(path), "sha256": sha256_file(path), "reviewed": False})
    audit = {
        "schema_version": 1, "paper_root": str(root),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_files": inputs,
        "scope": {"description": "Full declared input snapshot; inventory pending.",
                  "full_manuscript": True, "inventory_complete": False, "exclusions": []},
        "units": [],
        "stages": {name: {"status": "pending", "scope_ids": [], "reviewed_ids": [],
                          "evidence": [], "reason": ""} for name in STAGES},
        "findings": [],
        "independent_review": {"status": "pending", "method": "", "evidence": ""},
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation closes the race with another initializer.
    with open(str(target), "x", encoding="utf-8", newline="\n") as destination:
        json.dump(audit, destination, ensure_ascii=False, indent=2, allow_nan=False)
        destination.write("\n")
    return target


def exit_status(diagnostic):
    if diagnostic["verdict"] == "INVALID_AUDIT":
        return 2
    if diagnostic["verdict"] in ("NO_ISSUES_FOUND", "NOTES_ONLY"):
        return 0
    return 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init", help="Create an unfinished snapshot ledger without changing sources")
    init_parser.add_argument("--paper-root", required=True)
    init_parser.add_argument("--audit-dir", required=True)
    init_parser.add_argument("--files", nargs="+", required=True,
                             help="Explicit discovered input set; relative paths resolve against paper-root")
    check_parser = subparsers.add_parser("check", help="Derive the verdict from a ledger and current input hashes")
    check_parser.add_argument("audit_json")
    check_parser.add_argument("--output", help="Also save diagnostics to a new file; never overwrite")
    args = parser.parse_args(argv)
    if args.command == "init":
        try:
            target = initialize_audit(args.paper_root, args.audit_dir, args.files)
            print(json.dumps({"audit_json": str(target), "status": "initialized",
                              "assessment_limit": ASSESSMENT_LIMIT}, ensure_ascii=True, indent=2))
            return 0
        except (OSError, ValueError) as exc:
            print(json.dumps(error_diagnostic(str(exc)), ensure_ascii=True, indent=2))
            return 2
    try:
        diagnostic = check_audit(load_json(args.audit_json))
    except (OSError, ValueError, RecursionError) as exc:
        diagnostic = error_diagnostic("Cannot read audit JSON: {}".format(exc))
    rendered = json.dumps(diagnostic, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if args.output:
        try:
            output_path = Path(args.output).expanduser()
            if canonical_path(output_path) == canonical_path(args.audit_json):
                raise ValueError("Diagnostic output must not replace the audit record")
            with open(str(output_path), "x", encoding="utf-8", newline="\n") as destination:
                destination.write(rendered)
        except (OSError, ValueError) as exc:
            failure = error_diagnostic("Cannot save diagnostic output: {}".format(exc))
            print(json.dumps(failure, ensure_ascii=True, indent=2))
            return 2
    # Escape console JSON for Windows legacy encodings and redirected ASCII
    # streams; the optional saved diagnostic remains readable UTF-8.
    print(json.dumps(diagnostic, ensure_ascii=True, indent=2, allow_nan=False))
    return exit_status(diagnostic)


if __name__ == "__main__":
    sys.exit(main())
