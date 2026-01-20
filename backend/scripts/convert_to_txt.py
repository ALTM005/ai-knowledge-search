import os
import pdfplumber

source_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
dest_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/clean_paper.txt"))

print(f"📖 Reading: {source_path}")

try:
    with pdfplumber.open(source_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n\n"
    
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"Success! Created 'clean_paper.txt' ({len(full_text)} chars).")
    print(f"Location: {dest_path}")

except Exception as e:
    print(f" Error: {e}")