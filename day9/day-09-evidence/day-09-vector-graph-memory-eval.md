# Day 9 - Data For AI At Scale Evidence

## 1. Lane And Dataset

- Lane: Insurance
- Primary dataset: `Insurance/Insurance Claims and Policy Data/Insurance Claims and Policy Data.zip`
- Fallback used:
- Evidence folder: `Persistent_Folder/day-09-evidence`

## 2. Business Question

Can a claims agent answer a governed claims question with citation, permission check, graph path, memory scope and evaluation evidence?

## 3. Serving Architecture

Paste the Day 9 serving diagram or explain the path here.

## 4. Feature, Vector, Graph And Memory Proof

Paste actual command outputs and file names here.

## 5. Permission-Aware Retrieval

| User role | Question | Decision | Reason |
| --- | --- | --- | --- |

## 6. Grounded Answer And Citations

Paste the cited answer and source ids.

## 7. GraphRAG Path

Paste graph path or fallback edge list.

## 8. Memory Scope And Expiry

Paste memory rule, TTL and deletion note.

## 9. Evaluation

| Metric | Result | Evidence |
| --- | --- | --- |

## 10. Audit And Cost

Paste audit row, cache result and estimated cost.

## 11. GCP Translation

| VM proof | GCP managed service | Control before trust |
| --- | --- | --- |

## 12. AI Assistance Used

- Tool:
- Prompt:
- What I accepted:
- What I rejected or corrected:

## 13. Tool Coverage Passport

| Tool | What I used it for | Evidence status |
| --- | --- | --- |
| VS Code / Jupyter | Artifact and runnable proof | |
| Python 3.12 | Embedding, retrieval, permission, memory and evaluation proof | |
| Qdrant | Vector search with payload filter | |
| LanceDB | Local vector table with metadata filter | |
| Neo4j | Entity graph and multi-hop GraphRAG path | |
| Postgres | Offline feature store (point-in-time join), access audit and governed NL query event | |
| Redis | Online feature store, semantic cache and memory TTL | |
| dbt | Builds `governed_claim_features` from claim events; PII-free semantic layer | |
| Airflow | `day09_rag_refresh` DAG: reindex -> evaluate -> permission gate -> publish | |
| Prometheus / Grafana | `day-09-rag-metrics.prom` scrape target + alert rule | |
| gcloud CLI | GCP AI-serving translation | |
| Codex or Claude | Draft/review assistant with human verification | |