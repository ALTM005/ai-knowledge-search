import os, math
from app.db import get_conn
from app.services.embeddings import embed_texts

BATCH = 64

def main():
    total_done = 0
    while True:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT id, content
                FROM chunks
                WHERE embedding IS NULL
                ORDER BY id
                LIMIT %s
            """, (BATCH,))
            rows = cur.fetchall()

            if not rows:
                print("No more rows to backfill.")
                break

            texts = [r["content"] or "" for r in rows]
            vecs = embed_texts(texts)
            if len(vecs) != len(rows):
                raise RuntimeError("Embedding count mismatch")

            for r, v in zip(rows, vecs):
                cur.execute("UPDATE chunks SET embedding = %s WHERE id = %s", (v, r["id"]))

            total_done += len(rows)
            print(f"Updated {total_done} rows so far...")

if __name__ == "__main__":
    main()
