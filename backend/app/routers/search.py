from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embeddings import embed_texts

router = APIRouter()

class SearchReq(BaseModel):
    query: str
    top_k: int = 5

@router.post("/")
def search(req: SearchReq):
    [qvec] = embed_texts([req.query])
    return {"embed_dim": len(qvec)}
