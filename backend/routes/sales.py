"""Sales Module routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.database import get_db, Lead
from backend.models.schemas import LeadCreate, LeadUpdate, LeadScoringRequest
from backend.services.ai_service import ai_service
import random

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/leads")
async def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead"""
    # Score the lead using AI
    score_result = await ai_service.score_lead(lead.dict())
    
    db_lead = Lead(
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        company=lead.company,
        industry=lead.industry,
        budget=lead.budget,
        source=lead.source,
        score=score_result["score"]
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    return {
        "lead": db_lead,
        "scoring": score_result
    }

@router.get("/leads")
async def get_leads(status: str = None, db: Session = Depends(get_db)):
    """Get all leads"""
    query = db.query(Lead)
    if status:
        query = query.filter(Lead.status == status)
    return query.order_by(Lead.score.desc()).all()

@router.get("/leads/{lead_id}")
async def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get specific lead"""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.put("/leads/{lead_id}")
async def update_lead(lead_id: int, update: LeadUpdate, db: Session = Depends(get_db)):
    """Update lead"""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    if update.score is not None:
        lead.score = update.score
    if update.status:
        lead.status = update.status
    if update.notes:
        lead.notes = update.notes
    
    db.commit()
    db.refresh(lead)
    return lead

@router.post("/score-lead")
async def score_lead(request: LeadScoringRequest):
    """Score a lead using AI"""
    result = await ai_service.score_lead(request.dict())
    return result

@router.get("/forecast")
async def get_forecast(db: Session = Depends(get_db)):
    """Get sales forecast"""
    # Get historical data (simulated)
    leads = db.query(Lead).all()
    total_budget = sum(lead.budget for lead in leads)
    
    # Generate forecast
    historical_data = [
        total_budget * random.uniform(0.7, 0.9),
        total_budget * random.uniform(0.75, 0.95),
        total_budget * random.uniform(0.8, 1.0),
        total_budget
    ]
    
    forecast_result = await ai_service.generate_forecast(historical_data)
    
    return {
        "current_pipeline": total_budget,
        "forecast": forecast_result,
        "high_value_leads": db.query(Lead).filter(Lead.score > 70).count()
    }

@router.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    """Get sales dashboard data"""
    leads = db.query(Lead).all()
    
    total_leads = len(leads)
    new_leads = db.query(Lead).filter(Lead.status == "New").count()
    qualified = db.query(Lead).filter(Lead.status == "Qualified").count()
    converted = db.query(Lead).filter(Lead.status == "Converted").count()
    
    total_pipeline = sum(lead.budget for lead in leads)
    avg_score = sum(lead.score for lead in leads) / total_leads if total_leads > 0 else 0
    
    # Group by industry
    industries = {}
    for lead in leads:
        industries[lead.industry] = industries.get(lead.industry, 0) + 1
    
    return {
        "total_leads": total_leads,
        "new_leads": new_leads,
        "qualified_leads": qualified,
        "converted_leads": converted,
        "conversion_rate": round((converted / total_leads * 100) if total_leads > 0 else 0, 2),
        "total_pipeline": round(total_pipeline, 2),
        "average_score": round(avg_score, 2),
        "industries": industries
    }
