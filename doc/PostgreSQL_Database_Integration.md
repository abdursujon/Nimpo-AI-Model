pip install psycopg2-binary
where it's installed
C:\Users\abdur\AppData\Local\Programs\Python\Python312\Lib\site-packages\
Verify from terminal:
pip show psycopg2-binary

set postgre with project
$env:DATABASE_URL="postgresql://postgres:191818@localhost:5432/nimpo"
echo $env:DATABASE_URL
run db connection test: python database_integration/db_connection_test.py

BEGIN;

CREATE TABLE dataset_analysis (
    id BIGINT PRIMARY KEY,              
    number_of_rows INT,
    number_of_columns INT,
    total_characters INT,
    created_at TIMESTAMP
);

CREATE TABLE column_statistics (
    id BIGSERIAL PRIMARY KEY,
    analysis_id BIGINT REFERENCES dataset_analysis(id) ON DELETE CASCADE,
    column_name TEXT,
    null_count INT,
    unique_count INT
);

CREATE TABLE nimpo_decision (
    analysis_id BIGINT PRIMARY KEY REFERENCES dataset_analysis(id) ON DELETE CASCADE,
    quality_score INT,
    usable BOOLEAN NOT NULL,
    risk_level TEXT NOT NULL,
    confidence_score INT
);

CREATE TABLE dataset_issues (
    id BIGSERIAL PRIMARY KEY,
    analysis_id BIGINT REFERENCES dataset_analysis(id) ON DELETE CASCADE,
    issue_details TEXT
);

CREATE TABLE dataset_recommendations (
    id BIGSERIAL PRIMARY KEY,
    analysis_id BIGINT REFERENCES dataset_analysis(id) ON DELETE CASCADE,
    recommendation_details TEXT
);

CREATE TABLE nimpo_model (
    id BIGSERIAL PRIMARY KEY,
    analysis_id BIGINT REFERENCES dataset_analysis(id),
    model_type TEXT,
    model_uri TEXT,
    created_at TIMESTAMP DEFAULT now()
);

COMMIT;

