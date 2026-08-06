import json
from datetime import datetime, timezone
from pathlib import Path

AUDIT = Path("day-07-tool-audit.json")

TOOL_REGISTRY = {
    "inspect_dag_status": {
        "purpose": "read-only DAG status lookup",
        "required": ["incident_id", "dag_id"],
        "approval_required": False,
        "reversible": True,
    },
    "trigger_approved_airflow_retry": {
        "purpose": "retry a known DAG run after incident review",
        "required": ["incident_id", "dag_id", "run_id", "idempotency_key"],
        "approval_required": False,
        "reversible": True,
    },
    "run_dbt_tests": {
        "purpose": "run named data tests as verification",
        "required": ["incident_id", "model", "test_name"],
        "approval_required": False,
        "reversible": True,
    },
    "apply_schema_mapping": {
        "purpose": "map a renamed source field in the staging transform",
        "required": ["incident_id", "dataset", "mapping", "idempotency_key"],
        "approval_required": True,
        "reversible": False,
    },
}

SEEN_KEYS = {}
audit_log = []

def audit(tool, decision, reason, params):
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "tool": tool,
        "decision": decision,
        "reason": reason,
        "incident_id": params.get("incident_id", "unknown"),
    }
    audit_log.append(entry)
    print(f"  [AUDIT] {decision:<8} {tool:<32} {reason}")
    return entry

def call_tool(tool_name, params, approval=None):
    print(f"\nagent requests -> {tool_name}")

    # Control 1: allowlist. An agent cannot invent a tool.
    if tool_name not in TOOL_REGISTRY:
        audit(tool_name, "DENIED", "tool not in registry", params)
        return {"ok": False}

    spec = TOOL_REGISTRY[tool_name]

    # Control 2: schema. Every required parameter must be present.
    missing = [p for p in spec["required"] if p not in params]
    if missing:
        audit(tool_name, "DENIED", f"missing required params: {missing}", params)
        return {"ok": False}

    # Control 3: approval gate on irreversible actions.
    if spec["approval_required"] and approval != "approved":
        audit(tool_name, "BLOCKED", "approval required, none supplied", params)
        return {"ok": False}

    # Control 4: idempotency. The same key never executes twice.
    key = params.get("idempotency_key")
    if key and key in SEEN_KEYS:
        audit(tool_name, "SKIPPED", f"idempotency key already executed: {key}", params)
        return {"ok": True, "replayed": True}
    if key:
        SEEN_KEYS[key] = True

    audit(tool_name, "ALLOWED", spec["purpose"], params)
    return {"ok": True}

INC = "INC-CLAIMS-007"

print("=== 1. read-only call: allowed ===")
call_tool("inspect_dag_status", {"incident_id": INC, "dag_id": "claims_ingest"})

print("\n=== 2. agent invents a tool that is not in the registry ===")
call_tool("drop_table", {"incident_id": INC, "table": "claims_raw"})

print("\n=== 3. schema change WITHOUT approval ===")
call_tool("apply_schema_mapping", {
    "incident_id": INC, "dataset": "insurance_claims_feed",
    "mapping": "amount_paid->claim_amount", "idempotency_key": f"{INC}:schema"})

print("\n=== 4. malformed call: missing idempotency key ===")
call_tool("trigger_approved_airflow_retry", {"incident_id": INC, "dag_id": "claims_ingest", "run_id": "r1"})

print("\n=== 5. schema change WITH owner approval ===")
call_tool("apply_schema_mapping", {
    "incident_id": INC, "dataset": "insurance_claims_feed",
    "mapping": "amount_paid->claim_amount", "idempotency_key": f"{INC}:schema"},
    approval="approved")

print("\n=== 6. same approved call replayed (idempotency) ===")
call_tool("apply_schema_mapping", {
    "incident_id": INC, "dataset": "insurance_claims_feed",
    "mapping": "amount_paid->claim_amount", "idempotency_key": f"{INC}:schema"},
    approval="approved")

print("\n=== 7. verification test after repair ===")
call_tool("run_dbt_tests", {"incident_id": INC, "model": "stg_claims", "test_name": "required_claim_amount"})

AUDIT.write_text(json.dumps(audit_log, indent=2))
print(f"\nSaved {AUDIT} with {len(audit_log)} audit events")
counts = {}
for e in audit_log:
    counts[e["decision"]] = counts.get(e["decision"], 0) + 1
print("Decision summary:", counts)