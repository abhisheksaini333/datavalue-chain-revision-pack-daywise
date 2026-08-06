# Day 4 - Serving data to AI and Agents Evidence

## 1. Dataset and Lane

- Lane: Insurance
- Dataset: day-04-evidence/source-extract/Insurance Claims Fraud Data.zip
- Evidence Folder: day-04-evidence

## 2 Business Decision

A claims or underwriting user must decide wether an AI-generated answer about claims/fraud is safe to use, based on governed metrics, permissions, citations and audit evidence


## 3 Semantic Layer Metric definition

### 3.1 Semantic metric definition

| Metric field | Approved definition |
| --- | ---- | 
| Metric name | `claim_approval_rate` |
| business question | what percentage of reviewed claims were approved ? |
| formula | `approved_claims / reviewd_claims` |
| Grain | claim-level, aggregated by allowed dimensions | 
| Approved numerator | claims where final decision / status means approved | 
| Approved denominator | reviewed claims with valid decision / status |
| Allowed dimensions | time perios, regionm claim type, product line | 
| Not allowed by default | raw claim PII, full claim notes, customer-level information | 
| Owner | claims analytics / data steward | 
| limitation | column names and status values must be confirmed from actual dataset | 

### 3.2 Metric Proof

| Metric | Formula | Result | Column used | Need Confirmation ? |
| ---- | --- | --- | ---- | ---- |
| `claim_approval_rate` | approved_claims / reviewed_claims | 0.9497 | claim_status | Yes |

### 32. dataset lOad proof

DONE


## 4 Text-to-SQL guardrail and audit

| Check | Pass ? | Evidence | 
|--- | --- | --- |
| SQL is read-only SELECT | Yes | SQL statement |
| SQL avoids SELECT * | Yes | SQL statment |
| SQL avoids Raw PII | Yes | Output | 
| SQL uses approved metric definition | Yes | compared with the semantic definition | 
| SQL has LIMIT or Aggrergate | Yes | In case of aggregation it is ready with Limit clause |
| SQL refrences only known columns | Yes | SQL Statement | 
| Human review required | Yes | to build trust |


### Allowed query audit

| Field | Value | 
| --- | --- |
| User | claims_analyst_training |
| Question | claim approval rate |
| SQL | Refer the notebook |
| Allowed ? | Yes |
| Reason | No violation |


### Blocked query audit

| Field | Value | 
| --- | --- |
| User | claims_analyst_training |
| Question | claim approval rate |
| SQL | had SELECT * in the query |
| Allowed ? | NO |
| Reason | SELECT * is blocked |


## 5 Permission-aware serving and PII guard

| User | Can view PII ? | Max rows | Serving rule |
| --- | --- | --- | ---- |
| claims_analyst_training | no | 20 | aggregated or masked result only |
| data_steward_training | yes | 20 | full governance view for approved purpose |

## 6 RAG / GraphRAG with citation

### Agentic RAG Answer

| Field | Evidence | 
| ---- | ----- | 
| Question | Can the claims AI answer approval-rate questions and cite the control policy? | 
| Structure evidence used | yes | 
| Document evidence used | no |
| Answer | TOp 2 policies retrieved based on scoring | 
| Citations | Yes | 
| Limitation | proof of concept, productiongrade needs embeddings as well |

## 7 Evaluation, Cost and Latency

## 8 GCP Translation

## 9 AI Assiatnce Used

- Tool Used: Claude
- Prompt Used: 
    We are in Day 4: Servind Data to AI and Agents
    Dataset lane: insurance

    Visible columnas are below. DO not invent columns.

    Columns:
    'TXN_DATE_TIME', 'TRANSACTION_ID', 'CUSTOMER_ID', 'POLICY_NUMBER', 'POLICY_EFF_DT', 'LOSS_DT', 'REPORT_DT', 'INSURANCE_TYPE', 'PREMIUM_AMOUNT', 'CLAIM_AMOUNT', 'CUSTOMER_NAME', 'ADDRESS_LINE1', 'ADDRESS_LINE2', 'CITY', 'STATE', 'POSTAL_CODE', 'SSN', 'MARITAL_STATUS', 'AGE', 'TENURE', 'EMPLOYMENT_STATUS', 'NO_OF_FAMILY_MEMBERS', 'RISK_SEGMENTATION', 'HOUSE_TYPE', 'SOCIAL_CLASS', 'ROUTING_NUMBER', 'ACCT_NUMBER', 'CUSTOMER_EDUCATION_LEVEL', 'CLAIM_STATUS', 'INCIDENT_SEVERITY', 'AUTHORITY_CONTACTED', 'ANY_INJURY', 'POLICE_REPORT_AVAILABLE', 'INCIDENT_STATE', 'INCIDENT_CITY', 'INCIDENT_HOUR_OF_THE_DAY', 'AGENT_ID', 'VENDOR_ID'

    Task:
    Draft a read-only SQL query to answer this question.
    "What is the claim approval rate, using the approved semantic metric definition ?"

    Rules:
    - Select only.
    - No Select *.
    - Include LIMIT where row-level output is returned.
    - Do not include raw PII columns.
    - If Needed columns are uncertain, mark them as placeholders.
    - Return SQL plus a short explaination as risks.

- What I accepted: The result set was accepted
- What I rejected: Couple of low risks highlighted
- AI Assumption that still needs verification.

## 10 Ship review