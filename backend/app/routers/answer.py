import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from app.services.embeddings import embed_texts
from app.db import get_conn
from app.services.embeddings import embed_texts

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AnswerRequest(BaseModel):
    query: str
    top_k: int = 5

class AnswerResponse(BaseModel):
    answer: str
    citations: list[dict]
    context_used: list[str]

@router.post("/", response_model=AnswerResponse)
def generate_answer(request: AnswerRequest):
    conn = get_conn()
    
    try:
        query_vecs = embed_texts([request.query])
        if not query_vecs:
            raise HTTPException(500, "Failed to generate embedding")
        query_embedding = query_vecs[0]

        sql = """
        SELECT 
            c.id, 
            c.document_id, 
            c.content, 
            d.title as doc_title,
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
