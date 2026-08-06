## Course Syllabus Gap Closure - Day 1 Foundation Choices

### Open Table Format Choice

Chosen enterprise pattern: Iceberg-first for portability; Delta noted for Databricks; Hudi noted for upsert-heavy ingestion.
Classroom hands-on equivalent: BigQuery-managed tables plus local Markdown catalog.
Reason: the sandbox proves the design logic even if the exact enterprise table format is discussed conceptually.

### Catalog Namespace

Enterprise namespace example: `workspace.catalog.schema.table`
GCP classroom equivalent: `project.dataset.table`
Owner: Claims operations manager
Tags: insurance, policy, claims-foundation
PII fields suspected: customer/person identifiers, contact details, policy identifiers

### Medallion Layout

| Layer  | Table/folder                   | Purpose                           | Quality expectation          |
| ------ | ------------------------------ | --------------------------------- | ---------------------------- |
| Bronze | `bronze_policy_raw`          | Raw landed policy data            | Preserve source shape        |
| Silver | `silver_policy_clean`        | Cleaned, typed, deduplicated data | Valid schema and null checks |
| Gold   | `gold_claims_policy_product` | Business-ready product            | Defined metrics, owner, SLA  |

### Analytics And AI Model

Fact table: `fact_claim`
Dimensions: `dim_policy`, `dim_customer`, `dim_date`
Agent consumption fields: business definition, allowed questions, citation source, access rule

### AI-Ready Data Note

Dashboard-ready data supports charts. Agent-ready data supports governed SQL, retrieval over documents, embeddings/vector search, lineage, and citations.

### FinOps Estimate

| Cost item     | Assumption                                   | Estimated cost     | Owner              |
| ------------- | -------------------------------------------- | ------------------ | ------------------ |
| Storage       | small training file, future GB-scale product | classroom estimate | data product owner |
| Compute/query | profiling + queries + transformations        | classroom estimate | platform owner     |
| AI calls      | contract draft/retrieval/agent answer        | classroom estimate | AI product owner   |


# Day 1 - Modern Data Foundation And The Agentic Data Value Chain Evidence

## 1. Dataset

- Locked lane: Insurance
- Primary dataset path: `Insurance/Insurance/insurance policy data.xlsx`
- Fallback dataset path: `Retail/salesamp Retail/Sample - Superstore.xls`
- Dataset used today: `Insurance/Insurance/insurance policy data.xlsx`
- Evidence folder: `Persistent_Folder/day-01-evidence`

## 2. Business Decision

A claims operations manager must decide whether an insurance policy dataset is trustworthy enough to become the base for claims, policy, and customer analytics.

Decision owner: Claims operations manager

Action this decision supports: Approve the insurance policy dataset as the starting point for governed claims and policy analytics.

## 3. Why This Matters

Today we convert a raw insurance file into a named, inspectable data product starting point.

## 4. Risk If Wrong

If the policy data is wrong, an agent may answer from unmanaged or unauthorized data and leadership may trust a metric that cannot be defended.

## 5. Verification Evidence

Paste or type the proof from the live demo here:

- Row count or input count: pending until live profiling/test output is visible
- Column list or schema: pending until live profiling/test output is visible
- Quality/test result: pending until live verification runs
- AI-generated artifact inspected: pending
- Output saved to Persistent_Folder: pending
- Screenshot/log/query/result reference: pending

## 6. Build Evidence

What I built:

- one sentence describing the artifact built today

What I ran:

- command, notebook cell, SQL query, API call, graph query, or checklist used

What I observed:

- actual result visible on screen

## 7. What Can Still Go Wrong

Today proves basic profiling and contract thinking; it does not yet prove full quality, lineage, access control, or production readiness.

Additional learner note:

- Current learner note: waiting for verification output from the live lab.

## 8. GCP Translation

Today's GCP mapping: BigQuery dataset and Cloud Storage landing bucket concept.

In GCP this would become:

- Storage/query/state/serving service: BigQuery dataset and Cloud Storage landing bucket concept
- Console services to mention: Cloud Storage, BigQuery
- Secret or access-control boundary: Secret Manager/IAM concept must protect credentials and access
- Audit or monitoring evidence: audit log, query history, service log, or saved screenshot depending on the day

## 9. One-Sentence Business Value

Today we convert a raw insurance file into a named, inspectable data product starting point.

## 10. Exit Ticket Draft

- One proof I created today: pending until end-of-day exit ticket
- One risk I now understand: If the policy data is wrong, an agent may answer from unmanaged or unauthorized data and leadership may trust a metric that cannot be defended.
- One question I want answered tomorrow: pending learner question


## Ship Review Summary

Evidence folder: day-01-evidence
Main Aritfact: learning-spec.md
Notebook: day-01-profile-insurance-policy.ipynb


### What is Ready

- The Artifact aexists.
- The datset pasth us recorded.
- The verification evidence is visible
- The risk / limitation is written

### Business Value

RToday we convert a raw insurance file into a named, inopectable data product starting point.


### Not yet Production Ready because

Today proves basic profiling and contract thinking; it does not proove full quality, lineage, access control is not there, finally production readiness is also not present