import sys, os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db import get_conn

def inspect():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) as null_embeds FROM chunks WHERE embedding IS NULL")
            result = cur.fetchone()
            nulls = result['null_embeds'] if result else 0
            print(f"⚠️  Chunks with NULL embeddings: {nulls} (Should be 0)")

            print("\nFirst 5 Chunks of Content:")
            cur.execute("""
                SELECT d.title, c.chunk_index, c.content, c.embedding 
                FROM chunks c 
                JOIN documents d ON c.document_id = d.id 
                LIMIT 5
            """)
            rows = cur.fetchall()
            
            if not rows:
                print("Query returned 0 rows! (Table might be empty or RLS is blocking)")
                return
            
            for row in rows:
                is_valid = row['embedding'] is not None
                has_vector = " Vector Present" if is_valid else " NULL VECTOR"
                
                content_preview = (row['content'] or "")[:50].replace('\n', ' ')
                
                print(f"   [{row['chunk_index']}] {row['title'][:20]}... | {has_vector} | \"{content_preview}...\"")

if __name__ == "__main__":
    inspect()