import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

with open("texts.json", "r") as f:
    texts = json.load(f)

index = faiss.read_index("index.faiss")

model = SentenceTransformer("all-MiniLM-L6-V2")

def retrieve_chunks(query, top_k=3):
    query_vec = model.encode([query]).astype("float32")
    D, I = index.search(np.array(query_vec), top_k)
    return [texts[i] for i in I[0]]

