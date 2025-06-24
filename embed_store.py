import faiss
import numpy as np
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embeddings(texts):
    embeddings = []
    for text in texts:
        try:
            response = openai.embeddings.create(
                input=text[:3000],
                model="text-embedding-3-small"
            )
            emb = np.array(response.data[0].embedding, dtype='float32')
            embeddings.append(emb)
        except Exception as e:
            print("Embedding error:", e)
            embeddings.append(np.zeros(1536, dtype='float32'))  # OpenAI embedding size
    return embeddings

def build_faiss_index(texts):
    embeddings = get_embeddings(texts)
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index, embeddings
