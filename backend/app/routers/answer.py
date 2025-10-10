from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class AnswerReq(BaseModel):
    query: str
    top_k: int = 6
    model: str = "gpt-4o-mini"

@router.post("/")
def answer(req: AnswerReq):
    return {"answer": "", "citations": [], "chunks": []}
