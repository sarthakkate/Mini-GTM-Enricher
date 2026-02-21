import os
import requests
from celery import Celery
from dotenv import load_dotenv
from urllib.parse import urlparse
import re
from .database import SessionLocal
from .models import EnrichmentBatch, Company

load_dotenv() 

REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)
EXPLORIUM_API_KEY = os.getenv("EXPLORIUM_API_KEY")

def get_clean_domain(raw_input):
    try:
        raw_input = str(raw_input).lower().strip()
        if "://" in raw_input:
            domain = urlparse(raw_input).netloc
        else:
            domain = raw_input.split('/')[0]
        
        if "google" in domain and "q=" in raw_input:
            match = re.search(r'q=([^&]+)', raw_input)
            if match: domain = match.group(1)

        return domain.replace("www.", "").split(':')[0]
    except:
        return raw_input

@celery_app.task(bind=True, max_retries=3)
def enrich_companies_task(self, batch_id, domains):
    db = SessionLocal()
    try:
        batch = db.query(EnrichmentBatch).filter(EnrichmentBatch.id == batch_id).first()
        if not batch: return
        
        headers = {"API_KEY": EXPLORIUM_API_KEY, "Content-Type": "application/json"}

        for domain in domains:
            clean_domain = get_clean_domain(domain)
            if not clean_domain: continue
            
            try:
                match_url = "https://api.explorium.ai/v1/businesses/match"
                payload = {
                    "businesses_to_match": [
                        {"domain": clean_domain}
                    ]
                }
                
                match_res = requests.post(match_url, json=payload, headers=headers)
                
                if match_res.status_code == 200:
                    match_results = match_res.json().get("data", [])
                    biz_id = None
                    if match_results and len(match_results) > 0:
                        biz_id = match_results[0].get("business_id")

                    if biz_id:
                        enrich_url = f"https://api.explorium.ai/v1/businesses/{biz_id}/enrich"
                        enrich_res = requests.get(enrich_url, headers=headers)
                        enrich_data = enrich_res.json().get("data", {})

                        new_company = Company(
                            batch_id=batch_id,
                            domain=clean_domain,
                            industry=enrich_data.get("industry", "N/A"),
                            company_size=enrich_data.get("size_range", "N/A"),
                            revenue_range=enrich_data.get("revenue_range", "N/A"),
                            enrichment_status="success"
                        )
                    else:
                        new_company = Company(batch_id=batch_id, domain=clean_domain, enrichment_status="failed")
                else:
                    print(f"❌ API Error {match_res.status_code}: {match_res.text}")
                    new_company = Company(batch_id=batch_id, domain=clean_domain, enrichment_status="error")
                
                db.add(new_company)
                db.commit()

            except Exception as e:
                print(f"❌ Worker Loop Error: {e}")
                continue # Ye line zaroori hai error ke baad

        batch.status = "completed"
        db.commit()
    finally:
        db.close()