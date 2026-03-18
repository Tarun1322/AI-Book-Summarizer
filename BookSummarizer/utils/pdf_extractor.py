import io

def extract_pdf_text(file_obj):
    raw = file_obj.read()
    # Try PyPDF2 first
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(raw))
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        if text.strip():
            return text.strip()
    except Exception:
        pass
    # Try pdfplumber as fallback
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            text = "\n".join(p.extract_text() or "" for p in pdf.pages)
        if text.strip():
            return text.strip()
    except Exception:
        pass
    raise Exception("PDF could not be read. Please paste text manually.")
