from fastapi import APIRouter
from pydantic import BaseModel
from app.db import get_conn
from app.services.embeddings import embed_texts

router = APIRouter()

class SearchReq(BaseModel):
    query: str
    top_k: int = 5

@router.post("/")
def search(req: SearchReq):
    [qvec] = embed_texts([req.query])

    sql = """
        select
          c.id,
          c.document_id,
          c.chunk_index,
          c.content,
          1 - (c.embedding <#> %s::vector) as score
        from chunks c
        order by c.embedding <#> %s::vector
        limit %s
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (qvec, qvec, req.top_k))
        rows = cur.fetchall()

    return {"results": rows}
