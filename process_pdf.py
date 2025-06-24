import fitz  # PyMuPDF

def extract_proposals_from_pdf(pdf_path="data.pdf"):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    proposals = full_text.split("Proposal #")  # Adjust split logic as needed
    proposals = ["Proposal #" + p.strip() for p in proposals if p.strip()]
    return proposals
