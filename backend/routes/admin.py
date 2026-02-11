"""Admin Module routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.models.database import get_db, Task
from backend.models.schemas import TaskCreate, TaskUpdate
from backend.services.ai_service import ai_service

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/tasks")
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks")
async def get_tasks(status: str = None, db: Session = Depends(get_db)):
    """Get all tasks"""
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    return query.order_by(Task.due_date).all()

@router.get("/tasks/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get specific task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}")
async def update_task(task_id: int, update: TaskUpdate, db: Session = Depends(get_db)):
    """Update task status"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if update.status:
        task.status = update.status
    
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

@router.post("/generate-email")
async def generate_email(subject: str, context: str):
    """Generate professional email using AI"""
    prompt = f"Write a professional email with subject: {subject}\nContext: {context}"
    email_context = "You are a professional business communication assistant. Write clear, concise emails."
    
    email = await ai_service.generate_response(prompt, email_context)
    return {"email": email}

@router.get("/reminders")
async def get_reminders(db: Session = Depends(get_db)):
    """Get upcoming task reminders"""
    now = datetime.utcnow()
    upcoming_tasks = db.query(Task).filter(
        Task.due_date >= now,
        Task.status != "Completed"
    ).order_by(Task.due_date).limit(10).all()
    
    reminders = []
    for task in upcoming_tasks:
        days_until = (task.due_date - now).days
        reminders.append({
            "task_id": task.id,
            "title": task.title,
            "due_date": task.due_date,
            "days_until": days_until,
            "priority": task.priority
        })
    
    return reminders

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get admin statistics"""
    total = db.query(Task).count()
    pending = db.query(Task).filter(Task.status == "Pending").count()
    in_progress = db.query(Task).filter(Task.status == "In Progress").count()
    completed = db.query(Task).filter(Task.status == "Completed").count()
    
    return {
        "total_tasks": total,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
        "completion_rate": round((completed / total * 100) if total > 0 else 0, 2)
    }
