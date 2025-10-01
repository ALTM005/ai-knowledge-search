from fastapi import APIRouter
from app.db import get_conn

router = APIRouter()

@router.get("/ping")
def db_ping():
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("select version() as v")
            row = cur.fetchone()
            return {"db_version": row["v"]}
    except Exception as e:
        return {"error": str(e)}