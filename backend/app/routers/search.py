from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SearchReq(BaseModel):
    query: str
    top_k: int = 5

@router.post("/")
def search(req: SearchReq):
    return {"results": []}