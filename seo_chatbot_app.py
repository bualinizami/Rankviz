import os
import time
import streamlit as st
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load OpenAI Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup OpenAI and LangChain
llm = ChatOpenAI(model_name="gpt-4", temperature=0.4, openai_api_key=OPENAI_API_KEY)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Load and vectorize your PDF proposals
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

# Streamlit App UI
st.set_page_config(page_title="SEO Proposal Generator", layout="wide")
st.title("📄 LangChain SEO Proposal Generator")

st.write("Upload your past proposals in the `/data` folder (PDFs), then paste a job post to get a tailored SEO proposal.")

job_post = st.text_area("🔍 Job Post", height=300, placeholder="Paste a job post from Upwork or elsewhere...")

if st.button("Generate Proposal"):
    if not job_post.strip():
        st.warning("Please paste a job post.")
    else:
        with st.spinner("Generating proposal..."):
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
import os
import time
import streamlit as st
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Load OpenAI Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup OpenAI and LangChain
llm = ChatOpenAI(model_name="gpt-4", temperature=0.4, openai_api_key=OPENAI_API_KEY)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Load and vectorize your PDF proposals
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

# Streamlit App UI
st.set_page_config(page_title="SEO Proposal Generator", layout="wide")
st.title("📄 LangChain SEO Proposal Generator")

st.write("Upload your past proposals in the `/data` folder (PDFs), then paste a job post to get a tailored SEO proposal.")

job_post = st.text_area("🔍 Job Post", height=300, placeholder="Paste a job post from Upwork or elsewhere...")

if st.button("Generate Proposal"):
    if not job_post.strip():
        st.warning("Please paste a job post.")
    else:
        with st.spinner("Generating proposal..."):
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
