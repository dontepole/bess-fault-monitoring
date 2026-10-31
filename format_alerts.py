"""Format synthetic BESS alerts for an operator-facing notification."""

from classify_faults import classify_fault


def format_alert(record: dict) -> str:
    concern_type = classify_fault(record.get("fault_name"))
    reasons = ", ".join(record.get("alert_reasons", []))

    return (
        f"[{record['record_type']}] {record['site_id']} | {record['asset_id']}\n"
        f"Reason: {reasons}\n"
        f"Rack Availability: {record['racks_in_service']}/{record['expected_racks']}\n"
        f"Status: {record['status']}\n"
        f"Concern Type: {concern_type}"
    )
