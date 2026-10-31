"""Detect abnormal conditions in synthetic BESS telemetry."""

from __future__ import annotations

import pandas as pd


def load_latest_states(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp")
    return df.groupby(["site_id", "asset_id"], as_index=False).tail(1)


def detect_conditions(df: pd.DataFrame) -> pd.DataFrame:
    records: list[dict] = []

    for _, row in df.iterrows():
        reasons: list[str] = []

        if bool(row["is_faulted"]):
            reasons.append("Active Fault")
        if int(row["racks_in_service"]) < int(row["expected_racks"]):
            reasons.append("Reduced Rack Availability")
        if bool(row["maint_mode"]):
            reasons.append("Maintenance Mode")
        if float(row["max_cell_voltage"]) > 3.60:
            reasons.append("High Cell Voltage")

        if reasons:
            record = row.to_dict()
            record["alert_reasons"] = reasons
            record["record_type"] = "FAULT" if bool(row["is_faulted"]) else "HEALTH"
            records.append(record)

    return pd.DataFrame(records)


if __name__ == "__main__":
    latest = load_latest_states("data/synthetic_bess_telemetry.csv")
    alerts = detect_conditions(latest)
    print(alerts[["site_id", "asset_id", "record_type", "alert_reasons"]].to_string(index=False))
