import json
from pathlib import Path

def load_aggregation_mapping():
    base_dir = Path(__file__).resolve().parent.parent  # goes up from /app/utils → /app
    file_path = base_dir / "data/sql_database/aggregationmapping.json"

    if not file_path.exists():
            raise FileNotFoundError(f"Aggregation mapping file not found at {file_path}")

    with open(file_path, "r") as f:
        mapping = json.load(f)

    return mapping
