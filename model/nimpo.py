import pandas as pd
from sklearn.linear_model import LinearRegression
from joblib import dump
from service.analysis_client import ingest_csv, get_analysis

csv_text = open("data/raw.csv").read()

analysis = ingest_csv(csv_text)
analysis_id = analysis["id"]

meta = get_analysis(analysis_id)

df = pd.read_csv("data/raw.csv")

X = df.select_dtypes(include=["number"]).dropna()
y = X.iloc[:, 0]

model = LinearRegression()
model.fit(X, y)

dump(model, f"model/model_{analysis_id}.joblib")
