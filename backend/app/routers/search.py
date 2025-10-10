from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import get_conn
from app.services.embeddings import embed_texts

router = APIRouter()

class SearchReq(BaseModel):
    query: str
    top_k: int = 5

@router.post("/")
def search(req: SearchReq):
    q = (req.query or "").strip()
    if not q:
        raise HTTPException(400, "Query must not be empty")

    top_k = req.top_k if req.top_k is not None else 5
    if not (1 <= top_k <= 50):
        raise HTTPException(400, "top_k must be between 1 and 50")

    [qvec] = embed_texts([q])

    sql = """
        SELECT
          c.id,
          c.document_id,
          c.chunk_index,
          c.content,
          1 - (c.embedding <=> %s::vector) AS score   -- similarity in [0,1]
        FROM chunks c
        ORDER BY c.embedding <=> %s::vector           -- smallest distance first
        LIMIT %s;
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (qvec, qvec, top_k))
        rows = cur.fetchall() 

    return {"results": rows}



