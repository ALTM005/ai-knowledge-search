# AI Knowledge Search

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Frontend](https://img.shields.io/badge/frontend-Tailwind-38B2AC.svg)
![Backend](https://img.shields.io/badge/backend-FastAPI-009688.svg)
![Database](https://img.shields.io/badge/database-PostgreSQL-336791.svg)

A high-performance **RAG (Retrieval-Augmented Generation)** engine that transforms static documents into an interactive knowledge base. AI Knowledge Search combines **OpenAI's embeddings** with **pgvector** for semantic search, allowing users to chat with their PDF and text files in real-time with precise, source-backed citations.

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Database Maintenance](#database-maintenance)
- [License](#license)

---

## Features

- **Semantic Search:** Retrieves information based on meaning, not just keyword matching, using vector embeddings.
- **Multi-Format Ingestion:** High-fidelity text extraction for PDFs (`pdfplumber`) and standard text files.
- **Smart Chunking:** Context-aware text splitting algorithm that preserves sentence boundaries for better AI comprehension.
- **Source Citations:** Every AI response includes direct references (`[1]`) and relevance scores to ensure accuracy.
- **Robust Admin Tools:** Includes a suite of CLI scripts for database inspection, index repair, and bulk embedding backfills.

---

## Project Structure

```bash
ai-knowledge-search/
├── backend/
│   ├── app/
│   │   ├── db/                 # Database connection & vector registration
│   │   ├── routers/            # API endpoints (ingest, answer, search)
│   │   ├── services/           # Business logic (chunking, embeddings)
│   │   └── main.py             # FastAPI entry point
│   ├── scripts/                # Database maintenance tools
│   │   ├── backfill_embeddings.py
│   │   ├── check_pdf.py
│   │   ├── inspect_db.py
│   │   └── reset_db.py
│   ├── .env                    # Environment variables (Add your API keys, DB URL)
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   └── index.html              # Responsive Chat UI
│
├── data/                       # Local storage for uploaded documents
│
└── README.md

```

---

## Tech Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| Frontend | HTML5, Tailwind CSS, JS | Responsive Chat UI, real-time citation rendering |
| Backend | FastAPI, Uvicorn | High-performance asynchronous REST API |
| Database | PostgreSQL, pgvector | Vector storage and relational metadata |
| AI Model | OpenAI (GPT-4o) | Contextual answering and text embeddings |
| DevOps | Docker (Optional) | Containerization for deployment |

---

## Installation

### Prerequisites

* Python 3.10+
* PostgreSQL (with `vector` extension installed)
* OpenAI API Key

### 1. Clone Repository

```bash
git clone https://github.com/ALTM005/ai-knowledge-search.git
cd ai-knowledge-search

```

### 2. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Database Setup

First, create the empty database in PostgreSQL:

```bash
psql -U postgres
# Inside SQL Shell:
CREATE DATABASE ai_search;
\c ai_search
CREATE EXTENSION IF NOT EXISTS vector;
\q

```

Then, run the initialization script to create the schema (tables and indexes):

```bash
# From the root directory
python backend/scripts/reset_db.py

```

---

## Environment Variables

Create a `.env` file in the `backend/` directory.

### Backend (`backend/.env`)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/ai_search
OPENAI_API_KEY=sk-your-openai-key-here
EMBEDDING_MODEL=text-embedding-3-small
EMBED_DIM=1536

```

---

## Usage

### 1. Start Backend

```bash
# inside /backend (ensure venv is active)
uvicorn app.main:app --reload --port 8000

```

### 2. Start Frontend

You can open `frontend/index.html` directly, or serve it to avoid CORS issues:

```bash
# inside /frontend
python3 -m http.server 8080

```

### 3. Workflow

1. Open `http://localhost:8080` in your browser.
2. **Upload:** Drag and drop a PDF into the sidebar.
3. **Ingest:** Watch the terminal for the ingestion report.
4. **Chat:** Ask questions like *"What is the main conclusion of this paper?"*

---

## Database Maintenance

The project includes powerful scripts in `backend/scripts/` to manage your data:

| Script | Description |
| --- | --- |
| `reset_db.py` | **Warning:** Wipes all documents and chunks from the database and recreates tables. |
| `inspect_db.py` | Shows current row counts and vector index status. |
| `repair_index.py` | Forces a re-indexing of the vector column if searches become slow. |
| `backfill_embeddings.py` | Generates embeddings for chunks that might have failed initially. |

**Example:**

```bash
python backend/scripts/inspect_db.py

```

---

## License

MIT License