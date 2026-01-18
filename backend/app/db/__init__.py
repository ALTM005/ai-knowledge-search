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

def get_conn():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Put it in backend/.env or export it."
        )
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    register_vector(conn)
    return conn
