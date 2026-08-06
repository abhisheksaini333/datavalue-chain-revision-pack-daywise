from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd 


PRIMARY = Path("/home/labuser/Desktop/Persistent_Folder/Workspace/day-05-evidence/source-extract/insurance_cash_application.csv")
OUTPUT = Path("logs") / "smoke_test_result.json"


def read_dataset() -> tuple[Path, pd.DataFrame]:
    if PRIMARY.exists():
        return PRIMARY, pd.read_csv(PRIMARY)
    raise FileNotFoundError("Dataset not found")


def main() -> int:
    dataset_path, df = read_dataset()
    columns = [str(c) for c in df.columns]
    checks = {
        "dataset_exists": dataset_path.exists(),
        "row_count_positive": len(df) > 0,
        "at_least_three_columns": len(columns) >= 3,
        "business_column_hints_present": any(
            token in " ".join(columns).lower()
            for token in ["claim", "policy", "customer", "amount", "payment", "cash"]
        ),
    }
    passed = all(checks.values())
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_used": str(dataset_path),
        "row_count": int(len(df)),
        "column_count": int(len(columns)),
        "sample_columns": columns[:8],
        "checks": checks,
        "status": "PASS" if passed else "FAIL",
        "production_decision": "ready_for_demo_packaging" if passed else "blocked_before_apckaging",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    return 0 if passed else 1

if __name__ == "__main__":
    raise SystemExit(main())