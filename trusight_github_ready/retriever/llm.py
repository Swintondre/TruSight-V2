import subprocess
import json

def run_llm_with_context(claim, sources):
    context = "\n".join([f"{s['text']}" for s in sources])
    prompt = f"""Evaluate the following claim for truthfulness:

Claim: {claim}

Sources:
{context}

Respond in JSON:
{{
  "verdict": "...",
  "score": ...,
  "explanation": "..."
}}
"""

    result = subprocess.run(
        ["ollama", "run", "mistral", prompt],
        capture_output=True, text=True
    )
    try:
        output = json.loads(result.stdout.strip().split('
')[-1])
        return output.get("score", 50), output.get("explanation", "No explanation found.")
    except Exception:
        return 50, "Could not parse LLM output."
