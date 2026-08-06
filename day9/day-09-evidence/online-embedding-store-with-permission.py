import json, subprocess
import importlib

#from day_09_ai_serving_layer import chunks, embed 

serving_layer = importlib.import_module("day-09-ai-serving-layer")
chunks = serving_layer.chunks
embed = serving_layer.embed

points = []

for idx, item in enumerate(chunks, start=1):
    points.append({
        "id": idx,
        "vector": [round(v, 6) for v in embed(item["text"])],
        "payload": {
            "source_id": item["source_id"],
            "allowed_roles": item["allowed_roles"],
            "text": item["text"]
        }
    })
body = json.dumps({"points": points})
open("day-09-qdrant-points.json", "w").write(body)
print(f"built {len(points)} points from the ai serving layer chunks")
print(f"first vector:", points[0]["vector"])
