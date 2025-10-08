from fastapi import APIRouter, UploadFile, File, HTTPException
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

    return {"filename": safe_name, "bytes": len(raw), "path": path}