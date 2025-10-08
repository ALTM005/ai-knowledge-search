import os
from typing import List
from openai import OpenAI

EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
_client = OpenAI()

def embed_texts(texts: List[str]) -> List[List[float]]:
    if not texts:
        return []
    resp = _client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]