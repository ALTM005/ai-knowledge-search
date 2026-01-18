import re

def simple_chunk(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Splits text into smaller overlapping chunks to improve search precision.
    """
    clean_text = re.sub(r'\s+', ' ', text).strip()
    
    chunks = []
    i = 0
    while i < len(toks):
        window = toks[i:i+max_tokens]
        chunks.append(enc.decode(window))
        i += max_tokens - overlap
    return [c for c in chunks if c.strip()]
