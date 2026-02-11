"""HR Module routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta, timezone
import random
from backend.models.database import get_db, Employee, Attendance, LeaveRequest
from backend.models.schemas import (
    EmployeeCreate, AttendanceCreate, LeaveRequestCreate, ResumeAnalysisRequest
)
from backend.services.ai_service import ai_service

router = APIRouter(prefix="/hr", tags=["HR"])

@router.post("/employees")
async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee"""
    db_employee = Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        position=employee.position,
        salary=employee.salary,
        hire_date=datetime.now(timezone.utc)
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/employees")
async def get_employees(db: Session = Depends(get_db)):
    """Get all employees"""
    return db.query(Employee).all()

@router.post("/attendance")
async def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    """Record attendance"""
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.get("/attendance/simulate")
async def simulate_attendance(db: Session = Depends(get_db)):
    """Simulate attendance for all employees"""
    employees = db.query(Employee).all()
    today = datetime.now(timezone.utc).date()
    
    attendance_records = []
    for emp in employees:
        status = random.choices(
            ["Present", "Absent", "Leave"],
            weights=[85, 10, 5]
        )[0]
        
        hours = random.uniform(7, 9) if status == "Present" else 0
        
        record = Attendance(
            employee_id=emp.id,
            date=datetime.combine(today, datetime.min.time()),
            status=status,
            hours_worked=round(hours, 2)
        )
        db.add(record)
        attendance_records.append({
            "employee": emp.name,
            "status": status,
            "hours": round(hours, 2)
        })
    
    db.commit()
    return {"date": str(today), "records": attendance_records}

@router.post("/leave-requests")
async def create_leave_request(leave: LeaveRequestCreate, db: Session = Depends(get_db)):
    """Create leave request"""
    db_leave = LeaveRequest(**leave.dict())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

@router.get("/leave-requests")
async def get_leave_requests(db: Session = Depends(get_db)):
    """Get all leave requests"""
    return db.query(LeaveRequest).all()

@router.put("/leave-requests/{leave_id}/approve")
async def approve_leave(leave_id: int, db: Session = Depends(get_db)):
    """Approve leave request"""
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    leave.status = "Approved"
    db.commit()
    return leave

@router.post("/analyze-resume")
async def analyze_resume(request: ResumeAnalysisRequest):
    """Analyze resume using AI"""
    result = await ai_service.analyze_resume(request.resume_text)
    return result

@router.get("/performance-report/{employee_id}")
async def get_performance_report(employee_id: int, db: Session = Depends(get_db)):
    """Get employee performance report"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Get attendance data
    attendance = db.query(Attendance).filter(Attendance.employee_id == employee_id).all()
    
    total_days = len(attendance)
    present_days = sum(1 for a in attendance if a.status == "Present")
    attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
    
    return {
        "employee": employee.name,
        "department": employee.department,
        "position": employee.position,
        "attendance_rate": round(attendance_rate, 2),
        "total_days": total_days,
        "present_days": present_days,
        "performance_score": employee.performance_score,
        "hire_date": employee.hire_date
    }
