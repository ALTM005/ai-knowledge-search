import sys, os
import psycopg

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.services.embeddings import embed_texts
from app.db import get_conn

def nuclear_test():
    query = "How is AI transforming cybersecurity?"
    print(f"NUCLEAR SEARCH TEST")
    print(f"Query: {query}")

    try:
        vecs = embed_texts([query])
        vector = vecs[0]
        dim = len(vector)
        print(f"Generated Embedding. Dimensions: {dim}")
        
        if dim != 1536:
            print(f"CRITICAL ERROR: Expected 1536 dimensions, got {dim}.")
            print("   (Did you change the embedding model in .env or OpenAI?)")
            return
            
    except Exception as e:
        print(f"Embedding Generation Failed: {e}")
        return

    vector_str = str(vector)

    sql = f"""
    SELECT id, content, 1 - (embedding <=> '{vector_str}'::vector) as score 
    FROM chunks 
    ORDER BY embedding <=> '{vector_str}'::vector 
    LIMIT 3;
    """

    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            
            print(f"\n SQL Results: {len(rows)} rows found")
            
            if not rows:
                print("Still 0 rows. This means the vectors in the DB are incompatible.")
                cur.execute("SELECT vector_dims(embedding) FROM chunks LIMIT 1;")
                db_dim = cur.fetchone()['vector_dims']
                print(f"DB Vector Dimension: {db_dim}")
            
            for row in rows:
                print(f"   [Score: {row['score']:.4f}] {row['content'][:60]}...")
                
    except Exception as e:
        print(f"SQL Execution Failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    nuclear_test()