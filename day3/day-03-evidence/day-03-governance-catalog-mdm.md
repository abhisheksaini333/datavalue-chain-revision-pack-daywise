# Day 3 -  Data quality, Governance, Catalog and MDM Evidence


## 1. Dataset and Lane (Insurance)

- Lane: Insurance
- Primary Dataset :  day-03-evidence/source-extract/insurance policy data.xlsx
- Evidence folder : day-03-evidence

## 2. Business Decision

A data steward must decide wether policy / customer records are clean, classified, goverbed and safe enough to publish as trusted insurance data product.

## 3. Quality checks and data contract

Done in the Notebook

## 4. Observability and incident note

| Monitor | Signal to watch | Example Evidence | Action if breached |
|------- | ------ | ------ | ------ |
| Freshness | dataset did not arrive by SLA | latest file timestamp or date column check | notify owner; do not pusblish |
| Volumne | Row count changes unexpectedly | row count compared to previous run | diagnose source / load issue |
| Schema | column added / removed / renamed | current columns to the contract | open contract change review |
| Distribution | Status / category / value pattern shifted | top values or null distribution | ispect business reason |


### AI-Driven Quality Monitoring Note

- AI can summarize anomalies and propose possible causes.
- AI must cite the signal it used.
- AI must not silenlty change contracts, policies or golden records
- Risky remediation requires human approval.


## 5. Catalog, glossary, classification and access policy

### 5.1 Catalog Entry

| Field | Value |
| --- | --- |
| Catalog asset name | `insurance_policy_governed_product` |
| Four-level namespace | `catalog.insurance.policy.governed_policy_document` |
| Domain | Insurance |
| Owner | Data product owner / data steward |
| Technical source | `day-03-evidence/source-extract/insurance policy data.xlsx` |
| Business purpose | Trusted policy/customer/claim master for operation and governed AI use |
| Quality | Draft; checks cpatured today; production thresholds need owner approval |
| Lineage status | Source to governed product documented; column-level lineage draft captured |


### 5.2 Business Glossary Entry

| Term | Defintion | Owner | Example use | AI Serving note |
| -- | -- | -- | -- | -- |
| Policyholder | Person or entity that owns or is covered by an insurance policy | Insurance data steward | claims, underwriting, customer service | AI must not expose PII unless policy permits |
| Golden customer record | Approved best representation of on real-world customer/entity | MDM steward | Identity resolution and de-duplication | Agent may propose; steward approves the merge |
| Claim amount | Monetry value associated with a claim | Claims owner | claims analytics and fraud checks | Definition and currency must be confirmed |


### 5.3 PII Classification

| Column or placeholder | Classification | Reason | Default access policy |
| --- | --- | --- | --- | 
| customer / person / name column | PII | Identifies a person | Mask unless authorized | 
| phone / email / address column | PII | contact information | Mask unless authorized | 
| date of birth / national id column | sensitive PII | Strong identity attribute | Restricted; do not expose to AI by default | 
| policy/ claim id | confidential business data | links to insurance transaction | Allowed only for approved |


### 5.4 Access Policy Draft

| User or Agent | Allowed | Not Allowed | Approval matrix |
| --- | --- | --- | --- |
| Claims analyst | masked policy/customer view | Raw sensitive PII | Request steward approval |
| Data steward | Full view for governance | Bulk export without reason | Audit required |
| AI Assistant | Aggreagted or masked evidenc only | RAW PII, deletion, merge approval | Human approval needed |
| MDM merge agent | Propose / match / merge candidates | Execute merge independently | Steward approval required | 


### 5.5 Governance Platform Vocabulary Map

| Term / Tool  | Plain meaning | what to remember | 
| --- | --- | --- |
| Unity Catalog | Lakehouse catalog nd governance plane | controls tables, permissions, lineage and AI / data assests in databricks style environments |
| Collibra / Alation / Atlan | Enterprise data catalog and governance platforms | glossary, lineage, classification, ownership, stewardship workflows | 
| Immuta / Privacera | Policy-as-a-code and access governance platforms | row/column controls, masking, purpose-based access, policy enforcement | 
| MCP service / agent / skills governance | Tool governance for AI systems | controls which tool calls are allowed, denioed, masked or escalated |



## 6. Lineage and Privacy / deletion proof

### 6.1 Column-level lineage draft

| source column | transformation | target field | used by | Risk if wrong |
| ----- | ---- | ----- | ---- | ---- |
| policy / customner id | standardized / select | golden customer id candidate | MDM matching | wrong customer treatment | 
| name / contact field | classified and possibly masked | governed customer attribute | steward / AI masked context | PII leakage |
| policy status / date field | validated and copy | governed attribute | claims or analytics | wrong operational decision |



### 6.2 Privacy / deletion workflow

| Step | Evidence required | 
| --- | --- | 
| Verify identity and scope | request id, perdon, entity, legal basis | 
| find source of record | source system /table/ file and owner |
| trace downstream lineage | reports, derived tables, features, vector indexes, exports | 
| decide action  | delete, mask, retain with legal reason, or escalate |
| execute the approved action | system log / ticket /query result |
| save audit proof | timestamp, approver, scope, outcome, limitation |


### 6.3 Privacy compliance Note

| Regulation idea | plain english meaning | evidence |
| ---- | ---- | ---- |
| DPDP-style personal data protection  | know perosnal data purpose, protect it and act responsibly | PII classification and access policy |
| GDPR right to erasure | deletions request can be made where legally applicable | deletion workflow and lineage trace | 
| source-of-record lineage | know where the authoritative value lives | source and downstream lineage tables |
| AUDITED deletion | deletion / masking must leave proof | request ID, approver, action and timestamp |


## 7. Agentic MDM Golden Record

| Concept | Meaning | Insurance example | 
| --- | --- | ---- |
| Entity resolution | decide wether records refer to the same real-world person / entity | `A. Sharma` and `Abhishek Sharma` may be the same policyholder |
| Golden record | Approved best version of the entity | one trusted customer / policyholder record |
| Survivorship rule | Rule for which source value wins | verified policy admin phone no. which wins free text claim note | 
| Stewardship | Human review and approval for risky merges | data steward approves or rejects a candidate | 
| Confidence threshold | Score that determines review path | High score goes to steward approval; low score goes to manual approval queue | 

## 8. GCP Translation

| Responsibility | GCP Translation | Evidence to Collect | Control before trust |
| --- | --- | --- | --- |
| Quality checks | BigQuery SQL Validation rules | query result / failig rows | pass / fail evidence |
| PII Classification | BigQuery policy tags / data governance tags | tag name and column mapping | do no expose raw PII data |
| Row / column Access | IAM, policy tags, data policies | access policy note | least privilege |
| catalog / glossary/lineage | Data catalog concept or coatalog note | asset entry and lineage notes | owner/steward review |
| golden record | Cloud SQL or BQ tables which are governed | record or logs | steward approval |
| Audit | cloud audit logs / logs explorer | audit event or note | reatain proof and limitation |
| Secrets | Secret Manager | Secret name , but never the value | no secret in code / chats / screenshots |

## 9. AI Assistance

- Tool used: codex / claude 
- Prompt: 
        I am teaching Day 3: data quality, governance, catalog and MDM.
        Dataset lane: Insurance.
        Visible columns from the dataset are pasted below. Do no invent columns.

        Columns:
        'Name', 'Date', 'Shift Timing', 'Team Name', 'Activity', 'Job Number', 'policy category', 'Job Type', 'Fund', 'Sub Fund', 'Final Action', 'Average handling time (minutes)', 'country'

        Create a small quality-and-contract draft with:
        1. four quality rules mapped to completeness, validity, timeliness and distribution,
        2. likely PII columns and why they are sensitive,
        3. one catalog glossary term,
        4. one lineage statement,
        5. one human approval point.

        Use plain English. mark uncertain items as "needs business confirmation".

- What we accepted: 
    Quality Rules, partial PII, Partial glossary, lineage, human approval points

- What we rejected or corrected: 
    Some PII classification, some glossary items

## 10. Ship review

To be completed during the lab / end of the day.