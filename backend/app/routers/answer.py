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
        LEFT JOIN documents d ON c.document_id = d.id
        ORDER BY c.embedding <=> %s::vector
        LIMIT %s;
        """
        
        with conn.cursor() as cur:

            cur.execute("SET LOCAL enable_indexscan = off;")
            
            cur.execute(sql, (query_embedding, query_embedding, request.top_k))
            rows = cur.fetchall()
            
        if not rows:
            return AnswerResponse(
                answer="I couldn't find any relevant information in the uploaded documents.",
                citations=[],
                context_used=[]
            )

        context_text = ""
        citations = []
        context_list = []
        
        for i, row in enumerate(rows):
            chunk_text = row['content']
            source_title = row.get('doc_title') or "Unknown"
            score = row.get('score', 0)

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
