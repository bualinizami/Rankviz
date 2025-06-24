import os
import time
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load .env for Gemini API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini LLM and Embeddings
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY, temperature=0.4)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)

# Load and process PDFs from ./data
@st.cache_resource
def load_vector_store():
    loader = PyPDFDirectoryLoader("./data")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(texts, embeddings)
    return vectorstore

retriever = load_vector_store().as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Streamlit UI
st.set_page_config(page_title="SEO Proposal Generator (Gemini)", layout="wide")
st.title("📄 SEO Proposal Generator (Gemini)")

st.write("Upload your past proposals in the `/data` folder (PDFs), then paste a job post to get a tailored SEO proposal.")

job_post = st.text_area("🔍 Job Post", height=300, placeholder="Paste a job post from Upwork or elsewhere...")

if st.button("Generate Proposal"):
    if not job_post.strip():
        st.warning("Please paste a job post.")
    else:
        with st.spinner("Generating proposal with Gemini..."):
            query = f"""
Write a personalized, 150–200 word SEO proposal for the following job post:
---
{job_post}
---
Use real examples from the reference documents (PDFs). 
Avoid generic phrases like 'I'm thrilled' or 'As a seasoned professional'.
Structure it clearly with a greeting, brief strategy, and call to action.
"""
            start = time.time()
            result = qa_chain.run(query)
            end = time.time()

            st.success("✅ Proposal Generated!")
            st.markdown(result)
            st.caption(f"⏱️ Time taken: {end - start:.2f} seconds")
