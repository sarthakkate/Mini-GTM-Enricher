import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database import Base

class EnrichmentBatch(Base):
    __tablename__ = "enrichment_batches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    filename = Column(String)

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(UUID(as_uuid=True), ForeignKey("enrichment_batches.id"))
    domain = Column(String, index=True)
    
    # Enrichment fields from Explorium
    industry = Column(String, nullable=True)
    company_size = Column(String, nullable=True)
    revenue_range = Column(String, nullable=True)
    enrichment_status = Column(String, default="not_started") # success, failed