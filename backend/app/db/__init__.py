import os
import psycopg
from pathlib import Path
from psycopg.rows import dict_row
from pgvector.psycopg import register_vector

try:
    from dotenv import load_dotenv
    base_dir = Path(__file__).resolve().parent.parent.parent
    env_path = base_dir / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv() 
except ImportError:
    pass

def get_conn() -> psycopg.Connection:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set.")

    try:
        conn = psycopg.connect(
            db_url, 
            row_factory=dict_row, 
            autocommit=False,
            prepare_threshold=None 
        )
        
        register_vector(conn)
        return conn
    except psycopg.OperationalError as e:
        print(f"DB Connection Failed: {e}")
        raise e