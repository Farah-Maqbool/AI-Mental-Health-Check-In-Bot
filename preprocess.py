import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


with open("intents.json", "r") as f:
    talk = json.load(f)

#make chunks
documents = []
for i, talk in enumerate(talk):
    text = f"Tag: {talk["tag"]}\nPatterns: {talk["patterns"]}\nResponses: {talk["responses"]}"
    documents.append({"id": f"doc_{i}", "text" : text})

#select model
model = SentenceTransformer("all-MiniLM-L6-V2")

texts = [document["text"] for document in documents]

#make vectors
vectors = model.encode(texts)

vectors = np.array(vectors).astype("float32")


index = faiss.IndexFlatL2(vectors.shape[1])


index.add(vectors)

faiss.write_index(index, "index.faiss")

with open("texts.json","w") as f:
    json.dump(texts, f)