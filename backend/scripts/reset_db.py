import sys, os
import psycopg

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db import get_conn

def reset_db():
    print("  Wiping database...")
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE chunks, documents CASCADE;")
            conn.commit()
        print("✨ Database is empty and clean.")
    except Exception as e:
        print(f" Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    reset_db()