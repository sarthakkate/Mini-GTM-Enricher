from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd
import io
from .database import get_db, engine
from . import models, schemas, worker

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dashboard connectivity ke liye CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload", response_model=schemas.BatchResponse)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode("utf-8")))
    
    if "domain" not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must contain a 'domain' column")

    domains = df["domain"].tolist()

    new_batch = models.EnrichmentBatch(filename=file.filename, status="processing")
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)

    # Celery task trigger
    worker.enrich_companies_task.delay(str(new_batch.id), domains)

    return new_batch

@app.get("/batch/{batch_id}")
def get_batch(batch_id: str, db: Session = Depends(get_db)):
    batch = db.query(models.EnrichmentBatch).filter(models.EnrichmentBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    # Ye part results dashboard pe bhejta hai
    results = db.query(models.Company).filter(models.Company.batch_id == batch_id).all()
    
    return {
        "id": batch.id,
        "status": batch.status,
        "results": results
    }