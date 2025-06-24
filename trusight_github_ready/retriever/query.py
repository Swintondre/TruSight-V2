from app.retriever.llm import run_llm_with_context
from app.retriever.search import get_context

def verify_claim(claim: str):
    context = get_context(claim)
    score, explanation = run_llm_with_context(claim, context)
    return {
        "claim": claim,
        "truth_score": score,
        "explanation": explanation,
        "sources": context
    }
