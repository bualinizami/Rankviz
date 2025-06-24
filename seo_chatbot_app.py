import os
import fitz  # PyMuPDF
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load all PDF text from ./data/
@st.cache_data
def load_pdf_contexts(folder_path="data.pdf"):
    context_texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            doc = fitz.open(os.path.join(folder_path, filename))
            text = ""
            for page in doc:
                text += page.get_text()
            context_texts.append(text)
    return "\n\n".join(context_texts)

pdf_context = load_pdf_contexts()

# Prompt Template
def build_prompt(job_post, context):
    return f"""
You are an experienced SEO proposal writer. Write a concise, natural-sounding proposal for the following job post. Use real examples from the provided past proposals.

Job Post:
{job_post}

Past Proposals (Reference Only):
{context}

Rules:
- Do NOT use phrases like "I'm thrilled" or generic openings.
- Start with: "Based on your requirements..." or similar alternatives.
- Keep it under 200 words.
- Use only examples from the reference context above.
- End with a clear call to action.

Proposal:
"""

# Streamlit App UI
st.set_page_config(page_title="SEO Proposal Generator (Gemini)", layout="wide")
st.title("📄 SEO Proposal Generator (Gemini)")

job_post = st.text_area("🔍 Job Post", height=300, placeholder="Paste a job post here...")

if st.button("Generate Proposal"):
    if not job_post.strip():
        st.warning("Please enter a job post.")
    else:
        with st.spinner("Generating..."):
            prompt = build_prompt(job_post, pdf_context)
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            st.success("✅ Proposal Generated!")
            st.markdown(response.text)
