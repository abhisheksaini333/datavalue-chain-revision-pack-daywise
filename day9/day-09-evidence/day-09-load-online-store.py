import subprocess

sql = """
SELECT DISTINCT ON (claim_id) claim_id, reserve_amount, provider_disputes, events_ts
FROM day09_claim_events ORDER BY claim_id, events_ts DESC;
"""

out = subprocess.run(["psql", "-U", "labuser", "-d", "labuser_db", sql],
                        capture_output=True, text=True
                    )

if out.returncode != 0:
    raise SystemExit("Postgres not available")

def redis(*a):
    return subprocess.run(["redis-cli", "-p", "6379", *a], capture_output=True, text=True)

count = 0
for line in out.stdout().strip().splitlines():
    claim_id, reserve, disputes, ts = line.split("|")
    key = f"day09:features:{claim_id}"
    redis("HSET", key, "reserve_amount", reserve, "provider_disputes", disputes, "event_ts", ts)
    redis("EXPIRE", key, "3600")
    count += 1
    print(f" online {key} reserve={reserve} disputes={disputes}")


print(f"\n loaded {count} entities into online store")
print("single-entity serving lookup for CLM-9001:")
print(" ", redis("HGET", "day09:features:CLM-9001"))