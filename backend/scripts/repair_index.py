import sys, os
import psycopg

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db import get_conn
from app.services.embeddings import embed_texts

def repair_index():
    print(" STARTING INDEX REPAIR...")
    
    conn = get_conn()
    conn.autocommit = True

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) as c FROM chunks")
            count = cur.fetchone()['c']
            print(f"Rows in DB: {count}")
            
            if count == 0:
                print("DB is empty! You need to re-upload the file.")
                return

            print(" Dropping potential corrupted indexes...")
            cur.execute("DROP INDEX IF EXISTS chunks_embedding_idx;")
            cur.execute("DROP INDEX IF EXISTS chunks_embedding_cosine_idx;")
            print("    Indexes dropped. Database is now in 'Manual Search' mode.")

            print("\n Testing Search without Index...")
            query = "What is the conclusion?"
            vec = embed_texts([query])[0]

            cur.execute("""
                SELECT content, 1 - (embedding <=> %s::vector) as score 
                FROM chunks 
                ORDER BY embedding <=> %s::vector 
                LIMIT 1;
            """, (vec, vec))
            
            row = cur.fetchone()
            if row:
                print(f"   FOUND MATCH! Score: {row['score']:.4f}")
                print(f"   snippet: {row['content'][:50]}...")
                print("\n REPAIR SUCCESSFUL. The API will work now.")
            else:
                print(" Still 0 rows. This is a data/embedding mismatch.")

    except Exception as e:
        print(f" Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    repair_index()