import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load the dataset
with open("cleaned_facts.json", "r") as f:
    raw_data = json.load(f)

# Extract facts using the correct key
facts = [entry["facts"] for entry in raw_data if "facts" in entry]

print(f"✔️ Loaded {len(facts)} facts")

# Generate embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(facts)

if len(embeddings) == 0:
    raise ValueError("🚫 No embeddings were generated. Check that the input data is valid.")

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

# Save index
faiss.write_index(index, "fact_index.faiss")

# Save texts for reference
with open("fact_texts.json", "w") as f:
    json.dump(facts, f)

print("✅ FAISS index and fact_texts.json saved successfully.")
