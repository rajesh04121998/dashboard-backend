from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List, Optional
from utils.file_utils import load_aggregation_mapping
from utils.function_utils import generate_dashboard_data
app = FastAPI(title="Dynamic Dashboard API")

class DashboardRequest(BaseModel):
    dimension: str
    metrics: List[str]
    start_date: str
    end_date: Optional[str] = None

df = pd.read_csv("data/warehouse/warehouse.csv", parse_dates=["assigned_date"])

try:
    DIMENSION_MAPPING = load_aggregation_mapping()
except FileNotFoundError:
    DIMENSION_MAPPING = {}

@app.get("/")
def root():
    return {"message": "Dynamic Dashboard API is running"}


@app.get("/dimension-mapping")
def get_dimension_mapping():
    return DIMENSION_MAPPING


@app.post("/dashboard-data")
def get_dashboard_data(request: DashboardRequest):
    try:
        result = generate_dashboard_data(
            df=df,
            dimension=request.dimension,
            metrics=request.metrics,
            start_date=request.start_date,
            end_date=request.end_date,
        )
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

