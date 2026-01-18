import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db import get_conn

with get_conn() as conn:
    print("Documents:", conn.execute("SELECT COUNT(*) FROM documents").fetchone()['count'])
    print("Chunks:   ", conn.execute("SELECT COUNT(*) FROM chunks").fetchone()['count'])