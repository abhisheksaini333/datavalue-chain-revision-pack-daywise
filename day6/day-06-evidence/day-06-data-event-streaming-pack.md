# Real-Time And Streaming Data Products



## Lane and Dataset
- Lane: Logistics
- Primary Dataset : day-06-evidence/source_extract/industry_datasets-main-Miscellaneous/Miscellaneous/Delivery_Logistics.csv
- Fallback Dataset : day-06-evidence/source_extract/industry_datasets-main-Miscellaneous/Miscellaneous/Delivery truck trip data.xlsx
- Evidence Folder : day-06-evidence


## Event Contract

| Fields | Meaning | Required ? | Example |
|--- | --- | --- | --- |
| event_id | Idempotency and replay key | yes | EVT-001 |
| shipment_id | Business Entity | yes | SHIP-001 |
| event_type | pickup, location_update, delay, delivered | yes | delay |
| event_time | when the business event happened | yes | 2026-08-03T10:05:00z |
| processing_time | When our system processed it | yes | 2026-08-03T10:06:00z | 
| source_system | where the event came from | yes | carrier_api |
| payload_status | Raw status or reason | yes | weather_delay |


## Stream to Table Proof

event sample, row counts, lag metric, duplicate check, late event check, or dead-letter row

| Source | Processor | Table Target | Proof |
| ---- | --- | ---- | ---- |
| Shipment events | microbatch/flink/spark | gold shipment status | printed gold rows and SLO metrics |


lakehouse table target: classroom proof used microbatch output; production target would be Iceberg/delat/bigquery table with checkpoint/replay controls.


## Freshness SLO

- Product : logistics control tower gold shipment status
- SLO : 95 percent of valid events available within 5 minutes
- Lag Formula : `processing_time - event_time`
- Breach rule : 
- Alert Owner :
- Freshness Breach : at least one valid event exceeded the 5 minute freshness target, so the agent may summarize the risk but cannot take any action


## Event Driven Agent Gate

- Signal the agent can read:
- Agent recommendation :
- Human Approval needed before :
- What AI is not allowed to do:

The agent may draft a recommendation; it may not auto-escalate, re-route, refund, or notify a customer without policy or human approval.


## Reiability, Replay and Cost

- Idempotency Key :  `event_id`
- Dead-letter rule: missing required fileds or duplicate event goes to review path
- Replay rule: replay by event_time window using idempotency key to avoid duplicate gold output
- Exactly-once or duplicate-control note: transactional / checkpointed broker-processor-sink guearantees
- small-file / compaction note: need to keep the small file count under check
- const control note: choose 5 minute SLO before paying for sub second always-on processing
- Streaming quality control: required event fields checked before gold table serving
- transformation control: event-time slice can be run or backfilled.
- small-files control: production design needs compaction when low latency writes create tiny files
- cost control : choose latency target intentionally; do not run always-on comoute if near realtime is suffcient.

## GCP Translation

- Pub/Sub responsibility:
- Cloud Run functions / Cloud functions responsibility:
- BigQuery / Storage Write API responsibility:
- Logging and Monitoring responsibility:


## Tool Responsibility Map

| Layer | Job |
| --- | ---- |
| Topic / event bus | Recieve events and decouple producers from consumers |
| Processor | Apply time, state, joins, validation and windows |
| Lakehouse table | Store fresh, goverend, queryable state |
| Observability | Prove lag, freshness, failures and cost |
| Agent gate | Allow recommendations only from trusted sources |


## Hackathon Problem Statement