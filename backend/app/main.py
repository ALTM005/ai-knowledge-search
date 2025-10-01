from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dbtest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dbtest.router, prefix="/db", tags=["db"])

@app.get("/health")
def health():
    return {"status":"running"}