import requests
import logging

BASE_URL = "http://localhost:8080"

logging.basicConfig(level=logging.INFO)

def ingest_csv(csv_text: str) -> dict:
    r = requests.post(
        f"{BASE_URL}/api/analysis/ingestCsv",
        headers={"Content-Type": "text/plain"},
        data=csv_text
    )
    r.raise_for_status()
    data = r.json()
    logging.info("Ingest response: %s", data)
    return data

def get_analysis(analysis_id: int) -> dict:
    r = requests.get(f"{BASE_URL}/api/analysis/{analysis_id}")
    r.raise_for_status()
    data = r.json()
    logging.info("Get analysis response: %s", data)
    return data
