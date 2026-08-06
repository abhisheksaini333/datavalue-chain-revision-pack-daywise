psql -U labuser -d labuser_db
DROP TABLE day09_claim_events;

CREATE TABLE day09_claim_events (
    claim_id text,
    policy_id text,
    events_ts timestamptz,
    reserve_amount numeric,
    provider_disputes int
);

INSERT INTO day09_claim_events VALUES
    ('CLM-9001', 'POL-101', '2026-08-06 09:00+00', 12000, 1),
    ('CLM-9001', 'POL-101', '2026-07-20 09:00+00', 18000, 3),
    ('CLM-9001', 'POL-101', '2026-08-10 09:00+00', 25000, 7),
    ('CLM-9002', 'POL-102', '2026-07-05 09:00+00', 4200, 0),
    ('CLM-9002', 'POL-102', '2026-08-12 09:00+00', 6100, 2);

SELECT claim_id, events_ts, reserve_amount, provider_disputes 
FROM day09_claim_events ORDER BY claim_id, events_ts;



WITH labels(claim_id, decision_ts, is_fraud) AS (
    VALUES ('CLM-9001', timestamptz '2026-08-06 00:00+00', true),
    ('CLM-9002', timestamptz '2026-08-01 00:00+00', true)
)
SELECT
    l.claim_id,
    l.decision_ts,
    l.is_fraud,
    e.reserve_amount AS reserve_amount_at_decision_time,
    e.provider_disputes AS disputes_at_decision_time,
    e.events_ts AS feature_as_of
FROM labels l
LEFT JOIN LATERAL (
    SELECT reserve_amount, provider_disputes, events_ts
    FROM day09_claim_events c
    WHERE c.claim_id = l.claim_id
        AND c.events_ts <= l.decision_ts
    ORDER BY c.events_ts DESC
    LIMIT 1
) e ON true
ORDER BY l.claim_id;




