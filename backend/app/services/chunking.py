from typing import List
import tiktoken

def simple_chunk(text: str, max_tokens: int = 500, overlap: int = 60) -> List[str]:
   
    enc = tiktoken.get_encoding("cl100k_base")
    toks = enc.encode(text or "")
    if not toks:
        return []
    chunks = []
    i = 0
    while i < len(toks):
        window = toks[i:i+max_tokens]
        chunks.append(enc.decode(window))
        i += max_tokens - overlap
    return [c for c in chunks if c.strip()]
