#!/usr/bin/env python3
"""Validate the canonical draft PIP and governance ledger deterministically."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
LEDGER_JSON = ROOT / "knowledge/governance/PIP-Registry.json"
LEDGER_MD = ROOT / "knowledge/governance/PIP-Registry.md"
GENERATOR = HERE / "build_ledger.py"
SEMANTIC_PATH = ROOT / "archive/semantic/governance/pip-registry-semantic.json"
TREASURY_STATES_BY_FIELD = {
    "request_state": {"REQUESTED", None},
    "authorization_state": {"AUTHORIZED", None},
    "payment_state": {"COUNCIL_REPORTED", "UNVERIFIED", None},
    "onchain_verification_state": {"MISSING_ONCHAIN_EVIDENCE", "UNVERIFIED", None},
}
EXPECTED_ELECTION_PIPS = {6, 7, 11, 25, 27}
EXPECTED_FAILED_PIPS = {13, 15, 19, 26}
SOLANA_SENTINEL_WALLET = "11111111111111111111111111111111"
GENERATED = [
    LEDGER_JSON,
    LEDGER_MD,
    HERE / "conflict-report.json",
    HERE / "conflict-report.md",
    HERE / "governance-research-backlog.json",
    HERE / "governance-research-backlog.md",
    HERE / "campaign-summary.json",
    HERE / "campaign-summary.md",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_digest(path: Path) -> str:
    """Hash text artifacts with canonical LF endings for cross-platform stability."""
    data = path.read_bytes()
    if path.suffix.lower() in {".json", ".md", ".py"}:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def manifest_size(path: Path) -> int:
    data = path.read_bytes()
    if path.suffix.lower() in {".json", ".md", ".py"}:
        data = data.replace(b"\r\n", b"\n")
    return len(data)


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, encoding="utf-8", errors="replace")


def iso(value: str | None) -> bool:
    if not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def changed_paths() -> list[str]:
    paths: set[str] = set()
    branch = run(["git", "diff", "--name-only", "origin/main...HEAD"])
    if branch.returncode == 0:
        paths.update(line.strip().replace("\\", "/") for line in branch.stdout.splitlines() if line.strip())
    status = run(["git", "status", "--porcelain"])
    for line in status.stdout.splitlines():
        if len(line) >= 4:
            path = line[3:].strip().strip('"').replace("\\", "/")
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            paths.add(path)
    return sorted(paths)


def internal_links(path: Path) -> list[str]:
    failures: list[str] = []
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#")):
            continue
        clean = target.split("#", 1)[0]
        if clean and not (path.parent / clean).resolve().exists():
            failures.append(target)
    return failures


def schema_errors(value: Any, schema: dict[str, Any], root: dict[str, Any], path: str = "$") -> list[str]:
    """Evaluate the Draft 2020-12 keywords used by the checked-in schema.

    This campaign-local evaluator keeps validation deterministic without adding a
    runtime dependency. Unsupported schema keywords fail closed.
    """
    errors: list[str] = []
    supported = {
        "$schema", "$id", "$ref", "$defs", "title", "type", "additionalProperties",
        "required", "properties", "const", "enum", "minimum", "maximum", "minLength",
        "pattern", "format", "minItems", "maxItems", "uniqueItems", "items", "oneOf",
    }
    ignored_annotations = {"title"}
    unknown = set(schema) - supported - ignored_annotations
    if unknown:
        return [f"{path}: unsupported schema keywords {sorted(unknown)}"]
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            return [f"{path}: unsupported external ref {ref}"]
        target: Any = root
        for part in ref[2:].split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
        return schema_errors(value, target, root, path)
    if "oneOf" in schema:
        alternatives = [schema_errors(value, option, root, path) for option in schema["oneOf"]]
        passing = [item for item in alternatives if not item]
        if len(passing) != 1:
            errors.append(f"{path}: expected exactly one schema alternative; matched {len(passing)}")
        return errors
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} is outside enum")
    expected = schema.get("type")
    allowed = expected if isinstance(expected, list) else ([expected] if expected else [])
    type_ok = not allowed
    for item_type in allowed:
        if item_type == "null" and value is None:
            type_ok = True
        elif item_type == "object" and isinstance(value, dict):
            type_ok = True
        elif item_type == "array" and isinstance(value, list):
            type_ok = True
        elif item_type == "string" and isinstance(value, str):
            type_ok = True
        elif item_type == "integer" and isinstance(value, int) and not isinstance(value, bool):
            type_ok = True
        elif item_type == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
            type_ok = True
        elif item_type == "boolean" and isinstance(value, bool):
            type_ok = True
    if not type_ok:
        return errors + [f"{path}: expected type {allowed}, got {type(value).__name__}"]
    if isinstance(value, dict):
        missing = set(schema.get("required", [])) - set(value)
        errors.extend(f"{path}: missing required property {name}" for name in sorted(missing))
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            errors.extend(f"{path}: unexpected property {name}" for name in sorted(set(value) - set(properties)))
        for name, child_schema in properties.items():
            if name in value:
                errors.extend(schema_errors(value[name], child_schema, root, f"{path}.{name}"))
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: fewer than minItems")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: more than maxItems")
        if schema.get("uniqueItems"):
            frozen = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(frozen) != len(set(frozen)):
                errors.append(f"{path}: items are not unique")
        if "items" in schema:
            for index, item in enumerate(value):
                errors.extend(schema_errors(item, schema["items"], root, f"{path}[{index}]"))
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: shorter than minLength")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            errors.append(f"{path}: does not match pattern")
        if schema.get("format") == "date" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            errors.append(f"{path}: invalid date format")
        if schema.get("format") == "date-time" and not iso(value):
            errors.append(f"{path}: invalid date-time format")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: above maximum")
    return errors


def main() -> int:
    failures: list[str] = []
    warnings = [
        "Validation confirms structural and evidence reconciliation only; it does not establish implementation, payment, or on-chain execution.",
        "The ledger remains QUALIFIED and DRAFT_FOR_REVIEW pending human governance review.",
    ]
    checks: dict[str, Any] = {}

    def require(condition: bool, name: str, failure: str, detail: Any = None) -> None:
        checks[name] = {"passed": bool(condition), "detail": detail}
        if not condition:
            failures.append(failure)

    # All output JSON must parse before deeper validation.
    json_paths = [LEDGER_JSON, HERE / "conflict-report.json", HERE / "governance-research-backlog.json", HERE / "campaign-summary.json", HERE / "canonical-pip-governance-ledger.schema.json"]
    parsed = {}
    for path in json_paths:
        try:
            parsed[path.name] = read_json(path)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            failures.append(f"JSON parse failed for {path.relative_to(ROOT)}: {exc}")
    require(len(parsed) == len(json_paths), "json_parse", "not all ledger JSON artifacts parse", len(parsed))
    if failures:
        report = {"campaign_id": "canonical-pip-governance-ledger-2026-07", "status": "FAIL", "checks": checks, "warnings": warnings, "failures": failures}
        write_json(HERE / "validation-report.json", report)
        return 1

    ledger = parsed[LEDGER_JSON.name]
    schema = parsed["canonical-pip-governance-ledger.schema.json"]
    records = ledger["records"]
    conflicts = parsed["conflict-report.json"]["conflicts"]
    backlog = parsed["governance-research-backlog.json"]["items"]
    by_number = {item["pip_number"]: item for item in records}
    source_proposals = read_json(SEMANTIC_PATH)["proposals"]
    source_by_number = {item["pip_number"]: item for item in source_proposals}
    actual_election_pips = {item["pip_number"] for item in records if item["vote"]["mechanism"] == "RANKED_CHOICE_ELECTION"}
    actual_failed_pips = {item["pip_number"] for item in records if item["result"]["reviewed_result"] == "FAILED"}
    actual_passed_non_election_pips = {
        item["pip_number"]
        for item in records
        if item["vote"]["mechanism"] != "RANKED_CHOICE_ELECTION" and item["result"]["reviewed_result"] == "PASSED"
    }
    source_election_pips = {item["pip_number"] for item in source_proposals if item["vote_mechanism"] == "RANKED_CHOICE_ELECTION"}
    source_failed_pips = {item["pip_number"] for item in source_proposals if item["reviewed_result"] == "FAILED"}
    source_passed_non_election_pips = {
        item["pip_number"]
        for item in source_proposals
        if item["vote_mechanism"] != "RANKED_CHOICE_ELECTION" and item["reviewed_result"] == "PASSED"
    }

    required_record_fields = {"pip_id", "pip_number", "source_id", "proposal_uuid", "title", "reviewed_title", "author", "category", "dates", "sources", "vote", "result", "relationships", "authorization", "implementation", "funding_scope", "treasury_states", "financial_terms", "reconciliation", "conflict_ids", "research_backlog_ids", "known_limitations", "review_status"}
    schema_top_required = set(schema.get("required", []))
    schema_record_required = set(schema.get("properties", {}).get("records", {}).get("items", {}).get("required", []))
    record_ref = schema.get("properties", {}).get("records", {}).get("items", {}).get("$ref")
    record_schema = schema.get("$defs", {}).get("pipRecord", {}) if record_ref == "#/$defs/pipRecord" else schema.get("properties", {}).get("records", {}).get("items", {})
    schema_record_required = set(record_schema.get("required", []))
    require(schema_top_required <= set(ledger) and schema_record_required == required_record_fields and schema.get("properties", {}).get("records", {}).get("minItems") == 33 and schema.get("properties", {}).get("records", {}).get("maxItems") == 33, "schema_contract", "ledger does not reconcile to the checked-in schema contract")
    actual_schema_errors = schema_errors(ledger, schema, schema)
    require(not actual_schema_errors, "json_schema_validation", "ledger fails the checked-in Draft 2020-12 schema", actual_schema_errors[:50])
    require(len(records) == 33 and [item["pip_number"] for item in records] == list(range(1, 34)), "pip_sequence", "ledger is not exactly PIP-1 through PIP-33", len(records))
    require(all(required_record_fields <= set(item) for item in records), "required_fields", "a PIP record lacks required fields")
    require(len({item["pip_id"] for item in records}) == len({item["source_id"] for item in records}) == len({item["proposal_uuid"] for item in records}) == 33, "unique_identifiers", "PIP, Source, or proposal identifiers are not unique")
    require(ledger["ledger_status"] == "DRAFT_FOR_REVIEW" and ledger["review_status"] == "HUMAN_REVIEW_REQUIRED" and ledger["knowledge_status"] == "QUALIFIED", "draft_status", "ledger was promoted beyond draft review status")
    require(ledger["interpretation_policy"]["completed_binary_rule_authority"] == "REPOSITORY_OWNER_APPROVED_EDITORIAL_ADJUDICATION" and not ledger["interpretation_policy"]["completed_binary_rule_is_source_native_pip_1_text"], "binary_rule_attribution", "completed-binary rule is not durably labeled as editorial adjudication")
    require(not ledger["interpretation_policy"]["onchain_verification_performed"], "no_onchain_verification", "ledger asserts on-chain verification")

    source_failures: list[str] = []
    checksum_failures: list[str] = []
    for item in records:
        for key in ("full_text_source_path", "source_record_path", "semantic_record_path", "reconciliation_path"):
            if not (ROOT / item["sources"][key]).exists():
                source_failures.append(f"{item['pip_id']}:{key}")
        raw_path = ROOT / item["sources"]["full_text_source_path"]
        source_path = ROOT / item["sources"]["source_record_path"]
        if raw_path.exists() and source_path.exists():
            raw = read_json(raw_path)
            source = read_json(source_path)
            if raw.get("pipNumber") != item["pip_number"] or digest(raw_path) != source.get("content_sha256") or digest(raw_path) != item["sources"]["raw_content_sha256"]:
                checksum_failures.append(item["pip_id"])
    require(not source_failures, "source_paths", "a ledger source path does not resolve", source_failures)
    require(not checksum_failures, "raw_source_checksums", "raw capture checksum does not reconcile to the Source Record", checksum_failures)

    date_failures = []
    for item in records:
        dates = item["dates"]
        if not all(iso(dates[key]) for key in ("publication", "vote_start", "vote_end")) or datetime.fromisoformat(dates["vote_start"].replace("Z", "+00:00")) >= datetime.fromisoformat(dates["vote_end"].replace("Z", "+00:00")):
            date_failures.append(item["pip_id"])
    require(not date_failures, "date_integrity", "a date is missing, malformed, or out of order", date_failures)

    binary = [item for item in records if item["vote"]["mechanism"] == "BINARY_PVP"]
    elections = [item for item in records if item["vote"]["mechanism"] == "RANKED_CHOICE_ELECTION"]
    require(actual_election_pips == source_election_pips, "source_election_partition", "generated election membership does not match source vote mechanisms", sorted(actual_election_pips ^ source_election_pips))
    require(actual_failed_pips == source_failed_pips, "source_failed_partition", "generated failed membership does not match source reviewed results", sorted(actual_failed_pips ^ source_failed_pips))
    require(actual_passed_non_election_pips == source_passed_non_election_pips, "source_passed_partition", "generated authorized non-election membership does not match source reviewed results", sorted(actual_passed_non_election_pips ^ source_passed_non_election_pips))
    require(actual_election_pips == EXPECTED_ELECTION_PIPS, "expected_election_regression", "source-derived election set changed from the reviewed regression guard", sorted(actual_election_pips))
    require(actual_failed_pips == EXPECTED_FAILED_PIPS, "expected_failed_regression", "source-derived failed set changed from the reviewed regression guard", sorted(actual_failed_pips))
    require(len(binary) == 28 and len(elections) == 5, "mechanism_partition", "binary/election partition is incorrect")
    require(all("COUNCIL_ELECTION" not in by_number[number]["category"]["normalized"] for number in (10, 13)), "category_precision", "PIP-10 or PIP-13 was misclassified as an election category")
    binary_failures = []
    for item in binary:
        vote = item["vote"]
        values = vote["binary"]
        expected = "PASSED" if Decimal(values["yes_pvp"]) > Decimal(values["no_pvp"]) else "FAILED"
        summed = sum(Decimal(value) for value in (values["yes_pvp"], values["no_pvp"], values["abstain_pvp"]) if value is not None)
        if vote["election"] is not None or item["result"]["reviewed_result"] != expected or Decimal(vote["total_pvp"]) != summed:
            binary_failures.append(item["pip_id"])
    require(not binary_failures, "binary_vote_reconciliation", "a binary result or total does not reconcile", binary_failures)
    require(by_number[9]["vote"]["binary"]["abstain_pvp"] is None and by_number[9]["vote"]["binary"]["abstain_capture_status"] == "NOT_CAPTURED_OR_NOT_OFFERED", "pip_9_abstain_gap", "PIP-9 absence of abstain evidence was converted to zero")

    election_failures = []
    for item in elections:
        vote = item["vote"]
        election = vote["election"]
        raw = read_json(ROOT / item["sources"]["full_text_source_path"])
        if vote["binary"] is not None or election["candidate_totals_status"] != "MISSING_FROM_CAPTURE" or any(candidate["candidate_pvp"] is not None or candidate["candidate_ballots"] is not None for candidate in election["candidates"]) or election["candidate_count"] != len(raw.get("voteOptions") or []):
            election_failures.append(item["pip_id"])
    require(not election_failures, "elections_not_binary_or_inferred", "an election has binary or invented candidate totals", election_failures)
    require(by_number[6]["result"]["reviewed_result"] == "FIRST_ROUND_ADVANCEMENT_RECORDED" and len(by_number[6]["vote"]["election"]["official_outcome_names"]) == 12, "pip_6_advancement", "PIP-6 is not preserved as first-round advancement")
    require(by_number[7]["result"]["reviewed_result"] == "ELECTED_OFFICEHOLDERS_RECORDED" and len(by_number[7]["vote"]["election"]["official_outcome_names"]) == 5, "pip_7_winners", "PIP-7 final winners are not preserved")
    unresolved_election_pips = {
        item["pip_number"] for item in elections if not item["vote"]["election"]["official_outcome_names"]
    }
    require(all(by_number[number]["result"]["reviewed_result"] == "COUNCIL_REPORTED_PASSAGE_WINNERS_UNRESOLVED" and by_number[number]["vote"]["election"]["outcome_identification_status"] == "UNRESOLVED" for number in unresolved_election_pips), "unresolved_elections", "an unresolved election inferred a winner")
    require(all(by_number[number]["authorization"]["state"] == "NOT_APPLICABLE_ELECTION" and by_number[number]["implementation"]["state"] == "NOT_APPLICABLE_ELECTION" and by_number[number]["implementation"]["independent_verification_state"] == "NOT_APPLICABLE_ELECTION" for number in actual_election_pips), "election_lifecycle_separation", "an election outcome was reused as authorization, implementation, or implementation-verification state")
    candidate_wallets = [candidate for item in elections for candidate in item["vote"]["election"]["candidates"]]
    require(all(candidate["wallet_public_key"] != SOLANA_SENTINEL_WALLET and (candidate["captured_wallet_value"] != SOLANA_SENTINEL_WALLET or (candidate["wallet_public_key"] is None and candidate["wallet_identification_status"] == "PLACEHOLDER_IN_CAPTURE")) for candidate in candidate_wallets), "candidate_wallet_placeholders", "a sentinel candidate-wallet value was normalized as an identified wallet")
    require(by_number[27]["vote"]["election"]["winner_count_configured"] == 5 and by_number[27]["vote"]["election"]["max_choices"] == 6 and by_number[27]["vote"]["election"]["candidate_count"] == 13, "pip_27_configuration", "PIP-27 captured ballot discrepancy was normalized away")
    require(all(by_number[number]["authorization"]["state"] == "NOT_AUTHORIZED" and by_number[number]["implementation"]["state"] == "NOT_APPLICABLE_NO_AUTHORIZATION" and by_number[number]["implementation"]["independent_verification_state"] == "NOT_APPLICABLE_NO_AUTHORIZATION" for number in actual_failed_pips), "failed_no_authorization", "a failed PIP has authorization, implementation, or an applicable implementation-verification state")
    require(all(by_number[number]["implementation"]["independent_verification_state"] == "MISSING_INDEPENDENT_PRIMARY_EVIDENCE" for number in actual_passed_non_election_pips), "authorized_implementation_verification_gap", "an authorized non-election proposal lacks the required missing-primary-evidence state")
    require(all(by_number[number]["implementation"]["council_reported_state"] == "MILESTONES_REPORTED_COMPLETE" and by_number[number]["implementation"]["attribution"] == "STAR_ATLAS_COUNCIL_TRACKER" for number in actual_failed_pips), "failed_tracker_conflict_preserved", "a failed proposal lost its contradictory attributed Council milestone state")
    failed_conflict = next(item for item in conflicts if item["conflict_id"] == "GOV-CONFLICT-FAILED-MILESTONES-001")
    require(set(failed_conflict["pip_numbers"]) == actual_failed_pips and "implementation.independent_verification_state" in failed_conflict["treatment"], "failed_conflict_scope", "the failed-milestones conflict does not cover the source-derived failed set and both implementation dimensions")
    require(by_number[14]["implementation"]["state"] == "COUNCIL_REPORTED_TERMINATED" and by_number[17]["implementation"]["state"] == "COUNCIL_REPORTED_CANCELED" and by_number[31]["implementation"]["state"] == "COUNCIL_REPORTED_WITHDRAWN_AFTER_PASSAGE_NOT_IMPLEMENTED", "terminal_states", "termination, cancellation, or withdrawal state was collapsed")
    require(any(rel["from_pip"] == 23 and rel["to_pip"] == 4 and rel["relationship"] == "SUPERSEDES" for rel in by_number[23]["relationships"]), "pip_23_supersedes_4", "PIP-23 supersession of PIP-4 is missing")

    treasury_failures = []
    for item in records:
        for field, value in item["treasury_states"].items():
            if value not in TREASURY_STATES_BY_FIELD[field]:
                treasury_failures.append(f"{item['pip_id']}:{field}={value}")
    require(not treasury_failures, "treasury_vocabulary_by_field", "a treasury state uses a value prohibited for that dimension", treasury_failures)
    failed_treasury_pips = {number for number in actual_failed_pips if by_number[number]["treasury_states"]["request_state"] == "REQUESTED"}
    require(all(all(by_number[number]["treasury_states"][key] is None for key in ("authorization_state", "payment_state", "onchain_verification_state")) for number in failed_treasury_pips), "failed_treasury_separation", "a failed funding request retains treasury authorization, payment, or verification state")
    concrete_reported = {
        number
        for number, pip in source_by_number.items()
        if any(
            value is not None and str(value).strip().upper() not in {"", "?", "N/A", "NA", "NONE", "NULL"}
            for key, value in ((pip.get("council_tracker") or {}).get("payment_fields") or {}).items()
            if key in {"paid_usdc", "paid_atlas"}
        )
        and by_number[number]["treasury_states"]["authorization_state"] == "AUTHORIZED"
    }
    require(all(by_number[number]["treasury_states"]["payment_state"] == "COUNCIL_REPORTED" and by_number[number]["treasury_states"]["onchain_verification_state"] == "MISSING_ONCHAIN_EVIDENCE" for number in concrete_reported), "council_payments_attributed", "a concrete Council payment report is missing attribution or overstates verification")
    authorized_without_payment_evidence = {
        item["pip_number"]
        for item in records
        if item["treasury_states"]["authorization_state"] == "AUTHORIZED"
        and item["pip_number"] not in concrete_reported
        and item["pip_number"] != 33
    }
    require(all(by_number[number]["treasury_states"]["payment_state"] == "UNVERIFIED" and by_number[number]["treasury_states"]["onchain_verification_state"] == "UNVERIFIED" for number in authorized_without_payment_evidence), "unreported_payments_not_inferred", "an authorization without payment evidence was treated as a payment or missing transaction", sorted(authorized_without_payment_evidence))
    pip33 = by_number[33]
    terms = pip33["financial_terms"]
    require(pip33["funding_scope"] == "DIRECT_DAO_TREASURY_MEASURE" and pip33["treasury_states"]["authorization_state"] == "AUTHORIZED", "pip_33_authorization", "PIP-33 authorization or funding scope is incorrect")
    require(pip33["treasury_states"]["payment_state"] == "UNVERIFIED", "pip_33_payment_occurrence", "PIP-33 authorization was conflated with payment occurrence")
    require(pip33["treasury_states"]["onchain_verification_state"] == "MISSING_ONCHAIN_EVIDENCE", "pip_33_onchain_evidence", "PIP-33 missing on-chain evidence is not preserved in the verification dimension")
    require(terms["stated_total_usd"] == "469513.53" and terms["stated_composition"] == {"usdc_percent": 75, "atlas_percent": 25, "stated_usdc_total": "352135.15", "stated_atlas_equivalent_total": "117378.38"} and terms["payment_verified"] is False, "pip_33_stated_terms", "PIP-33 stated total, composition, or unverified-payment flag changed")
    require([item["sequence"] for item in terms["tranches"]] == [1, 2] and all(item["amount_usd"] == "234756.76" and item["usdc_percent"] == 75 and item["usdc_amount"] == "176067.57" and item["atlas_percent"] == 25 and item["atlas_equivalent_usd"] == "58689.19" for item in terms["tranches"]), "pip_33_tranche_composition", "PIP-33 two-tranche 75/25 composition is not preserved")
    require(terms["tranches"][0]["timing"] == "T_PLUS_14_DAYS_AFTER_PASSAGE" and terms["tranches"][1]["timing"] == "180_DAYS_AFTER_TRANCHE_1" and terms["tranches"][1]["source_schedule"] == "T_PLUS_194_DAYS_AFTER_PASSAGE" and terms["tranches"][1].get("condition") == "DAO_TREASURY_MUST_RETAIN_CAPITAL_FOR_AN_ADDITIONAL_YEAR_OF_FOUNDATION_DAO_OPERATING_COSTS", "pip_33_tranche_timing", "PIP-33 source timing or conditional second tranche is not preserved")
    require({(item["field"], item["displayed_sum"], item["stated_total"], item["difference_usd"]) for item in terms["arithmetic_discrepancies"]} == {("tranche_total", "469513.52", "469513.53", "0.01"), ("usdc_total", "352135.14", "352135.15", "0.01")}, "pip_33_arithmetic_discrepancies", "PIP-33 one-cent discrepancies are not preserved exactly")
    require(all(item["financial_terms"] is None for item in records if item["pip_number"] != 33), "pip_33_financial_terms_exclusive", "PIP-33 financial terms leaked into another proposal")

    conflict_ids = {item["conflict_id"] for item in conflicts}
    backlog_ids = {item["research_id"] for item in backlog}
    require(all(set(item["conflict_ids"]) <= conflict_ids and set(item["research_backlog_ids"]) <= backlog_ids for item in records), "cross_references", "a conflict or research reference does not resolve")
    open_conflicts = [item for item in conflicts if item["status"] == "OPEN_DOCUMENTED"]
    related = {conflict_id for item in backlog for conflict_id in item["related_conflict_ids"]}
    require(all(item["required_artifacts"] for item in open_conflicts), "open_conflicts_artifacts", "an open conflict lacks required artifacts")
    require(all(item["conflict_id"] in related for item in open_conflicts), "open_conflicts_backlogged", "an open conflict is not linked to the research backlog", sorted(item["conflict_id"] for item in open_conflicts if item["conflict_id"] not in related))
    open_ids = {item["conflict_id"] for item in open_conflicts}
    require(all(item["reconciliation"]["overall_status"] == ("OPEN_DOCUMENTED_CONFLICTS" if set(item["conflict_ids"]) & open_ids else "RECONCILED_NO_OPEN_CONFLICTS") for item in records), "overall_reconciliation_status", "a record claims full reconciliation while an open documented conflict remains")
    tracker_input = "archive/semantic/governance/council-pip-tracker/council-pip-tracker-semantic-records.jsonl"
    require(tracker_input in ledger["source_inputs"] and (ROOT / tracker_input).exists(), "tracker_source_input", "Council tracker semantic input is absent from top-level provenance")
    research_004 = next(item for item in backlog if item["research_id"] == "GOV-RESEARCH-004")
    require(set(research_004["pip_numbers"]) == actual_passed_non_election_pips, "implementation_backlog_scope", "implementation research scope is not limited to source-derived authorized non-election proposals")
    research_001 = next(item for item in backlog if item["research_id"] == "GOV-RESEARCH-001")
    require(set(research_001["pip_numbers"]) == unresolved_election_pips, "election_backlog_scope", "unresolved-election research scope does not match generated election evidence")
    research_002 = next(item for item in backlog if item["research_id"] == "GOV-RESEARCH-002")
    missing_onchain_scope = {item["pip_number"] for item in records if item["treasury_states"]["onchain_verification_state"] == "MISSING_ONCHAIN_EVIDENCE"}
    require(set(research_002["pip_numbers"]) == missing_onchain_scope, "treasury_backlog_scope", "on-chain research scope does not match generated missing-evidence states")

    # Prove that proposal numbers do not construct lifecycle state.
    builder_source = GENERATOR.read_text(encoding="utf-8")
    require(all(marker not in builder_source for marker in ("ELECTION_PIPS =", "FAILED_PIPS =", "PASSED_NON_ELECTION_PIPS =")), "no_generator_lifecycle_membership_sets", "generator retains a hard-coded lifecycle membership set")
    try:
        spec = importlib.util.spec_from_file_location("canonical_pip_ledger_builder", GENERATOR)
        if spec is None or spec.loader is None:
            raise RuntimeError("could not load generator module")
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        synthetic_failed = {
            "pip_number": 6,
            "vote_mechanism": "BINARY_PVP",
            "reviewed_result": "FAILED",
            "execution_state": "UNKNOWN",
            "council_reported_implementation_state": "MILESTONES_REPORTED_COMPLETE",
        }
        synthetic_election = {
            "pip_number": 13,
            "vote_mechanism": "RANKED_CHOICE_ELECTION",
            "reviewed_result": "PASSED",
            "execution_state": "UNKNOWN",
            "council_reported_implementation_state": "MILESTONES_REPORTED_COMPLETE",
        }
        derived_behavior = (
            builder.authorization_state(synthetic_failed) == "NOT_AUTHORIZED"
            and builder.implementation_state(synthetic_failed) == "NOT_APPLICABLE_NO_AUTHORIZATION"
            and builder.implementation_verification_state(synthetic_failed) == "NOT_APPLICABLE_NO_AUTHORIZATION"
            and builder.authorization_state(synthetic_election) == "NOT_APPLICABLE_ELECTION"
            and builder.implementation_state(synthetic_election) == "NOT_APPLICABLE_ELECTION"
            and builder.implementation_verification_state(synthetic_election) == "NOT_APPLICABLE_ELECTION"
        )
        derivation_detail: Any = None
    except Exception as exc:  # pragma: no cover - reported as a named validation failure
        derived_behavior = False
        derivation_detail = str(exc)
    require(derived_behavior, "source_derived_lifecycle_behavior", "lifecycle helpers depend on proposal-number membership rather than source fields", derivation_detail)

    campaign_summary = parsed["campaign-summary.json"]
    require(set(campaign_summary["failed_pips"]) == actual_failed_pips and set(campaign_summary["unresolved_election_outcomes"]) == unresolved_election_pips, "campaign_summary_source_scopes", "campaign summary lifecycle scopes do not reconcile to generated records")
    require(campaign_summary["lifecycle_generation_basis"] == "SOURCE_BACKED_VOTE_MECHANISM_AND_REVIEWED_RESULT", "campaign_summary_generation_basis", "campaign summary does not disclose its source-derived lifecycle basis")
    require(campaign_summary["pip_33_treasury_states"] == {"payment_state": "UNVERIFIED", "onchain_verification_state": "MISSING_ONCHAIN_EVIDENCE", "payment_implied": False}, "campaign_summary_pip_33", "campaign summary misstates the PIP-33 payment/on-chain boundary")

    markdown = LEDGER_MD.read_text(encoding="utf-8")
    ledger_table = markdown.split("## Election detail", 1)[0]
    row_ids = re.findall(r"^\| (PIP-\d{2}) \|", ledger_table, flags=re.MULTILINE)
    require(row_ids == [item["pip_id"] for item in records], "markdown_ledger_reconciliation", "human ledger rows do not reconcile to machine records", len(row_ids))
    require(not internal_links(LEDGER_MD), "internal_links", "human ledger contains broken internal links", internal_links(LEDGER_MD))

    # Regeneration must be byte-identical from the committed or staged state.
    before = {path.relative_to(ROOT).as_posix(): digest(path) for path in GENERATED}
    generated = run([sys.executable, str(GENERATOR)])
    after = {path.relative_to(ROOT).as_posix(): digest(path) for path in GENERATED}
    differing = sorted(path for path in before if before[path] != after[path])
    require(generated.returncode == 0 and not differing, "deterministic_regeneration", "ledger regeneration is not byte-deterministic", differing or generated.stderr)

    paths = changed_paths()
    prohibited = [path for path in paths if path.startswith(("archive/", "graph/", "publication/"))]
    unrelated = [path for path in paths if not path.startswith(("knowledge/governance/PIP-Registry.", "knowledge/governance/README.md", "operations/campaigns/canonical-pip-governance-ledger-2026-07/", "operations/ci/validate_repository.py"))]
    require(not prohibited, "source_and_prohibited_layers_unchanged", "archive evidence, graph, or publication changed", prohibited)
    require(not unrelated, "allowed_paths_only", "campaign changed an unrelated path", unrelated)
    diff_check = run(["git", "diff", "--check"])
    require(diff_check.returncode == 0, "git_diff_check", "git diff --check failed", diff_check.stdout)

    manifest_paths = [
        LEDGER_JSON,
        LEDGER_MD,
        HERE / "README.md",
        HERE / "build_ledger.py",
        HERE / "validate_ledger.py",
        HERE / "canonical-pip-governance-ledger.schema.json",
        HERE / "conflict-report.json",
        HERE / "conflict-report.md",
        HERE / "governance-research-backlog.json",
        HERE / "governance-research-backlog.md",
        HERE / "campaign-summary.json",
        HERE / "campaign-summary.md",
    ]
    manifest = {
        "campaign_id": "canonical-pip-governance-ledger-2026-07",
        "as_of": "2026-07-18",
        "artifact_count": len(manifest_paths),
        "artifact_normalization": "UTF8_TEXT_CRLF_NORMALIZED_TO_LF_BEFORE_SHA256_AND_SIZE",
        "artifacts": [{"path": path.relative_to(ROOT).as_posix(), "sha256": manifest_digest(path), "size_bytes": manifest_size(path)} for path in sorted(manifest_paths, key=lambda item: item.relative_to(ROOT).as_posix().casefold())],
    }
    write_json(HERE / "manifest.json", manifest)

    status = "PASS" if not failures else "FAIL"
    report = {
        "campaign_id": "canonical-pip-governance-ledger-2026-07",
        "status": status,
        "as_of": "2026-07-18",
        "checks": checks,
        "warnings": warnings,
        "failures": failures,
        "records_validated": len(records),
        "documented_conflicts": len(conflicts),
        "research_backlog_items": len(backlog),
    }
    write_json(HERE / "validation-report.json", report)
    lines = [
        "# Canonical PIP and Governance Ledger Validation",
        "",
        f"**Result: {status}**",
        "",
        f"- PIP records: {len(records)}",
        f"- Documented conflict clusters: {len(conflicts)}",
        f"- Research backlog items: {len(backlog)}",
        f"- Checks passed: {sum(value['passed'] for value in checks.values())}/{len(checks)}",
        "- On-chain verification performed: no",
        "- Archive source records rewritten: no",
        "- Graph modified: no",
        "- Publication modified: no",
        "",
        "## Checks",
        "",
    ]
    for name, value in checks.items():
        lines.append(f"- {'PASS' if value['passed'] else 'FAIL'} — `{name}`")
    if failures:
        lines += ["", "## Failures", ""] + [f"- {item}" for item in failures]
    lines += ["", "## Preserved limitations", ""] + [f"- {item}" for item in warnings] + [""]
    (HERE / "validation-report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Validation {status}: {len(failures)} failures; {len(checks)} checks; {len(records)} PIPs")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
