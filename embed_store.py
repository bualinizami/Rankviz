import faiss
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

embedding_model = genai.embed_content

def get_embeddings(texts):
    embeddings = []
    for text in texts:
        result = embedding_model(model="models/embedding-001", content=text, task_type="retrieval_document")
        embeddings.append(np.array(result['embedding'], dtype='float32'))
    return embeddings

def build_faiss_index(texts):
    embeddings = get_embeddings(texts)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    return index, embeddings
