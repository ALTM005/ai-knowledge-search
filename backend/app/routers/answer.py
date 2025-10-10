from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from app.services.embeddings import embed_texts
from app.db import get_conn

router = APIRouter()
client = OpenAI()

SYSTEM = (
    "You are a concise research assistant. Answer using ONLY the provided context. "
    "If the context is insufficient, say you don't know. "
    'Keep answers short (3-6 sentences). '
    "End with: 'Citations: [<chunk_ids>]' listing the chunk IDs you used."
)

class AnswerReq(BaseModel):
    query: str
    top_k: int = 6
    model: str = "gpt-4o-mini"

@router.post("/")
def answer(req: AnswerReq):
    q = (req.query or "").strip()
    if not q:
        raise HTTPException(400, "Query must not be empty")
    if not (1 <= req.top_k <= 20):
        raise HTTPException(400, "top_k must be between 1 and 20")

    [qvec] = embed_texts([q])

    sql = """
        SELECT
          c.id,
          c.document_id,
          c.chunk_index,
          c.content,
          1 - (c.embedding <=> %s::vector) AS score
        FROM chunks c
        ORDER BY c.embedding <=> %s::vector
        LIMIT %s;
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (qvec, qvec, req.top_k))
        hits = cur.fetchall()

    if not hits:
        return {"answer": "I don't know.", "citations": [], "chunks": []}

    ids = [h["id"] for h in hits]
    context = "\n\n".join(
        f"(chunk {h['id']}): { (h['content'] or '').replace('\\n', ' ')[:2000] }"
        for h in hits
    )
    prompt = f"Context:\n{context}\n\nQuestion: {q}\n\nFollow the system instructions."


    resp = client.chat.completions.create(
        model=req.model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
    )
    answer = resp.choices[0].message.content

    return {"answer": answer, "citations": ids, "chunks": hits}
