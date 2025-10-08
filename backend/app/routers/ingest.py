from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    return {"filename": file.filename, "status": "received"}