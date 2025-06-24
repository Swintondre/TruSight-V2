
import subprocess
import json

def run_mistral_judgment(claim, facts):
    context = "\n".join(f"- {fact}" for fact in facts)
    prompt = f"""You are a fact-checking assistant. Determine the veracity of the following claim based on the facts.

Claim: "{claim}"

Facts:
{context}

Instructions:
1. Return "True", "False", or "Uncertain"
2. Return a confidence score 0-100
3. Return a short justification

Respond in JSON with keys: "verdict", "score", "explanation"""

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        response = json.loads(result.stdout)
        return response.get("score", 50), response.get("verdict", "Uncertain"), response.get("explanation", "Unknown")
    except Exception as e:
        return 50, "Uncertain", f"LLM error: {e}"
