import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from pgvector.psycopg import register_vector

# Load .env
try:
    from dotenv import load_dotenv

    backend_dir = Path(__file__).resolve().parents[2] 
    env_path = backend_dir / ".env"                    
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv() 
except Exception:
    pass

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Put it in backend/.env or export it."
        )
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    register_vector(conn)
    return conn
