import pandas as pd
from datetime import datetime
from .file_utils import load_aggregation_mapping


def generate_dashboard_data(df: pd.DataFrame, dimension: str, metrics: list, start_date: str, end_date: str = None):
    mapping = load_aggregation_mapping()

    if dimension not in mapping:
        raise ValueError(f"Invalid dimension: {dimension}")

    valid_metrics = mapping[dimension]["aggregation_fields"]
    invalid_metrics = [m for m in metrics if m not in valid_metrics]
    if invalid_metrics:
        raise ValueError(f"Invalid metrics for {dimension}: {invalid_metrics}")

    # Convert and filter by date
    df["assigned_date"] = pd.to_datetime(df["assigned_date"])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date) if end_date else datetime.now()
    df = df[(df["assigned_date"] >= start_date) & (df["assigned_date"] <= end_date)]

    if df.empty:
        return {}

    result = {}

    if dimension == "agent_id":
        group_col = "assigned_to"
        grouped = df.groupby(group_col)

        for key, group in grouped:
            agg_data = {}

            if "total_calls" in metrics:
                agg_data["total_calls"] = len(group)

            if "answered_calls" in metrics:
                agg_data["answered_calls"] = len(group[group["call_status"] == "answered"])

            if "missed_calls" in metrics:
                agg_data["missed_calls"] = len(group[group["call_status"] == "missed"])

            if "conversion_rate" in metrics:
                total = len(group)
                converted = len(group[group["status"] == "converted_yes"])
                agg_data["conversion_rate"] = round((converted / total) * 100, 2) if total > 0 else 0

            if "avg_call_duration" in metrics:
                agg_data["avg_call_duration"] = round(group["call_duration"].mean(), 2)

            if "hot_deals_count" in metrics:
                agg_data["hot_deals_count"] = int(group["is_hot"].sum())

            if "warm_deals_count" in metrics:
                agg_data["warm_deals_count"] = int(group["is_warm"].sum())

            if "cold_deals_count" in metrics:
                agg_data["cold_deals_count"] = int(group["is_cold"].sum())

            result[key] = agg_data

    elif dimension == "manager_id":
        group_col = "assigned_by"
        grouped = df.groupby(group_col)

        for manager, group in grouped:
            agg_data = {}

            # Total distinct agents under this manager
            if "total_agents" in metrics:
                agg_data["total_agents"] = group["assigned_to"].nunique()

            # Total leads assigned by this manager
            if "total_leads" in metrics:
                agg_data["total_leads"] = len(group)

            # Leads converted under this manager
            if "leads_converted" in metrics:
                agg_data["leads_converted"] = len(group[group["status"] == "converted_yes"])

            # Average conversion rate of manager’s team
            if "avg_team_conversion_rate" in metrics:
                total_leads = len(group)
                converted = len(group[group["status"] == "converted_yes"])
                agg_data["avg_team_conversion_rate"] = round((converted / total_leads) * 100, 2) if total_leads > 0 else 0

            result[manager] = agg_data

    return result
