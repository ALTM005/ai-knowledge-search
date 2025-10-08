from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dbtest, ingest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dbtest.router, prefix="/db", tags=["db"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])

@app.get("/health")
def health():
    return {"status":"running"}