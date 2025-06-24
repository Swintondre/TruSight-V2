# app/main.py
from aggregator import aggregate_facts
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from retriever.retriever import FactRetriever, build_faiss_index_from_facts
import subprocess 
import threading
import fact_updater  # assuming it's in the same directory as main.py
import json

# Start fact updater in background
threading.Thread(target=fact_updater.run, daemon=True).start()

subprocess.Popen(["python", "fact_updater.py"])

app = FastAPI(title="TruthScore Hybrid API")
retriever = FactRetriever()
print("🌐 Auto-enriching from fact sources...")
enriched_facts = aggregate_facts(limit_per_source=30)
build_faiss_index_from_facts(enriched_facts)  # this updates FAISS
print(f"✅ Enriched with {len(enriched_facts)} facts")

class ClaimRequest(BaseModel):
    claim: str
    top_k: int = 5

@app.get("/")
def root():
    return {"message": "Hybrid backend is active."}

@app.post("/verify_claim")
def verify_claim(data: ClaimRequest):
    claim = data.claim.strip()
    relevant_facts = retriever.query(claim, top_k=data.top_k)

    try:
        # Step 1: Format prompt with retrieved facts
        context = "\n".join(f"- {fact}" for fact in relevant_facts)
        prompt = f"""Evaluate the following claim for truthfulness using the listed context facts.
Claim: "{claim}"

Context:
{context}

Respond with:
1. A judgment (True, False, or Uncertain)
2. A 0-100 confidence score
3. A brief explanation
"""

        # Step 2: Call local LLM via Ollama using subprocess
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        output = result.stdout.strip()

        # Step 3: Heuristic score extraction (simplified)
        score = next((int(s) for s in output.split() if s.isdigit() and 0 <= int(s) <= 100), 50)

        return {
            "claim": claim,
            "truth_score": score,
            "verdict": "Hybrid LLM",
            "explanation": output,
            "sources": relevant_facts
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
