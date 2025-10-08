from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader
from app.db import get_conn
from app.services.chunking import simple_chunk
from app.services.embeddings import embed_texts
import os


router = APIRouter()

@router.post("/pdf")
async def ingest_pdf(file: UploadFile = File(...), title: str | None = None):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Please upload a PDF")

    raw = await file.read()
    if not raw:
        raise HTTPException(400, "Empty file upload")

    #saving a local copy 
    safe_name = os.path.basename(file.filename)
    save_dir = os.path.abspath(os.path.join(os.getcwd(), "..", "data"))
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, safe_name)
    with open(path, "wb") as f:
        f.write(raw)

    #extract text
    try:
        reader = PdfReader(path)
        text = "\n".join([p.extract_text() or "" for p in reader.pages])
    except Exception as e:
        raise HTTPException(400, f"Failed to read PDF: {e}")

    #chunk and embed
    chunks = simple_chunk(text)
    if not chunks:
        raise HTTPException(400, "No text extracted from PDF")

    vectors = embed_texts(chunks)
    if not vectors or len(vectors) != len(chunks):
        raise HTTPException(400, "Failed to embed chunks")

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "insert into documents(title, source, filepath) values(%s,%s,%s) returning id",
            (title or safe_name, "upload", path),
        )
        doc_id = cur.fetchone()["id"]

        for i, (c_text, vec) in enumerate(zip(chunks, vectors)):
            cur.execute(
                """
                insert into chunks(document_id, chunk_index, content, embedding, tokens)
                values (%s, %s, %s, %s, %s)
                """,
                (doc_id, i, c_text, vec, len(c_text.split()))
            )

    return {"document_id": str(doc_id), "chunks": len(chunks)}