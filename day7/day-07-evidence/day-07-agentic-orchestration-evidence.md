# Day 7 Agentic Orchestration Evidence

## 1. Incident

Lane: Insurance
Incident: claims feed shcema drift
Detected symptom:
Business Impact:

## 2. Agent Roles

| Role           | Responsibility                              | Must not do          |
| -------------- | ------------------------------------------- | -------------------- |
| Monitor        | Detect failure, freshness breach or anomaly | change data          |
| Diagnoser      | Explain likely cause using evidence         | Execute repair       |
| Planner        | Propose a repai plan and authority level    | Approve own plan     |
| Fixer          | Prepare or execute allowed repair           | Bypass gate          |
| Human approver | Approve risky or irreversible action        | Skip evidence        |
| Verifier       | Test result and close incident              | Hide failed evidence |

## 3. Graguated Authority

| Levels             | Meaning                             | Example action          | Allowed today       |
| ------------------ | ----------------------------------- | ----------------------- | ------------------- |
| observe_only       | Record and explain                  | summarise a failed task | yes                 |
| suggestion_only    | Draft recommendation                | propose retry           | yes                 |
| approval_required  | wait before action                  | schema approval change  | yes                 |
| limited_auto       | Execute low-risk reversible actions | retry a failed job      | demo only           |
| approved_execution | Execute after policy and proof      | run approved DAG/tool   | no production claim |

## 4. Decision Log

| Step | Agent          | Evidence                                                   | Decision          | Authority         | Approved by       |
| ---- | -------------- | ---------------------------------------------------------- | ----------------- | ----------------- | ----------------- |
| 1    | monitor        | claims feed schema drift simulated                         | incident opened   | observe_only      | not required      |
| 2    | planner        | claim_amount missing; amount_paid present; confidence 0.72 | wait for approval | approval_required | not yet           |
| 3    | fixer          | approval missing                                           | do not execute    | blocked           | not approved      |
| 4    | human_approver | field meaning confirmed                                    | approved          | approval_required | claims_data_owner |
| 5    | verifier       | required columns present; duplicate count 0                | close incident    | not required      |                   |

## 5. Tool Boundary

| Tool    | Allowed Call                                | Bloacked call                            | Evidence |
| ------- | ------------------------------------------- | ---------------------------------------- | -------- |
| Airflow | inspect DAG status, trigger approved reties | create unknown DAG                       |          |
| dbt     | run names tests, inspect failures           | edit the production model without review |          |
| Catalog | Execute after policy and prof               | overwrite schema without approval        |          |

## 6. Incident Memory

Similiar incident:
Useful past fix:
why it applies:
wht it may not apply:

### 6.1 Incident Memory Entry

| Field                  | value                                                             |
| ---------------------- | ----------------------------------------------------------------- |
| Incident pattern       | required column missing after source feed change                  |
| past fix               | map renamed field in staging transform                            |
| current evidence match | column`amount_paid` apeears where `claim_amount` was expected |
| Risk                   | fields may not have identical bnusiness meaning                   |
| Required control       | data-owner approval before schema changing action                 |
| Verification           | required column test and duplicate test                           |

## 7. Trace summary

Trace ID: INC-CLAIMS-007
Total steps: 7
Human approval required: yes
Final state: verified

## 8. Cloud transformation

VM Proof:
GCP Equivalent:
Security boundary:
Observability boundary:

## 9. Autonomy Decision

|                         | Result                                       |
| ----------------------- | -------------------------------------------- |
| confidence threshold    | 0.85 required for low-risk auto action       |
| Current confidence      | 0.72                                         |
| Risk type               | schema changing action                       |
| Reversible ?            | partially, but downstream meaning may change |
| Decision ?              | human approval required                      |
| Auo-execution allowed ? | no                                           |



## 10. MCP-Style Tool Schema

Tool Name: `trigger_approved_airflow_retry`
Purpose: retry a known DAG run after incident review.
Inputs: 
- `incident_id`
- `dag_id`
- `run_id`
- `idempotency_key`
Blocked:
- creating new DAGs
- editing DAG code
- triggering schema-changing DAGs without approval
- audit event ID


## 11. dbt verification contract

| Test | Why it matters | Passing condition | 
| ---- | ----- | ----- |
| not_null_claim_id | incident should not create blank claim ids | zero failing rows |
| accepted_values_claim_status | status should stay controlled | zero invalid statuses |
| required_claim_amount | schema repair should restore expected field | zero missing fields |
| duplicate_claim_id | retry should not duplicate claims | duplicate count equals 0 |


## 10. limitations, if any
