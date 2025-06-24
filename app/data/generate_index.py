import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

with open("cleaned_facts.json", "r") as f:
    raw_data = json.load(f)

facts = [entry["facts"] for entry in raw_data if "facts" in entry]
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(facts)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

faiss.write_index(index, "fact_index.faiss")

with open("fact_texts.json", "w") as f:
    json.dump(facts, f)

print("✅ FAISS index and facts saved.")
