import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from .web_search import search_web
from typing import List, Union

def build_faiss_index_from_facts(facts):
    print("⚙️  Building FAISS index from fetched facts...")

    texts = [fact["claim"] for fact in facts if "claim" in fact]
    if not texts:
        print("❌ No valid claims found. Aborting FAISS index build.")
        return

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts)

    # Safeguard: Check if embeddings exist and are usable
    if embeddings is None or len(embeddings) == 0 or (
        hasattr(embeddings, "shape") and embeddings.shape[0] == 0
    ):
        print("❌ Embeddings could not be generated or are empty.")
        return

    embeddings = np.array(embeddings, dtype="float32")
    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(1, -1)


    print("✅ Embedding shape:", embeddings.shape)

    # Save FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    print("✅ Embedding shape before FAISS add:", embeddings.shape)
    print("✅ Embedding dtype:", embeddings.dtype)
    print("✅ Is np array:", isinstance(embeddings, np.ndarray))
    print("✅ FAISS index dim:", index.d)
    index.add(np.asarray(embeddings, dtype=np.float32))
    faiss.write_index(index, "data/fact_index.faiss")

    # Save facts as text JSON
    with open("data/fact_texts.json", "w", encoding="utf-8") as f:
        json.dump(facts, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(facts)} facts to FAISS and JSON.")


class FactRetriever:
    def __init__(self, index_path=None, facts_path=None):
        base_dir = os.path.dirname(__file__)
        data_dir = os.path.join(base_dir, "..", "data")

        index_path = index_path or os.path.join(data_dir, "fact_index.faiss")
        facts_path = facts_path or os.path.join(data_dir, "fact_texts.json")

        print("🔍 Initializing FactRetriever...")

        self.index = faiss.read_index(index_path)

        with open(facts_path, "r", encoding="utf-8") as f:
            self.facts = json.load(f)

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ Retriever ready.")

def query(self, claim: str, top_k: int = 5) -> List[str]:
    embedding = self.model.encode([claim])
    D, I = self.index.search(np.array(embedding).astype("float32"), top_k)

    # Retrieve top local facts
    results = [self.facts[i] for i in I[0] if i < len(self.facts)]

    # Optional: fallback to web if not enough relevant facts
    if len(results) < top_k:
        print("🌐 Not enough local facts, using Serper Web API...")
        web_results = search_web(claim, num_results=top_k)
        for item in web_results:
            snippet = item.get("snippet", "")
            if snippet:
                results.append(snippet)

    return results

