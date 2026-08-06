import json, urllib.request
import importlib

serving_layer = importlib.import_module("day-09-ai-serving-layer")
embed = serving_layer.embed

QUESTION = "What is the fraud risk for claim CLM-9001 ?"

def qdrant_query(role):
    body = json.dumps({
        "query": [round(v, 6) for v in embed(QUESTION)],
        "limit": 3,
        "with_payload": True,
        "filter": {"must": [{ "key": "allowed_roles", "match": {"any": [role]} }]},
    }).encode()
    req = urllib.request.Request(
        "http://localhost:6333/collections/day09_claim_chunks_new/points/query",
        data = body,
        headers = {
            "Content-Type": "application/json"
        },
        method = "POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())["result"]["points"]


#iterate over thr roles
for role in ["claims_adjuster", "claims_manager"]:
    hits = qdrant_query(role)
    ids = [h["payload"]["source_id"] for h in hits]
    print(f"{role:16} -> {ids}")