import streamlit as st
import fitz  # PyMuPDF
import faiss
import numpy as np
import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# ---------- CONFIG ---------- #
GEMINI_API_KEY = "your_google_api_key"
PDF_PATH = "data.pdf"

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Load local embedding model (for proposal similarity)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- LOAD & EMBED PROPOSALS ---------- #
@st.cache_resource
def load_proposals():
    doc = fitz.open(PDF_PATH)
    text = ""
    for page in doc:
        text += page.get_text()
    # Assuming each proposal is separated by a line or heading
    proposals = text.split("\n\n")  # Adjust based on real format
    return [p.strip() for p in proposals if len(p.strip()) > 100]

@st.cache_resource
def embed_proposals(proposals):
    vectors = embed_model.encode(proposals)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(np.array(vectors))
    return index, vectors, proposals

proposals = load_proposals()
index, vectors, raw_proposals = embed_proposals(proposals)

# ---------- STREAMLIT UI ---------- #
st.title("💼 Upwork Proposal Generator (Gemini 1.5 Flash)")
job_post = st.text_area("Paste the Upwork job post:", height=300)

if st.button("Generate Proposal"):
    if not job_post.strip():
        st.warning("Please paste a job post to proceed.")
    else:
        # Embed job post
        job_vector = embed_model.encode([job_post])
        scores, indices = index.search(np.array(job_vector), 3)

        # Retrieve top proposals
        similar_proposals = "\n---\n".join([raw_proposals[i] for i in indices[0]])

        # Gemini prompt
        prompt = f"""
You are a professional Upwork proposal writer.

Below is a new job post. After that, you’ll see some similar past proposals.

Write a new custom proposal that reflects the tone and structure of these examples.

Job Post:
{job_post}

Relevant Proposals:
{similar_proposals}

Now write a tailored proposal that sounds natural, strategic, and client-focused.
"""

        with st.spinner("Generating proposal..."):
            response = model.generate_content(prompt)
            st.subheader("📄 Generated Proposal")
            st.markdown(response.text)
