from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dbtest, ingest, search, answer

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
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(answer.router,  prefix="/answer", tags=["answer"])

@app.get("/health")
def health():
    return {"status":"running"}