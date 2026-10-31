-- Public-safe demo logic for BESS health/fault monitoring.
-- Designed for synthetic data only.

WITH latest AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY site_id, asset_id
            ORDER BY timestamp DESC
        ) AS rn
    FROM synthetic_bess_telemetry
),
current_state AS (
    SELECT *
    FROM latest
    WHERE rn = 1
)
SELECT
    site_id,
    asset_id,
    expected_racks,
    racks_in_service,
    maint_mode,
    is_faulted,
    fault_name,
    max_cell_voltage,
    soc,
    status,
    CASE
        WHEN is_faulted = TRUE THEN 'FAULT'
        WHEN racks_in_service < expected_racks THEN 'HEALTH'
        WHEN maint_mode = TRUE THEN 'HEALTH'
        WHEN max_cell_voltage > 3.60 THEN 'HEALTH'
        ELSE 'NORMAL'
    END AS record_type,
    CASE
        WHEN is_faulted = TRUE THEN 'Active Fault'
        WHEN racks_in_service < expected_racks THEN 'Reduced Rack Availability'
        WHEN maint_mode = TRUE THEN 'Maintenance Mode'
        WHEN max_cell_voltage > 3.60 THEN 'High Cell Voltage'
        ELSE 'Normal'
    END AS alert_reason
FROM current_state
WHERE
    is_faulted = TRUE
    OR racks_in_service < expected_racks
    OR maint_mode = TRUE
    OR max_cell_voltage > 3.60
ORDER BY site_id, asset_id;
