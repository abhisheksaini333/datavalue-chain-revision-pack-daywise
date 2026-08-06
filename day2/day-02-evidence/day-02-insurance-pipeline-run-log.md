# Day 2 - Agentic Data Engineering And Pipelines Evidence

Today We are going to prove:

- bronze / silver / gold outputs failed test evidence, diagnosis, approved fix, rerun log

## Topics:

- Orchestration backbone - data arrival
- Transformation backbone - cleaning the data
- CDC and incremental processing - checking data
- Pipeline Observability - governing the data
- NL -> pipeline code - serving and business decisions

## The hands-on expectations:

1. Build a model / test pair for trnasactions or claims.
2. Use AI to draft a model plus tests, then inspect and correct it.
3. Simulate schema changes and run monitor  - diagnose - proposed remediations.

## dbt-style Model Plan

| File                      | Purpose                                  | Key rule                                    |
| ------------------------- | ---------------------------------------- | ------------------------------------------- |
| `models/stg_claims.sql` | Clean raw claims into types staging rows | keep one row per source claim               |
| `models/gold_claims.sq` | Publish business-ready claims metrics    | Aggregate only after tests pass             |
| `models/schema.yml`     | Store tests and descriptions             | Fail on missing claim id and invalid amount |

### Versioned Model Note

Current model version: `v0.1`

Change made today: initial claims staging anf gold model skeleton

Reviewer:  inteructor / class review

### Incident Log

| Phase    | Evidence                                            |
| -------- | --------------------------------------------------- |
| Perceive | failed test or schema mismatch observed             |
| Reason   | suspected root cause written in plain English       |
| Act      | propsed fix only; no direct unsafe production write |
| Learn    | decision saved to incident memory                   |

### Pipeline Memory Record

Filled from the **negative-control drill** in notebook section 5, not from a real production
incident. Labelled as a drill on purpose so it is not mistaken for live evidence.

Incident signature: `silver_claims` / renamed amount column + nulls in `Age`

Failed check: schema test (`missing_columns: ['Claim_Amount']`, `unexpected_columns: ['ClaimAmount']`)
and null test (`Claim_Amount: COLUMN MISSING`, `Age: 25`)

Proposed fix: map the upstream `ClaimAmount` back to the contracted name `Claim_Amount` at the bronze
read, then re-run silver and both tests. Do not backfill the 25 null `Age` values - report them.

Confidence: high on the rename (the contract names the column). Low on the nulls - cause unknown
until the data owner confirms whether the source sent blanks.

Human approver: ______________________  (UNSIGNED - this is the approval gate, see section 9.5)

Outcome after rerun: not yet run - blocked pending the approval above.

## 1. Dataset

Locked Lane: Insurance

Primary Dataset:  Insurance Claims and Policy Data.zip

Fallback dataset:

Datset used today:  Insurance Claims and Policy Data.zip

Evidence Folder:  day-02-evidence

## 2. Business Decisions

A claims operations manager must decide wether the daily insurabce claims poipeine can be trusted after a schema or quality failiure

Decision Owner: Claims data engineering lead

Action this decision supports: Approve a rerun only after the pipeline failure is diagnosed, fixed, tested, and logged.

## 3. Why this matters

Today we turn a fragile data load into a tested pipeline with diagnosis and approval evidence.

## 4. Risk if wrong:

If a pipeline failure is treadted as only a rerun problem, the same bad data may be published again with no diagnosis.

## 5. Verification Evidence

Source file: `day-02-evidence/source_extract/insurance_dataset.csv` (reachable, `exists: True`)

- **Row count:** 13,000 data rows (13,001 lines including header)
- **Column list (7 real columns, verified from the file):** `Age`, `Gender`, `Income`,
  `Marital_Status`, `Education`, `Occupation`, `Claim_Amount`
- **Quality / test result:** schema test PASS; null test PASS (`Claim_Amount` 0 nulls, `Age` 0 nulls,
  13,000 rows checked). Negative control: both tests FAIL as expected.
- **AI-generated artifact:** `day-02-bronze-silver-gold-pipeline.ipynb` (drafted, then inspected and
  corrected - see the placeholder note below)
- **Output saved:** gold table, 5 rows, one per `Occupation`
- **Log reference:** notebook cell output, sections 1-5

### Placeholder register - columns that do NOT exist in this extract

| Placeholder                | Why it is a placeholder                                   | What it blocks                                                                   |
| -------------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `PLACEHOLDER_claim_id`   | The extract has no claim id and no unique key of any kind | The uniqueness test; the "one row per source claim" rule in the model plan above |
| `PLACEHOLDER_claim_date` | The extract has no date column                            | Incremental / CDC processing and any watermark                                   |

Correction made to the drafted model plan: the plan in this log assumes a claim id and a claim date.
Neither is present in the extract. Row identity is currently **positional only** (`_bronze_row_num`).
Both placeholders are open questions for the data owner.

### Layer and test summary

| Layer  | Grain                                                    | Result                                       |
| ------ | -------------------------------------------------------- | -------------------------------------------- |
| Bronze | One row per source line, all text + 3`_` audit columns | 13,000 rows, 10 columns                      |
| Silver | One row per bronze row, declared numerics cast           | 13,000 rows, row-count assert held           |
| Gold   | One row per`Occupation`                                | 5 rows, built only because both tests passed |

Test 1 (schema): expected 7 columns present, in order, with expected type family.
Test 2 (null): zero nulls in `Claim_Amount` and `Age`.

## 6. Build Evidence

1. **What I built:** a bronze -> silver -> gold skeleton in
   `day-02-bronze-silver-gold-pipeline.ipynb` with one schema test, one null test, a gate that
   refuses to build gold when a test fails, and a negative-control cell that breaks a copy of silver
   on purpose.
2. **What I ran:** all notebook cells top to bottom against `insurance_dataset.csv`.
3. **What I observed:** both tests passed on the clean extract, so gold was built (5 rows, one per
   `Occupation`). The negative control renamed `Claim_Amount` to `ClaimAmount` and nulled 25 `Age`
   values; the schema test reported `missing_columns: ['Claim_Amount']` and
   `unexpected_columns: ['ClaimAmount']`, and the null test reported
   `Claim_Amount: COLUMN MISSING, Age: 25`. That confirms the tests can actually fail, not just pass.

## 7. What can still go wrong

**Main risk if the gold output is wrong:** the tests can pass while gold is still wrong, because
there is no `PLACEHOLDER_claim_id` to test uniqueness against. If the extract ever contains
duplicated claim rows, the schema is intact and no nulls appear, so both tests go green - but
`total_claim_amount` per `Occupation` is inflated by the duplicates. The claims manager would
approve a rerun on green tests and publish overstated claim totals. Mitigation: obtain a real claim
id from the data owner and add a uniqueness test before this skeleton is trusted for a decision.

Also open:

- No date column, so nothing here proves the load is current rather than a stale re-read.
- `Age` reaches a max of 102.4 as a decimal, which is implausible for a real age and suggests the
  extract is synthetic or derived. No range test covers this yet.
- `Occupation` is dominated by one value (`CEO`, 10,575 of 13,000 rows), so per-occupation averages
  for the other four groups rest on small counts (581-633 rows each).

## 8. GCP Translations

Today's GCP mapping: BigQuery transformation pipeline and Could Functions trigger concept.

In GCP this would be mapped as follows:

- Storage / query / staate / serving service: BigQuery transformation pipeline and Could Functions trigger concept.
- Console service to mention:  BigQuery, Cloud Functions
- Secret or access-control boudary:  Secret Manager / IAM Concept, these must protect credentials and access
- Audit or monitoring evidence:  audit log, query history, service log, or saved screenshots depending on the data

## 9. Draft Walkthrough

Teaching companion to `day-02-bronze-silver-gold-pipeline.ipynb`. Draft only.

### 9.1 Simple explanation

Keep three copies of the data, each with one job.

- **Bronze** is exactly what arrived, read as text, nothing corrected. It is the sealed evidence bag.
  You can always prove what the source actually said.
- **Silver** is the same 13,000 rows, typed and trimmed so they are usable. Same grain as bronze -
  no rows added, none dropped.
- **Gold** is the small summary the claims manager reads: one row per `Occupation`.

The two tests sit **between silver and gold** and act as a gate. If either fails, gold is not
rebuilt, and yesterday's gold stays published rather than being overwritten with something wrong.
A failure becomes a written diagnosis, not a silent bad number.

One deliberate choice worth explaining: a bad number becomes a **null**, not a crash
(`errors="coerce"`). A crash tells the claims manager nothing. A null gets counted by the null test
and reported as "25 rows affected", which is something they can act on.

### 9.2 Practical steps

1. Open the notebook and run the setup cell. Confirm `exists: True`.
2. Run bronze. Read the printed column list and check it against the 7 real names. Change nothing here.
3. Run silver. Confirm 13,000 rows and that the row-count assert did not raise.
4. Run the tests. Read the printed dicts, not just PASS/FAIL - the dicts are the evidence.
5. Run gold only if both tests passed. Confirm 5 rows, one per `Occupation`.
6. Run the negative control in section 5. Confirm `all tests passed: False`. This proves the tests
   can fail; without it a green run means nothing.
7. Copy the printed numbers into section 5 and section 6 of this log.
8. Stop at the approval point in 9.5 before treating any rerun as trustworthy.

### 9.3 Verification evidence to collect

Capture the actual printed value, not the expected one. Full 12-row checklist is in notebook
section 6; the minimum set for this log is:

| Evidence                       | Expected                                       | Captured from  |
| ------------------------------ | ---------------------------------------------- | -------------- |
| Source reachable               | `exists: True`                               | setup cell     |
| Bronze row count               | 13,000                                         | bronze cell    |
| Column list                    | the 7 real names + 3`_` audit columns        | bronze cell    |
| Silver row count equals bronze | 13,000, no assert raised                       | silver cell    |
| Schema test dict               | `passed: True`, empty missing/unexpected     | test cell      |
| Null test dict                 | `passed: True`, all counts 0, 13,000 checked | test cell      |
| Gold grain                     | 5 rows, one per`Occupation`                  | gold cell      |
| Negative control               | `all tests passed: False`                    | section 5      |
| Placeholders still marked      | no`PLACEHOLDER_` used as a real field        | whole notebook |

### 9.4 One risk

**Green tests do not mean correct gold.** With no `PLACEHOLDER_claim_id`, there is no uniqueness
test. If the extract ever contains duplicated claim rows, the schema is intact and no nulls appear,
so both tests pass - while `total_claim_amount` per `Occupation` is silently inflated by the
duplicates. The claims manager approves a rerun on green tests and publishes overstated claim
totals. Mitigation: get a real claim id from the data owner and add a uniqueness test before this
skeleton is trusted for a decision.

### 9.5 One human approval point

**Gate: the claims data engineering lead must sign off before a rerun is allowed to publish gold.**

| Field               | Detail                                                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Who approves        | Claims data engineering lead (named in section 2 as decision owner)                                                            |
| When                | After a test fails and a fix is proposed; before gold is rebuilt                                                               |
| What they are shown | the failed test dict, the plain-English root cause, the proposed fix, and the confidence level from the Pipeline Memory Record |
| What they sign      | the`Human approver` line in the Pipeline Memory Record above                                                                 |
| If they decline     | gold is not rebuilt; the previous gold stays published; the incident stays open                                                |

The agent may diagnose and propose. It may not approve its own fix, and it may not write gold on a
failed test. That boundary is the point of the exercise - `Human approver` is currently **unsigned**,
so the drill in the Pipeline Memory Record is correctly still blocked.

## 10. One misconception

| Misconception                              | Better Understanding         | Proof needed           |
| ------------------------------------------ | ---------------------------- | ---------------------- |
| The tool produced output, so it is correct | Output is only a signal      | Verification evidence  |
| AI Suggested it, so it is safe             | AI draft needs inspection    | Human review and Audit |
| The dataset opened, so it is governed      | Open files is not governance | Owner, policy, lineage |

## 11. VM proof Hardening

| Pipeline Step        | Evidence Expected                   | Status                | Control before trust                   |
| -------------------- | ----------------------------------- | --------------------- | -------------------------------------- |
| bronze load          | raw claims rows loaded              | proved in VM          | record row count before transformation |
| silver clean         | cleaned claims table created        | proved in VM          | validate required columns and nulls    |
| gold business output | decision-ready summary created      | proved in VM          | tie output to business decision        |
| monitor              | failure or drift signal captured    | concept + proof note  | signalm does not approve a fix         |
| diagnose             | root cause written in plain English | concept + proof note  | diagnosis must cite the failed check   |
| human approval       | approved / reject decision logged   | concpet + manual gate | the fixer must not approve itself      |

## 12. BigQuery Mapping

| VM Proof Item          | GCP BigQuery Equivalent                | What We saw or will see                                         | Evidence to Collect            |
| ---------------------- | -------------------------------------- | --------------------------------------------------------------- | ------------------------------ |
| Insurance Excel or CSV | BQ Table                               | Dataset`day02_pipeline_demo`, table such as `claims_bronze` | Dataset / Tables / screenshots |
| Bronzed load           | Load job or external table             | Raw claims landing table                                        | Row count with query result    |
| Silver clean           | SQL Transformations                    | `claims_silver` query removes bad/null records                | validation query result        |
| Gold output            | Analytics table / view                 | `claims_gold_summary` for business decision                   | sample output rows             |
| Quality check          | SQL assertion / queries                | count null claim IDs, invalid dates, duplicate keys             | pass / fail result             |
| Run Evidence           | Job history / audit log plus any notes | Job Id, query, text, timestamp                                  | copied job id or screenshots   |

## 13. Claude powered pipeline monitor

Business scenraio:
An insurance claims pipeline loads a raw claims data, cleans them, creates a gold claim summary, and supports claims operations or underwriting decisions.

Failure:
The source file changes `claim_amount` to `amount_claimed`, so the silver transformation fails.

Agent Goal:
Monitor the pipeline, diagnose the failure, propose a safe code or SQL patch, and record the approval decision.

Agent must not:

- Read full raw claims data undless explicitly approved.
- Store secrets in prompts, markdown, screenshots or code.
- Execute a risky patch without human approval.
- Approve its own fix.

| Tool / function name                              | Purpose                                     | Read or write ?        | Approval Needed ? |
| ------------------------------------------------- | ------------------------------------------- | ---------------------- | ----------------- |
| `get_airflow_dag_status(dag_id)`                | Read DAG Health, latest run and failed task | read                   | no                |
| `get_dbt_test_failures(job_id)`                 | Read failed tests and compiled SQL path     | read                   | no                |
| `get_schema_diff(source_name)`                  | compare previous and current schemas        | read                   | no                |
| `propose_sql_patch(error_summary, schema_diff)` | Draft a SQL or dbt model patch              | draft only             | no                |
| `open_human_approval_request(patch_summary)`    | Ask owner to approve or reject              | write decision request | yes               |
| `trigger_airflow_dag(dag_id, config)`           | Start a DAG run after approval              | Write execution        | yes               |
| `write_pipeline_memory(incident_summary)`       | Save failure, fix and decision              | write memory           | yes               |

#### Sample function-calling payload:

{
  "tool_name": "get_schema_diff",
  "arguments": {
    "source_name": "insurance_claims_source",
    "previous_schema_ref": "last_successful_run",
    "current_schema_ref": "latest_landing_file"
  }
}

#### Sample Agent Output / Sample claude diagnosis:

Observed Signal:
The Silver claims transformation failed because column `claim_amount` was not found.

Diagnosis:
The latest source schema contains `amount_claimed`. Thus may be a rename, but business meaning must be confimred before mapping

Proposed Patch:
Update the silver trsnasformation to map `amount_claimed` as `claim_amount` only after business owner approval.

Risk:
if `amount_claimed` has a different definition, gold claim totals may be wring.

Approval Needed:
Yes. Hiuman approval is required before changing schema mapping and rerunning the DAG.

## 14. Agent design - silver_claims_transform schema-drift monitor

Concise design for the pipeline-monitor agent. Inputs the agent receives, and nothing else:

- **Failed task:** `silver_claims_transform`
- **Error:** `column claim_amount not found`
- **Schema diff:** old column `claim_amount`, new column `amount_claimed`

### 14.1 Diagnosis

An upstream schema change renamed `claim_amount` to `amount_claimed`. The `silver_claims_transform`
model still references the old name, so the transform fails at compile/run. This is **rename drift**,
not missing or corrupt data - confidence is high because the error and the diff point to the same
column. The business meaning of `amount_claimed` is **not yet confirmed** to equal the old
`claim_amount`; that is an open question for the data owner, not an assumption the agent may make.

### 14.2 Proposed SQL / dbt patch (pseudocode)

```sql
-- silver_claims_transform.sql
-- Map the renamed source column back to the contracted name.
-- Keeps the downstream (gold) contract stable so gold models need no edit.
SELECT
    amount_claimed AS claim_amount,   -- was: claim_amount (source renamed upstream)
    ...
FROM {{ ref('bronze_claims') }}
```

```yaml
# staging schema.yml
# rename claim_amount -> amount_claimed in the source/column definition
# re-point not_null / accepted_range tests onto the new column name
```

Alias-not-coerce: preserve the contract name via alias, do not default or null-fill values.

### 14.3 Approval required

**YES.** Schema-affecting change on a monetary (`claim_amount`) column must be reviewed and signed
off by the claims data engineering lead before merge, rerun, or publish. Ties to the approval gate
in section 9.5 and the unsigned `Human approver` line in the Pipeline Memory Record.

### 14.4 Evidence to save

- Failed task name, full error message, and timestamp
- Schema diff (old vs. new column)
- Diagnosis statement plus confidence level (high on rename, meaning unconfirmed)
- Proposed patch diff (SQL + schema.yml)
- Approval decision, approver name, and time
- Post-rerun status and row-count / null-count reconciliation on the amount column

### 14.5 What the agent must NOT do

- Must not auto-apply, merge, rerun, or publish the patch without human approval
- Must not approve its own fix
- Must not modify raw / bronze source data, or drop / backfill rows
- Must not alter monetary values, invent defaults, or mask nulls to force a green run
- Must not disable or edit data-quality tests to make the pipeline pass
- Must not read full raw claims data, use secrets, or access external systems
- Must not act if the error and schema diff disagree - escalate to the data owner instead


## Pipeline Memory, Guardrails and Legacy compatibility

Pipeline memory: we do not firget incidents. Usually they are stored in vectorDBs or searchable knowledge bases store failures, summaries, fixes, approval decisikons, owners, timestamsp and evidence.

Keeping model out of data path: Thsi means the raw data moves from system to syetm e.g. BQ, sbt, airflow, sopark, or any warehouse. The model only sees the small summaries unless approved.

Guardrails for autonomy: Autonomy is all about the levels. e.e Read-onl;y diagbosis is low risk. Chnaging schema is high risk. High risk operations need approvals and decision logs. Any autonomy needs to operate under certain guardrails.

Idempotent and reversible operations: We cannot re-run twice and do duplicate damage. Operations which can be rolled back are reversible in natiure. Agents must have a dry-run loop.

legacy compatibility: A good aent should connect to existing systems without requoring a full restart.