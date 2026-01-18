import os
from typing import List
from openai import OpenAI

EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Embeds a list of texts using OpenAI.
    """
    if not texts:
        return []
    cleaned_texts = [t.replace("\n", " ") for t in texts]

    try:
        client = get_client()
        resp = client.embeddings.create(model=EMBED_MODEL, input=cleaned_texts)
        return [d.embedding for d in resp.data]
    except Exception as e:
        print(f"Embedding error: {e}")
        return []