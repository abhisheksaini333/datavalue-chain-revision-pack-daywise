from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request


app = Flask(__name__)
RESULT_FILE = Path("logs") / "smoke_test_result.json"


def load_smoke_result() -> dict:
    if RESULT_FILE.exists():
        return json.loads(RESULT_FILE.read_text())
    return {"status": "UNKNOWN", "message": "smoke test has not been run"}

@app.get("/health")
def health():
    return jsonify({
        "status": "alive",
        "checked_at_utc": datetime.now(timezone.utc).isoformat()
    })


@app.get("/ready")
def ready():
    smoke = load_smoke_result()
    forced = request.args.get("smoke")
    if forced == "fail":
        smoke["status"] = "FAIL"
    ready_status = smoke.get("status") == "PASS"
    return jsonify({
        "ready": ready_status,
        "reason": "smoke_test_passed" if ready_status else "blocked_until_smoke_test_passes",
        "smoke_test_status": smoke.get("status")
    }), 200 if ready_status else 503


@app.get("/slo")
def slo():
    return jsonify({
        "freshness_slo_hours": 24,
        "reliability_slo_percent": 99.0,
        "quality_gate": "smoke_test_status_must_be_PASS",
        "incident_owner": "data_product_owner",
    })

@app.get("/cost")
def cost():
    return jsonify({
        "estimated_monthly_demo_cost_usd": 5,
        "cost_owner": "data_product_owner",
        "hard_cap_required_before_production": True,
        "smart_routing_rule": "use smaller model or cached result for low-risk questions",
    })

@app.get("/agent-card")
def agent_card():
    secret_present = bool(os.environ.get("DEMO_SECRET"))
    return jsonify({
        "agent_name": "insurance-production-readiness-agent",
        "allowed_actions": ["summarise readiness", "explained failed checks", "draft release notes"],
        "blocked_actions": ["change access policy", "delete records", "approve its own release"],
        "human_approval_required_for": ["production deployment", "policy change", "data deletion"],
        "secret_loaded_without_displaying_value": secret_present
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)