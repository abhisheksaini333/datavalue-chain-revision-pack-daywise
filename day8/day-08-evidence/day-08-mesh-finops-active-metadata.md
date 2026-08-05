# Day 8 Mesh, FinOps And Active Metadata Evidence

## 1. Data Product

Product name: insurance_policy_product
Domain: Insurance
Owner: insurance_data_owner
Primary consumers: claims_ops, finance_reporting, ai_claims_assistant
Business decision supported: whether the insurance policy product can be published with runtime AI governance and cost controls.

## 2. Mesh Product Contract

| Field          | Type   | Classification | Required | Notes                        |
| -------------- | ------ | -------------- | -------- | ---------------------------- |
| policy_id      | string | identifier     | yes      | stable product key           |
| customer_name  | string | pii            | yes      | restricted for AI raw access |
| email          | string | pii            | yes      | restricted for AI raw access |
| region         | string | residency      | yes      | drives regional policy       |
| premium_amount | number | financial      | yes      | used for finance reporting   |
| policy_status  | string | operational    | yes      | active/lapsed/cancelled      |

## 3. Runtime AI Governance

| Request | Consumer | Purpose | Decision | Reason | Evidence |
| ------- | -------- | ------- | -------- | ------ | -------- |
| raw policyholder PII access | ai_claims_assistant | claim summarization | approval_required | PII requested by agent | metdata classification says `pii` |

## 4. Contract Check

Contract file:
Check result:
Release decision:

## 5. Lineage And Compliance

Source:
Transform:
Product:
Consumers:
Deletion/audit note:

## 6. FinOps

Budget owner: insurance_data_owner
Monthly budget: 500 USD
Current estimated cost: 563 USD
Budget decision: warn

## 7. SME Capture

| SME insight | Client expectation | Capstone action | Evidence to add |
| ----------- | ------------------ | --------------- | --------------- |

## 8. GCP Translation

| Responsibility | GCP service/control |
| -------------- | ------------------- |
| Product labels |                     |
| Column policy  |                     |
| Row policy     |                     |
| Budget alert   |                     |
| Audit log      |                     |
| Monitoring     |                     |

## 9. Active Catalog Proof

| Step | System | output |
| ---- | ------------------ | --------------- |
| unknown column appear | source system | `applicant_contact_email` |
| semantic lookup | Qdrant glossary | nearest term `email address`, classified it as  `pii` |
| proposal | catalog | `PROPOSED - required data owner approval` |
| approval | data owner | `APPROVED by insurance_data_owner` |
| enforecement | policy engine | agent -> approval_required; US human -> block | 

## 10. Honest Limitation

What this class proof does not prove yet:
