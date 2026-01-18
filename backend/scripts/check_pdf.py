import os
import pdfplumber

pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/Computer Science Discourse Community Paper (1).pdf"))

print(f"📂 Checking File: {pdf_path}")

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"📄 Total Pages: {len(pdf.pages)}")
        
        full_text = ""
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                print(f"   -- Page {i+1}: Found {len(text)} characters.")
                full_text += text
            else:
                print(f"   -- Page {i+1}: ❌ NO TEXT FOUND (Likely an image)")
        
        print(f"\n📊 Total Text Length: {len(full_text)} characters")
        
        if len(full_text) < 200:
            print("\n🚨 CONCLUSION: This PDF is an image/scan. Python cannot read it without OCR.")
        else:
            print("\n✅ CONCLUSION: The PDF has text! The bug is in the database ingestion.")

except Exception as e:
    print(f"❌ Error reading file: {e}")