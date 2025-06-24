import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load facts
with open("app/data/fact_dataset.json", "r") as f:
    facts = json.load(f)

corpus = [item["text"] for item in facts]
embeddings = model.encode(corpus)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

def get_context(query: str):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), 5)
    return [facts[i] for i in I[0]]
