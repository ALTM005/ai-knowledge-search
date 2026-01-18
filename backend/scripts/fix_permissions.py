import sys, os
import psycopg

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db import get_conn

def fix_permissions():
    print("Attempting to disable Row Level Security (RLS)...")
    
    try:
        conn = get_conn()
        conn.autocommit = True
        
        with conn.cursor() as cur:
            cur.execute("ALTER TABLE documents DISABLE ROW LEVEL SECURITY;")
            print("Disabled RLS on 'documents' table")
            
            cur.execute("ALTER TABLE chunks DISABLE ROW LEVEL SECURITY;")
            print("Disabled RLS on 'chunks' table")
            
            cur.execute("GRANT ALL ON documents TO postgres;")
            cur.execute("GRANT ALL ON documents TO service_role;")
            cur.execute("GRANT ALL ON chunks TO postgres;")
            cur.execute("GRANT ALL ON chunks TO service_role;")
            print("Granted explicit permissions")

        conn.close()
        print("\nSUCCESS: Database is now fully readable by the API.")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("Tip: If this fails, go to Supabase Dashboard -> SQL Editor and run:")
        print("ALTER TABLE documents DISABLE ROW LEVEL SECURITY;")
        print("ALTER TABLE chunks DISABLE ROW LEVEL SECURITY;")

if __name__ == "__main__":
    fix_permissions()