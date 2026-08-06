-- Metric: claim_approval_rate
-- Approved definition (day-04-giverned-agent-audit.md §3.1):
--   approved_claims / reviewed_claims, claim-level grain
-- Read-only. No SELECT *. No raw PII columns.
--
-- PLACEHOLDER / NEEDS CONFIRMATION:
--   {{APPROVED_STATUS_VALUES}} = ('A')      -- assumed A = Approved
--   {{REVIEWED_STATUS_VALUES}} = ('A','D')  -- assumed D = Denied/Declined
--   No data dictionary confirms these codes. Do not ship without steward sign-off.


-- ============================================================
-- Q1. Headline metric (single aggregate row, no row-level output)
-- ============================================================
SELECT
    COUNT(DISTINCT CASE WHEN UPPER(TRIM(CLAIM_STATUS)) IN ('A')
                        THEN TRANSACTION_ID END)                    AS approved_claims,
    COUNT(DISTINCT CASE WHEN UPPER(TRIM(CLAIM_STATUS)) IN ('A','D')
                        THEN TRANSACTION_ID END)                    AS reviewed_claims,
    ROUND(
        COUNT(DISTINCT CASE WHEN UPPER(TRIM(CLAIM_STATUS)) IN ('A')
                            THEN TRANSACTION_ID END) * 1.0
        / NULLIF(COUNT(DISTINCT CASE WHEN UPPER(TRIM(CLAIM_STATUS)) IN ('A','D')
                                     THEN TRANSACTION_ID END), 0)
    , 4)                                                            AS claim_approval_rate
FROM gold_claims
WHERE CLAIM_STATUS IS NOT NULL
  AND UPPER(TRIM(CLAIM_STATUS)) IN ('A','D');   -- denominator guard: reviewed claims only


-- ============================================================
-- Q2. Same metric by allowed dimensions only
--     (§3.1 allowed: time period, region, claim type, product line)
--     Row-level output -> LIMIT enforced.
-- ============================================================
SELECT
    INSURANCE_TYPE                                                  AS claim_type,
    INCIDENT_STATE                                                  AS region,
    EXTRACT(YEAR FROM CAST(LOSS_DT AS DATE))                        AS loss_year,
    COUNT(DISTINCT CASE WHEN UPPER(TRIM(CLAIM_STATUS)) IN ('A')
                        THEN TRANSACTION_ID END)                    AS approved_claims,
    COUNT(DISTINCT TRANSACTION_ID)                                  AS reviewed_claims,
    ROUND(
        COUNT(DISTINCT CASE WHEN UPPER(TRIM(CLAIM_STATUS)) IN ('A')
                            THEN TRANSACTION_ID END) * 1.0
        / NULLIF(COUNT(DISTINCT TRANSACTION_ID), 0)
    , 4)                                                            AS claim_approval_rate
FROM gold_claims
WHERE CLAIM_STATUS IS NOT NULL
  AND UPPER(TRIM(CLAIM_STATUS)) IN ('A','D')
GROUP BY
    INSURANCE_TYPE,
    INCIDENT_STATE,
    EXTRACT(YEAR FROM CAST(LOSS_DT AS DATE))
HAVING COUNT(DISTINCT TRANSACTION_ID) >= 30   -- small-cell suppression
ORDER BY reviewed_claims DESC
LIMIT 100;
