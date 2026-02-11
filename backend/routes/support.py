"""Customer Support routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.database import get_db, SupportTicket
from backend.models.schemas import TicketCreate, TicketUpdate, TicketClassificationRequest
from backend.services.ai_service import ai_service

router = APIRouter(prefix="/support", tags=["Support"])

@router.post("/tickets")
async def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """Create a new support ticket"""
    # Classify the ticket using AI
    classification = await ai_service.classify_ticket(ticket.message)
    
    db_ticket = SupportTicket(
        customer_name=ticket.customer_name,
        email=ticket.email,
        subject=ticket.subject,
        message=ticket.message,
        category=classification["category"],
        priority=classification["priority"],
        ai_response=classification["suggested_response"]
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.get("/tickets")
async def get_tickets(status: str = None, db: Session = Depends(get_db)):
    """Get all support tickets"""
    query = db.query(SupportTicket)
    if status:
        query = query.filter(SupportTicket.status == status)
    return query.all()

@router.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Get specific ticket"""
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.put("/tickets/{ticket_id}")
async def update_ticket(ticket_id: int, update: TicketUpdate, db: Session = Depends(get_db)):
    """Update ticket status or response"""
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if update.status:
        ticket.status = update.status
    if update.ai_response:
        ticket.ai_response = update.ai_response
    
    db.commit()
    db.refresh(ticket)
    return ticket

@router.post("/classify")
async def classify_ticket(request: TicketClassificationRequest):
    """Classify ticket using AI"""
    result = await ai_service.classify_ticket(request.ticket_text)
    return result

@router.post("/generate-reply/{ticket_id}")
async def generate_reply(ticket_id: int, db: Session = Depends(get_db)):
    """Generate AI reply for ticket"""
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    prompt = f"Generate a professional reply to this support ticket:\n\nSubject: {ticket.subject}\n\nMessage: {ticket.message}"
    context = "You are a customer support representative. Provide helpful, empathetic responses."
    
    reply = await ai_service.generate_response(prompt, context)
    
    ticket.ai_response = reply
    db.commit()
    
    return {"ticket_id": ticket_id, "reply": reply}

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get support statistics"""
    total = db.query(SupportTicket).count()
    open_tickets = db.query(SupportTicket).filter(SupportTicket.status == "Open").count()
    resolved = db.query(SupportTicket).filter(SupportTicket.status == "Resolved").count()
    
    return {
        "total_tickets": total,
        "open": open_tickets,
        "resolved": resolved,
        "resolution_rate": round((resolved / total * 100) if total > 0 else 0, 2)
    }
