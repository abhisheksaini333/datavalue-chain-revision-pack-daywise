# Capstone Playbook

## Capstone Outcome

Each team ships an agentic data solution that demonstrates the full value chain and is logged on Ignite for the hackathon pipeline:

1. A governed data product.
2. A tested pipeline.
3. Quality, lineage, classification, and MDM evidence.
4. A safe data-access agent.
5. At least one advanced capability: streaming, orchestration, active metadata, FinOps, GraphRAG, or agent memory.
6. A proof pack with evaluation, cost, ROI, governance, and audit.

## Problem Statement Template

- Industry lane:
- Sandbox lane: VM-only / Databricks / AWS / Azure / GCP
- Business user:
- Decision or workflow improved:
- Source data:
- Target data product:
- Agentic capability:
- Risk boundary:
- Success metrics:
- Ignite idea title:
- Ignite problem statement:
- Proof-of-outcomes metric:
- Demo path:
- Persistent_Folder proof path:
- Cloud cleanup owner if applicable:

## Programme Idea Bank

| Code | Lane | Build | Proof |
| --- | --- | --- | --- |
| C1 | Insurance | Claims data value-chain modernization: messy ingestion to governed AI-ready claims product, self-healing pipeline, golden claimant, permission-aware text-to-SQL | Readiness time, pipeline incident rate, audited NL access |
| C2 | Banking | KYC and Customer-360 golden record with MDM match/merge, steward approval, lineage, classification, permission-aware access agent | Duplicate-resolution rate, match accuracy, source-of-record lineage |
| C3 | Supply chain/logistics | Streaming control-tower product with CDC/streaming, supplier/parts graph, GraphRAG control-tower agent | Freshness SLO, event-to-alert latency, multi-hop answer accuracy |
| C4 | Finance and accounts | Finance close and reconciliation platform with contracts, anomaly agent, semantic close metrics, governed NL analytics | Auto-flagged exceptions, contract catch rate, cost per data product |
| C5 | Healthcare | Patient data trust layer with PII/PHI classification, lineage, right-to-be-forgotten flows, cited agentic RAG | Lineage coverage, zero PII leakage in access tests, release audit packs |

## Required Proof Pack

- Capstone sandbox lane declaration from `templates/capstone-sandbox-lane-declaration.md`.
- Architecture diagram.
- Data contract.
- Pipeline run evidence.
- Quality results.
- Lineage and catalog screenshot or table.
- Access control decision.
- Agent prompt/tool/action trace.
- Evaluation results.
- Cost/ROI estimate.
- Known limitations and next steps.
- Ignite entry link or captured submission details.
- Live demo path plus recorded/screenshot fallback.
- Training-data-only statement.
- `Persistent_Folder` evidence path.
- Cloud stop/cleanup proof if AWS, Azure, or GCP was used.

## Sandbox Lane Requirements

| Lane | Required proof |
| --- | --- |
| VM-only | Tool list, local run output, saved proof folder, and production translation note |
| Databricks | Catalog/table/job/search/governance evidence where available, plus saved screenshots |
| AWS | us-east-1 service proof, Bedrock/S3/RDS/CloudWatch evidence if used, and cleanup confirmation |
| Azure | allowed region/SKU proof, Azure OpenAI/Search/Blob/Key Vault evidence if used, and cleanup confirmation |
| GCP | enabled service proof, Vertex/Cloud Storage/Cloud SQL/Secret Manager evidence if used, and cleanup confirmation |

## Shark Tank Pitch Structure

1. Problem in one sentence.
2. Current pain and cost.
3. Solution architecture.
4. Live demo.
5. Proof of outcome.
6. Governance and safety boundary.
7. ROI and scaling plan.
8. Ask or recommendation.

## Scoring Rubric

| Dimension | Weight | What Judges Look For |
| --- | ---: | --- |
| Problem and impact | 15 | Real, well-framed industry problem worth solving |
| Solution and innovation | 15 | Clear, creative, well-designed agentic solution |
| Technical execution | 20 | Working prototype, sound architecture, agentic depth |
| Proof of outcomes | 20 | Demonstrated results, evaluation evidence, metrics, working demo |
| Business value and ROI | 10 | Quantified value: resolution, cycle-time, cost, CSAT, productivity |
| Responsible AI and governance | 10 | Guardrails, human oversight, audit, compliance fit |
| Pitch and storytelling | 10 | Crisp, compelling, evidence-led pitch |

## Final Proof Audit

Before the Shark Tank pitch, every team must answer:

1. Which sandbox lane did you use?
2. Where is your proof saved in `Persistent_Folder`?
3. Which evidence proves the data was governed?
4. Which evidence proves the agent or model was controlled?
5. What did you stop or clean up if you used cloud?
6. What would change in production?
