import os, psycopg2

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()
cur.execute("SELECT 1;")
print(cur.fetchone())
conn.close()
