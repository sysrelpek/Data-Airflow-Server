from fastapi import FastAPI
from datetime import datetime
import json
import os

app = FastAPI(title="Data Airflow Monitor API")

# ====================== CONFIG ======================
STORAGE_PATH = "./demo_storage"
DEMO_FILE = "demo_run.json"
# ====================================================


@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/metrics")
def get_metrics():
    """Return current storage metrics"""
    file_path = os.path.join(STORAGE_PATH, DEMO_FILE)

    if not os.path.exists(file_path):
        return {
            "status": "no_data",
            "records_in_storage": 0,
            "last_updated": None
        }

    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        return {
            "status": "ok",
            "records_in_storage": len(data),
            "last_updated": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_monitor:app", host="0.0.0.0", port=8000, reload=True)