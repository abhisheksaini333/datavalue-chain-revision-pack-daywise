# Day 5 - Productionisation, DataOps, Security, Cost and Capstone Brief

## 1. Dataset And Lane

- Lane: Insurance
- Primary Dataset: day-05-evidence/source-extract/insurance_cash_application.csv
- Evidence Folder: day-05-evidence
- Shape observed by smoke test: 1200 rows, 30 columns
- Real columns used in this pack (verified from the file header, not invented):
  `Transaction_ID`, `Policy_Number`, `Payment_Date`, `Posting_Date`,
  `Amount_Received`, `Applied_Amount`, `Unapplied_Amount`,
  `Match_Confidence_%`, `TAT_Hours`, `Accuracy_%`, `Accuracy_Flag`,
  `Status`, `Exception_Code`, `Applied_By`, `Reviewed_By`,
  `Created_Timestamp`, `Updated_Timestamp`
- Sensitive column to protect: `Policyholder_Name` (personal data)

Placeholders still open (marked deliberately, to be confirmed with the business):
- `<PLACEHOLDER: named data product owner>`
- `<PLACEHOLDER: named release approver>`
- `<PLACEHOLDER: agreed monthly cost cap in USD>`
- `<PLACEHOLDER: target GCP project / environment name>`

## 2. Simple Explanation

Cash application is the step where money received from policyholders is matched to
the right policy and posted to the ledger. Today the proof of that process is a CSV
extract plus a script. That is fine for a demo, but a business cannot depend on it,
because nobody can tell whether it ran, whether it ran on good data, or who is
accountable when it breaks.

Productionisation means wrapping the same logic in four things a business can rely on:
a health signal (is the service up), a readiness gate (is it safe to serve),
a published service promise (freshness, reliability, owner), and a cost boundary.
The service already exposes exactly these at `/health`, `/ready`, `/slo` and `/cost`
in [app.py](day-05-evidence/day-05-productionisation-proof/app.py), and it refuses to
report ready unless the smoke test has passed. That refusal is the point: the quality
check controls the release, rather than a person remembering to look.

Security and cost are part of readiness, not extras. `Policyholder_Name` is personal
data, so it must not appear in logs or in anything sent to a model. Cost must have a
cap agreed before production, otherwise a background job can spend money quietly.

## Business Decision

Promote the insurance cash-application check from a one-off script to a gated,
owned service, and treat "ready" as a machine-verified state rather than an opinion.

Decision rule for go-live: deploy only when the smoke test status is `PASS`, the
readiness endpoint returns HTTP 200, the personal-data column is confirmed absent
from logs, and a named human has signed the release. Any one failing means no deploy.

## Practical Proof

Practical steps (in order):

1. Confirm the source extract exists and record its real shape (1200 rows, 30 columns).
   Do not assume columns; read the header.
2. Run the smoke test and let it write its verdict to
   [logs/smoke_test_result.json](day-05-evidence/day-05-productionisation-proof/logs/smoke_test_result.json).
   Current recorded verdict: `PASS`, `production_decision: ready_for_demo_packaging`.
3. Start the service and call `/health`. Expect `status: alive`.
4. Call `/ready`. Expect HTTP 200 and `ready: true` because the smoke result is `PASS`.
5. Prove the gate actually blocks, using the built-in override:
   `GET /ready?smoke=fail`. Expect HTTP 503 and reason
   `blocked_until_smoke_test_passes`. A gate that has never been seen to fail is
   not evidence of a gate.
6. Call `/slo` and record the published promise: freshness 24 hours, reliability 99.0%,
   quality gate `smoke_test_status_must_be_PASS`, owner `data_product_owner`.
7. Call `/cost` and record the estimate and that a hard cap is required before
   production. Replace the demo figure with `<PLACEHOLDER: agreed monthly cost cap in USD>`
   once the business confirms it.
8. Call `/agent-card`. Confirm `secret_loaded_without_displaying_value` reflects whether
   `DEMO_SECRET` is set, and that the secret value itself is never returned. Confirm the
   blocked actions include "approve its own release".
9. Run a data-quality read on the real columns only: count rows where `Status` is not
   `Applied`, where `Unapplied_Amount` is greater than zero, where `Accuracy_Flag` is
   not `Pass`, and where `Match_Confidence_%` is below the review threshold. These are
   the exception population a supervisor must work.
10. Check the personal-data control: grep the service logs and the smoke result file
    for `Policyholder_Name` values and confirm none are present.

Verification evidence to collect:

| # | Evidence | Where it comes from | Expected |
|---|---|---|---|
| 1 | Dataset shape and column list | smoke test result JSON | 1200 rows, 30 columns |
| 2 | Smoke test verdict with UTC timestamp | smoke test result JSON | `status: PASS` |
| 3 | `/health` response | service call | `status: alive` |
| 4 | `/ready` response, pass case | service call | HTTP 200, `ready: true` |
| 5 | `/ready?smoke=fail` response | service call | HTTP 503, `blocked_until_smoke_test_passes` |
| 6 | `/slo` response | service call | freshness 24h, reliability 99.0%, named owner |
| 7 | `/cost` response | service call | estimate plus `hard_cap_required_before_production: true` |
| 8 | `/agent-card` response | service call | secret presence flag only, no secret value |
| 9 | Exception counts by `Status`, `Exception_Code`, `Accuracy_Flag`, `Unapplied_Amount` | query over the CSV | counts recorded, reconciled to 1200 |
| 10 | Log scan for `Policyholder_Name` | grep over logs | zero hits |
| 11 | Signed release note naming the approver | human step | `<PLACEHOLDER: named release approver>` |

Save endpoint responses as files under `day-05-evidence/day-05-productionisation-proof/logs/`
so the evidence is re-readable later, not just seen once on a terminal.

## AI Assistance

Permitted uses, matching the allowed actions already declared in `/agent-card`:
summarise readiness output, explain which check failed and why, and draft release notes.

Not permitted: changing access policy, deleting records, or approving its own release.
Nothing containing `Policyholder_Name` may be sent to a model; use `Policy_Number` or
`Transaction_ID` as the reference instead, since those identify the record without
naming the person.

## Risk and Control

Risk: the readiness gate can report ready on stale evidence. `/ready` reads a saved
smoke-test file and only checks that `status` is `PASS`. It does not check
`timestamp_utc`. So if the extract is refreshed but the smoke test is not re-run, or
the smoke test fails to write, the service keeps serving a `PASS` from an earlier run
and the published 24-hour freshness promise is silently broken.

Control: compare `timestamp_utc` in the smoke result against the 24-hour freshness SLO
and fail readiness when the result is older than that window, so a missing rerun turns
into a visible 503 rather than a false green.

## GCP Translation

- CSV extract in `source-extract/` becomes a Cloud Storage landing bucket, then a
  BigQuery table in `<PLACEHOLDER: target GCP project / environment name>`.
- Flask service becomes a Cloud Run service, with `/health` as the liveness probe and
  `/ready` as the readiness probe, so a failed smoke test stops traffic automatically.
- Smoke test becomes a scheduled job whose result is the release gate.
- `DEMO_SECRET` becomes a Secret Manager secret injected at runtime, never printed.
- `/cost` becomes a billing budget with an alert at the agreed cap.
- `Policyholder_Name` is restricted by column-level access control so only the
  entitled role can read it.

## Human Approval Point

Production deployment requires explicit sign-off from
`<PLACEHOLDER: named release approver>`, who must have seen evidence items 2, 5 and 10
(smoke verdict, the gate proven to block, and the zero-hit personal-data log scan).
The agent may prepare the release note but must not approve it, which is already
enforced by `approve its own release` being listed as a blocked action.


## Release Gate

| Gate | Evidence pasted | Pass / Fail | Owner | If fails, what next ? |
| --- | --- | --- | --- | ---| 
| Dateset Exists | `smoke_test_result.json` shows dataset path | passed | data owner | Block packaging | 
| Row count positive | `row_count` greater than zero | passed | data engineer | Block packaging | 
| Business columns present | `smaple_columns` contains business like records | passed | data analyst | inspect schema |
| Service health | `/health` endpoint | passed | Platform servivce | Restart service |
| forced failure works | `/ready` endpoint | passed | DataOps owner | keep this gate always before deployment |
| cost note | `/cost` endpoint | passed | FinOps | Add budget before production | 
| Agent limits | `/agent-card` returned allowed and blocked actions | passed | Governance owner | Add human approval |


## Misconceptions

| Misconception | Better understanding | proof |
| --- | --- | --- |
| The tool produced an output, so it is correct | output is only a signal | verification evidence needed |
| AI suggested a fix / code, so it is safe | AI draft needs inspection  | Human review and audit |
| The dataset opened, so it is governed | open file is not governance | Owner, policy, lineage |


## Exit ticket

- Gate proven in both directions: pass gives 200, forced fail gives 503.
- Service promise published with a named owner and a quality gate.
- Cost has an owner and requires a hard cap before production.
- Personal data confirmed absent from logs.
- Open items: the four placeholders above, and the freshness check named in
  Risk and Control.
