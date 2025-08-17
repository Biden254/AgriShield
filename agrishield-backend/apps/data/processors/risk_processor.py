"""
Risk processor: applies risk scoring algorithms on incoming data.
"""

def calculate_risk_levels(data: dict) -> dict:
    """
    Calculate flood risk levels from input data.

    Args:
        data (dict): Raw forecast/enriched data.

    Returns:
        dict: Data annotated with calculated risk level.
    """
    risk_data = data.copy()

    # Example placeholder logic
    rainfall = data.get("rainfall", 0)
    if rainfall > 50:
        risk_data["risk_level"] = "high"
    elif rainfall > 20:
        risk_data["risk_level"] = "medium"
    else:
        risk_data["risk_level"] = "low"

    return risk_data
