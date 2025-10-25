import streamlit as st
import requests
import pandas as pd

# Backend API URLs
BASE_URL = "http://127.0.0.1:8000"
DIMENSION_API = f"{BASE_URL}/dimension-mapping"
DASHBOARD_API = f"{BASE_URL}/dashboard-data"

# Title
st.title("Dynamic Dashboard")

# Step 1: Fetch dimensions from API
try:
    dim_response = requests.get(DIMENSION_API)
    dimensions = dim_response.json()
except Exception as e:
    st.error(f"Failed to fetch dimensions: {e}")
    st.stop()

# Step 2: Dimension selection
selected_dimension = st.selectbox("Select Dimension", options=list(dimensions.keys()))

# Step 3: Metrics selection based on dimension
available_metrics = dimensions[selected_dimension]["aggregation_fields"]
selected_metrics = st.multiselect("Select Metrics", options=available_metrics)

# Step 4: Date filters
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# Step 5: Generate Report button
if st.button("Generate Report"):
    if not selected_metrics:
        st.warning("Please select at least one metric.")
    else:
        payload = {
            "dimension": selected_dimension,
            "metrics": selected_metrics,
            "start_date": str(start_date),
            "end_date": str(end_date),
        }
        try:
            dashboard_response = requests.post(DASHBOARD_API, json=payload)
            dashboard_response.raise_for_status()
            result = dashboard_response.json()["data"]

            if not result:
                st.info("No data available for selected filters.")
            else:
                # Convert result into DataFrame for easier display
                df = pd.DataFrame(result).T  # Transpose for better readability
                st.dataframe(df)

        except Exception as e:
            st.error(f"Failed to fetch dashboard data: {e}")
