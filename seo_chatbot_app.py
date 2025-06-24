import streamlit as st
import google.generativeai as genai
import os

# Use API key from Streamlit Secrets or .env fallback
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit page settings
st.set_page_config(page_title="SEO Proposal Generator", layout="centered")
st.title("📄 SEO Proposal Generator (Gemini)")

st.write("Paste a job post and get a high-quality SEO proposal tailored to the client’s requirements.")

job_post = st.text_area("🔍 Job Post", height=300, placeholder="Paste an SEO-related job post from Upwork or another platform")

if st.button("Generate Proposal"):
    if not job_post.strip():
        st.warning("⚠️ Please enter a job post.")
    else:
        with st.spinner("Generating proposal using Gemini..."):
            prompt = f"""
You are an experienced SEO professional writing short, natural-sounding proposals for freelance clients.

Write a concise and personalized proposal (max 200 words) for the following job post:

---
{job_post}
---

**Proposal rules:**
- DO NOT use phrases like "I'm thrilled", "I'm excited", or "as a seasoned expert"
- Start with: "Based on your requirements...", or "After reviewing your needs..."
- Be conversational but professional
- Suggest 3–4 specific next steps
- End with a clear, low-pressure call to action

Only respond with the proposal — no headers or extra commentary.
"""
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            st.success("✅ Proposal Generated!")
            st.markdown(response.text)
