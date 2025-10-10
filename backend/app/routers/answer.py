from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

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

    return {"answer": "", "citations": [], "chunks": []}
