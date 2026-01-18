import re

def simple_chunk(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Splits text into smaller overlapping chunks to improve search precision.
    """
    clean_text = re.sub(r'\s+', ' ', text).strip()
    
    chunks = []
    start = 0
    text_len = len(clean_text)

    while start < text_len:
        end = start + chunk_size
        
        if end < text_len:
            period_index = clean_text.rfind('.', start, end)
            if period_index != -1 and period_index > start + (chunk_size * 0.5):
                end = period_index + 1 
            else:
                space_index = clean_text.rfind(' ', start, end)
                if space_index != -1:
                    end = space_index
        
        chunk = clean_text[start:end].strip()
        if chunk: 
            chunks.append(chunk)
        
        start = end - overlap
        
        if start >= end:
            start = end

    return chunks