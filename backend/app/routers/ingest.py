from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader
from app.services.chunking import simple_chunk
import os

router = APIRouter()

@router.post("/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Please upload a PDF")

    raw = await file.read()
    if not raw:
        raise HTTPException(400, "Empty file upload")

    safe_name = os.path.basename(file.filename)
    save_dir = os.path.abspath(os.path.join(os.getcwd(), "..", "data"))
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, safe_name)
    with open(path, "wb") as f:
        f.write(raw)

    #extract the text
    try:
        reader = PdfReader(path)
        text = "\n".join([p.extract_text() or "" for p in reader.pages])
    except Exception as e:
        raise HTTPException(400, f"Failed to read PDF: {e}")

    if not text.strip():
        raise HTTPException(400, "No text extracted from PDF")

    #chunk
    chunks = simple_chunk(text)
    if not chunks:
        raise HTTPException(400, "Chunking produced no chunks")

    return {
        "filename": safe_name,
        "path": path,
        "extracted_chars": len(text),
        "chunks": len(chunks),
    }