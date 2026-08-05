from pathlib import Path 
import csv
import json
import sys

try:
    import yaml
    print("PyYAML available")
except ImportError:
    sys.exit("PyYAML is missing")

contract_path = Path("day-08-contract.yml")
contract = yaml.safe_load(contract_path.read_text())

if not isinstance(contract, dict):
    sys.exit("contract did not parse into a mapping")

required = contract.get("required_columns") or []

if not required:
    sys.exit("no columns found in the contract")

sample_path = Path("day-08-observed-sample.csv")

if sample_path.exists():
    with sample_path.open(newline="") as fh:
        observed_columns = next(csv.reader(fh))
    source = str(sample_path)
else:
    observed_columns = [
        "policy_id",
        "customer_name", 
        "email",
        "region",
        "premium_amount",
        "policy_status"
    ]
    source = "built-in sample (no day-08-observed-sample.csv found)"

missing = sorted(set(required) - set(observed_columns))
extra = sorted(set(observed_columns) - set(required))

result = {
    "contract": str(contract_path),
    "observed_source": source,
    "required_columns": required,
    "observed_columns": observed_columns,
    "missing_columns": missing,
    "extra_columns": extra,
    "release_decision": "pass" if not missing else "block",
}

Path("day-08-contract-check-result.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))



