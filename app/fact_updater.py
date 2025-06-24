# fact_updater.py

FACT_INDEX_PATH = "data/fact_index.faiss"
LOG_FILE_PATH = "data/factflow.log"

import time
from aggregator import aggregate_facts
from retriever.retriever import build_faiss_index_from_facts
import os
import json
from dotenv import load_dotenv
from aggregator import aggregate_facts
from utils.model import load_model
from utils.tokenizer import load_tokenizer
from retriever.web_search import search_web as fetch_web_results
from build_index.save import save_index

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def log_event(message: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

def run():
    while True:
        print("🔁 [Auto Update] Aggregating facts and updating FAISS...")
        log_event("[Auto Update] Aggregating facts and updating FAISS...")

        enriched = aggregate_facts(limit_per_source=30)
        build_faiss_index_from_facts(enriched)

        print("✅ Fact index refreshed.")
        log_event("Fact index refreshed.")

        time.sleep(900)  # 15 minutes

def run_fact_update():
    print("🧠 Aggregating facts from scrapers...")
    log_event("Aggregating facts from scrapers...")
    scraped_facts = aggregate_facts(limit_per_source=30)

    print("🔎 Fetching supplemental context from Serper...")
    log_event("Fetching supplemental context from Serper...")
    web_facts = fetch_web_results("latest fact-checked misinformation", num_results=10)

    all_facts = scraped_facts + web_facts
    print(f"📊 Total facts gathered: {len(all_facts)}")
    log_event(f"Total facts gathered: {len(all_facts)}")

    print("📦 Saving combined facts to JSON...")
    log_event("Saving combined facts to JSON...")
    os.makedirs("data", exist_ok=True)
    with open("data/aggregated_facts.json", "w", encoding="utf-8") as f:
        json.dump(all_facts, f, indent=2, ensure_ascii=False)

    print("📈 Building FAISS index...")
    log_event("Building FAISS index...")
    tokenizer = load_tokenizer()
    model = load_model()
    save_index(all_facts, tokenizer, model, index_path=FACT_INDEX_PATH)

    print("✅ Fact index updated successfully.")
    log_event("Fact index updated successfully.")

if __name__ == "__main__":
    run()  # ✅ This runs the infinite loop with a 15-minute update cycle
