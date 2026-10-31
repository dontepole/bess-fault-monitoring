"""Classify synthetic BESS fault messages into operator-friendly categories."""


def classify_fault(fault_name: str | None) -> str:
    if not fault_name:
        return "Unknown"

    name = fault_name.lower()

    if any(x in name for x in ["bms", "bmu", "cell", "rack", "battery"]):
        return "BMS / Cells / Racks"
    if any(x in name for x in ["pcs", "inverter"]):
        return "PCS / Inverter"
    if any(x in name for x in ["hvac", "chiller", "cooling", "fan", "tms"]):
        return "Cooling / TMS"
    if any(x in name for x in ["comm", "communication", "network", "modbus"]):
        return "Communications"
    if any(x in name for x in ["breaker", "relay", "poi"]):
        return "Breaker / Grid Interface"

    return "Other"
