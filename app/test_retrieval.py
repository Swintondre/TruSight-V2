from retriever.retriever import FactRetriever

retriever = FactRetriever()

results = retriever.query("Do cats glow under blacklight?", top_k=3)

print("\nTop relevant facts:")
for i, fact in enumerate(results, 1):
    print(f"{i}. {fact}")
