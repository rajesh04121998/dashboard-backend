from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import Optional
from datetime import datetime

app = FastAPI(title="Dynamic Dashboard API")

# Load CSV data
df = pd.read_csv("data/warehouse/warehouse.csv", parse_dates=["assigned_date"])


class DashboardRequest(BaseModel):
    dimension: str
    metrics: list
    start_date: Optional[str] = None
    end_date: Optional[str] = None
@app.get("/")
def root():
    return {"message": "Dynamic Dashboard API is running"}
