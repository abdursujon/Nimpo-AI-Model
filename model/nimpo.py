import os
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from joblib import dump
import psycopg2
import json

from .nimpo_decision import nimpo_decision

BASE_URL = "https://spring-data-analysis-api.onrender.com"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw.csv")
MODEL_DIR = BASE_DIR


# Ingest the csv to the api endpoint
def ingest_csv():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        csv_text = f.read()

    r = requests.post(
        f"{BASE_URL}/api/analysis/ingestCsv",
        data=csv_text,
        headers={"Content-Type": "text/plain"},
        timeout=30
    )
    r.raise_for_status()
    return r.json()


# Get analysis from the api endpoints
def get_analysis(analysis_id: int):
    r = requests.get(
        f"{BASE_URL}/api/analysis/{analysis_id}",
        timeout=30
    )
    r.raise_for_status()
    return r.json()


# Get db connection
def get_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


# Add save analysis data to the db
def save_analysis(meta, conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO dataset_analysis
            (id, number_of_rows, number_of_columns, total_characters, created_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            RETURNING id
            """,
            (
                meta["id"],
                meta["numberOfRows"],
                meta["numberOfColumns"],
                meta["totalCharacters"],
                meta["createdAt"]
            )
        )
        row = cur.fetchone()
        conn.commit()
    return row[0] if row else meta["id"]


def save_column_statistics(meta, conn):
    with conn.cursor() as cur:
        for col in meta.get("columnStatistics", []):
            cur.execute(
                """
                INSERT INTO column_statistics
                (analysis_id, column_name, null_count, unique_count)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    meta["id"],
                    col["columnName"],
                    col["nullCount"],
                    col["uniqueCount"]
                )
            )
        conn.commit()


def save_decision(analysis_id, decision, conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO nimpo_decision
            (analysis_id, quality_score, usable, risk_level, confidence_score)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                analysis_id,
                decision.get("qualityScore"),
                decision["usable"],
                decision["riskLevel"],
                decision.get("confidenceScore")
            )
        )
        conn.commit()


def save_decision_issues(analysis_id, decision, conn):
    issues = decision.get("issues", [])
    if not issues:
        return

    with conn.cursor() as cur:
        for issue in issues:
            cur.execute(
                """
                INSERT INTO decision_issues (analysis_id, issue)
                VALUES (%s, %s)
                """,
                (analysis_id, issue)
            )
        conn.commit()


def save_decision_recommendations(analysis_id, decision, conn):
    recs = decision.get("recommendedActions", [])
    if not recs:
        return

    with conn.cursor() as cur:
        for rec in recs:
            cur.execute(
                """
                INSERT INTO decision_recommendations (analysis_id, recommendation)
                VALUES (%s, %s)
                """,
                (analysis_id, rec)
            )
        conn.commit()


# Add save model refence to the db
def save_model(analysis_id, model_path, conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO nimpo_model (analysis_id, model_type, model_uri)
            VALUES (%s, %s, %s)
            """,
            (analysis_id, "LinearRegression", model_path)
        )
        conn.commit()


# Main application model
def main():
    analysis = ingest_csv()
    analysis_id = analysis["id"]

    meta = get_analysis(analysis_id)
    print(json.dumps(meta, indent=2))

    decision = nimpo_decision(meta)
    print(json.dumps(decision, indent=2))

    df = pd.read_csv(DATA_PATH)

    X = df.select_dtypes(include=["number"]).dropna()
    y = X.iloc[:, 0]

    model = LinearRegression()
    model.fit(X, y)

    conn = get_db()

    save_analysis(meta, conn)
    save_column_statistics(meta, conn)
    save_decision(meta["id"], decision, conn)
    save_decision_issues(meta["id"], decision, conn)
    save_decision_recommendations(meta["id"], decision, conn)

    if decision["usable"]:
        model_path = os.path.join(MODEL_DIR, f"model_{analysis_id}.joblib")
        dump(model, model_path)
        save_model(meta["id"], model_path, conn)

    conn.close()


# Run the model
if __name__ == "__main__":
    main()
