import streamlit as st
from process_pdf import extract_proposals_from_pdf
from embed_store import build_faiss_index, get_embeddings
from generate_proposal import generate_proposal
import numpy as np

st.set_page_config(page_title="Proposal Generator", layout="centered")

st.title("📄 Upwork Proposal Generator (Rankviz)")
job_input = st.text_area("Paste a job description here:", height=250)

@st.cache_resource
def setup():
    proposals = extract_proposals_from_pdf("data.pdf")  # Changed to "data.pdf"
    index, embeddings = build_faiss_index(proposals)
    return proposals, index, embeddings

proposals, index, embeddings = setup()

if st.button("Generate Proposal"):
    if not job_input.strip():
        st.warning("Please paste a job description.")
    else:
        job_emb = get_embeddings([job_input])[0]
        _, indices = index.search(np.array([job_emb]), k=5)
        similar = [proposals[i] for i in indices[0]]

        final_output = generate_proposal(job_input, similar)
        st.subheader("✍️ Generated Proposal")
        st.write(final_output)
