import os
import pdfplumber
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.db import get_conn
from app.services.chunking import simple_chunk
from app.services.embeddings import embed_texts

router = APIRouter()

@router.post("/pdf")
async def ingest_file(file: UploadFile = File(...), title: str | None = None):
    filename = file.filename.lower()
    
    if not (filename.endswith(".pdf") or filename.endswith(".txt")):
        raise HTTPException(400, "Please upload a PDF or TXT file")

    save_dir = os.path.abspath(os.path.join(os.getcwd(), "..", "data"))
    os.makedirs(save_dir, exist_ok=True)
    safe_name = os.path.basename(file.filename)
    path = os.path.join(save_dir, safe_name)
    
    raw = await file.read()
    with open(path, "wb") as f:
        f.write(raw)

    text = ""
    if filename.endswith(".txt"):
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1")        
    else:
        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n\n"
        except Exception as e:
            print(f"PDF Error: {e}")
            raise HTTPException(400, f"Failed to read PDF: {e}")

    print(f"\nINGEST REPORT:")
    print(f"   File: {safe_name}")
    print(f"   Length: {len(text)} characters")
    
    if len(text) < 100:
        raise HTTPException(400, "File is empty or could not be read.")

    chunks = simple_chunk(text)
    print(f"   Generated {len(chunks)} chunks.")
    
    vectors = embed_texts(chunks)

        for i, (c_text, vec) in enumerate(zip(chunks, vectors)):
            cur.execute(
                """
                insert into chunks(document_id, chunk_index, content, embedding, tokens)
                values (%s, %s, %s, %s, %s)
                """,
                (doc_id, i, c_text, vec, len(c_text.split()))
            )

    return {"document_id": str(doc_id), "chunks": len(chunks)}