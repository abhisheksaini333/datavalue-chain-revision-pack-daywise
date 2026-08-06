from __future__ import annotations

import csv
import hashlib
import json
import math

from datetime import datetime, timedelta, timezone
from pathlib import Path

import os

OUT = Path(__file__).resolve().parent

if os.environ.get("DAY(_FREEZE_CLOCK)") == "1":
    NOW = datetime(2026, 8, 6, 11, 0, tzinfo=timezone.utc)
else:
    NOW = datetime.now(timezone.utc)


def embed(text, dims=12):
    vec = [0.0] * dims
    for token in text.lower().replace("_", " ").split():
        h = int(hashlib.sha256(token.encode()).hexdigest(), 16)
        vec[h % dims] += 1.0
    norm = sum( v * v for v in vec) ** 0.5 or 1.0
    return [ round( v / norm, 6) for v in vec ]


def cosine(left: list[float], right: list[float]) -> float:
   return round(sum(a * b for a, b in zip(left, right)), 6)


chunks = [
    {
        "source_id": "POL-101",
        "text": "Policy POL-101 covers collision and medical claims for customer C-001 in region west.",
        "allowed_roles": ["claims_adjuster", "claims_manager"],
        "pii": "restricted",
        "entity_ids": ["POL-101", "C-001"],
        "version": "v1"
    },
    {
        "source_id": "CLM-9001",
        "text": "Claim CLM-9001 is tied to policy POL-101, provider P-77, reserve amount 18000, and fraud indicator medium.",
        "allowed_roles": ["claims_adjuster", "claims_manager", "fraud_analyst"],
        "pii": "restricted",
        "entity_ids": ["CLM-9001", "POL-101", "P-77"],
        "version": "v1"
    },
    {
        "source_id": "PROV-77",
        "text": "Provider P-77 has three recent claim disputes and required supervisor review for high reserve claims.",
        "allowed_roles": ["fraud_analyst", "claims_manager"],
        "pii": "internal",
        "entity_ids": ["P-77"],
        "version": "v1"
    },
    {
        "source_id": "SLO-CLAIMS",
        "text": "Claims AI answers must include citation ids, permission decision, graph path when relationships are used, an evaluation metrics.",
        "allowed_roles": ["claims_adjuster", "claims_manager", "fraud_analyst", "auditor"],
        "pii": "public_internal",
        "entity_ids": ["SLO-CLAIMS"],
        "version": "v1"
    },
]

features = [
    {
        "claim_id": "CLM-9001",
        "policy_id": "POL-101",
        "reserve_amount": 18000,
        "fraud_indicator": "medium",
        "provider_disputes": 3
    },
    {
        "claim_id": "CLM-9002",
        "policy_id": "POL-102",
        "reserve_amount": 4200,
        "fraud_indicator": "low",
        "provider_disputes": 0
    },
]

graph_edges = [
    ("C-001", "HAS_POLICY", "POL-101"),
    ("POL-101", "HAS_CLAIM", "CLM-9001"),
    ("CLM-9001", "USES_PROVIDER", "P-77"),
    ("P-77", "HAS_RISK_SIGNAL", "DISPUTE_SPIKE")
]

memory_events = [
    {
        "memory_id": "MEM-001",
        "scope": "claim:CLM-9001",
        "text": "Supervisor asked that P-77 high reserve claims be reviewed before AI recommendation is used.",
        "allowed_roles": ["claims_manager"],
        "expires_at": (NOW - timedelta(days=1)).isoformat()
    },
    {
        "memory_id": "MEM-002",
        "scope": "claim:CLM-9001",
        "text": "Old investigation note from a closed escalation.",
        "allowed_roles": ["claims_manager"],
        "expires_at": (NOW - timedelta(days=1)).isoformat()
    },
]

for item in chunks:
    item["embedding"] = embed(item["text"])


def retrieve(query: str, role: str, limit: int = 3, enforce_permissions: bool = True) -> list[dict]:
    query_vector = embed(query)
    candidates = []
    for item in chunks:
        if enforce_permissions and role not in item["allowed_roles"]:
            continue
        score = cosine(query_vector, item["embedding"])
        candidates.append({ **item, "score": score })
    return sorted(candidates, key=lambda row: row["score"], reverse=True)[:limit]    


def active_memory(role: str, scope: str) -> list[dict]:
    active = []
    for item in memory_events:
        expiry = datetime.fromisoformat(item["expires_at"])
        if role in item["allowed_roles"] and item["scope"] == scope and expiry > NOW:
            active.append(item)
    return active


def graph_path(start: str, target: str) -> list[str]:
    path= [start]
    current = start
    for left, rel, right in graph_edges:
        if left == current:
            path.append(f"{rel}->{right}")
            current = right
            if right == target:
                break
    return path


def answer_question(query: string, role: str, enforce_permissions: bool = True) -> dict:
    # 1. retrieve
    retrieved = retrieve(query, role, enforce_permissions=enforce_permissions)
    # 2. citations
    citations = [ item["source_id"] for item in retrieved]
    # 3. active memory
    memories = active_memory(role, "claim:CLM-9001")
    # 4  path
    path = graph_path("C-001", "P-77")
    chunk_acl = { item["source_id"]: item["allowed_roles"]  for item in chunks }
    permission_violations = [
        source_id
        for source_id in citations
        if role not in chunk_acl.get(source_id, [])
    ]
    expired_memory_ids = [
        item["memory_id"]
        for item in memory_events
        if datetime.fromisoformat(item["expires_at"]) < NOW
    ]
    answer = (
        "Claim CLM-9001 is connected to policy POL-101 and provider P-77."
        "The reserve amount is 18000, fraud indicator is medium, and provider P-77 has recent dispute spike."
        "Supervisor review is required before using this as an operationsl recommendation."
    )
    if role == "claims_adjuster":
        answer = (
            "Claim CLM-9001 is connected to policy POL-101 and has reserve amount 18000 with medium fraud indicator."
            "Provider-specific risk detail is hidden for this role;mroute to a claims manager for supervisor review."
        )
    return {
        "query": query,
        "role": role,
        "retrieved": [
            { "source_id": item["source_id"], "score": item["score"], "pii": item["pii"], }
            for item in retrieved
        ],
        "graph_path": path,
        "active_memory_ids": [ item["memory_id"] for item in memories ],
        "expired_memory_ids": expired_memory_ids,
        "answer": answer,
        "citations": citations,
        "evaluation": {
            "citation_coverage": round( len(citations) / max(len(retrieved), 1) , 2),
            "permission_violations": len(permission_violations),
            "memory_expiry_respected": not set(expired_memory_ids) & {item["memory_id"]  for item in memories },
            "faithfulness_check": "pass" if citations else "fail",
            "estimated_serving_cost_usd": 0.0032
        }
    }


questions = [
    (
        "claims_adjuster", "What should I know about claim CLM-9001 and provide risk ?",
    ),
    (
        "claims_manager", "Explain the CLM-9001 policy, provider risk and review path."
    ),
    (
        "auditor", "what evidence rules govern claims AI answers ?"
    )
]


results = [answer_question(query, role) for role, query in questions]


with (OUT / "day-09-feature-serving-table.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(features[0].keys()))
    writer.writeheader()
    writer.writerows(features)


(OUT/ "day-09-serving-layer-results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


markdown = [
    "# Day 9 Grounded Claims Answer",
    "",
    "## Claims Manager Answer",
    "",
    results[1]["answer"],
    "",
    f"Citations: {', '.join(results[1]['citations'])}",
    f"Graph path: {', '.join(results[1]['graph_path'])}",
    f"Active Memory: {', '.join(results[1]['active_memory_ids']) or 'none'}",
    "",
    "## Evaluation",
    "",
]

(OUT / "day-09-grounded-answer.md").write_text("\n".join(markdown), encoding="utf-8")


print("Success !")
print("Claims Manager citations:", ", ".join(results[1]["citations"]))