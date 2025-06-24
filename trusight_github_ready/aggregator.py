# app/enrichment/scrapers/aggregator.py

from enrichment.scrapers.politifact import fetch_politifact_claims
from enrichment.scrapers.factcheck import fetch_factcheck_claims
from enrichment.scrapers.healthfeedback import fetch_healthfeedback_claims
from enrichment.scrapers.snopes import fetch_snopes_claims
from enrichment.scrapers.fullfact import fetch_fullfact_claims
from enrichment.scrapers.scicheck import fetch_scicheck_claims

def aggregate_facts(limit_per_source=25):
    all_facts = []

    try:
        print("\U0001f50d  Fetching PolitiFact...")
        all_facts.extend(fetch_politifact_claims(limit=limit_per_source))
    except Exception as e:
        print(f"\u274c PolitiFact failed: {e}")

    try:
        print("\U0001f50d  Fetching FactCheck.org...")
        all_facts.extend(fetch_factcheck_claims(limit=limit_per_source))
    except Exception as e:
        print(f"\u274c FactCheck.org failed: {e}")

    try:
        print("\U0001f50d  Fetching HealthFeedback.org...")
        all_facts.extend(fetch_healthfeedback_claims(limit=limit_per_source))
    except Exception as e:
        print(f"\u274c HealthFeedback failed: {e}")

    try:
        print("\U0001f50d  Fetching Snopes.com...")
        all_facts.extend(fetch_snopes_claims(limit=limit_per_source))
    except Exception as e:
        print(f"\u274c Snopes failed: {e}")

    try:
        print("\U0001f50d  Fetching FullFact.org...")
        all_facts.extend(fetch_fullfact_claims(limit=limit_per_source))
    except Exception as e:
        print(f"\u274c FullFact failed: {e}")

    try:
        print("\U0001f50d  Fetching SciCheck...")
        all_facts.extend(fetch_scicheck_claims(limit=limit_per_source))
    except Exception as e:
        print(f"\u274c SciCheck failed: {e}")

    return all_facts
