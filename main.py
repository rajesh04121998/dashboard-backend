from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import Optional
from datetime import datetime
from utils.file_utils import load_aggregation_mapping

app = FastAPI(title="Dynamic Dashboard API")

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