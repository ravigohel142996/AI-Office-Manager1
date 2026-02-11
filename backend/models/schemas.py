"""Pydantic schemas for request/response models"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

# Authentication schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Employee schemas
class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    position: str
    salary: float

class AttendanceCreate(BaseModel):
    employee_id: int
    date: datetime
    status: str
    hours_worked: float

class LeaveRequestCreate(BaseModel):
    employee_id: int
    start_date: datetime
    end_date: datetime
    leave_type: str
    reason: str

# Support schemas
class TicketCreate(BaseModel):
    customer_name: str
    email: EmailStr
    subject: str
    message: str

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    ai_response: Optional[str] = None

# Task schemas
class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to: str
    due_date: datetime
    priority: str

class TaskUpdate(BaseModel):
    status: Optional[str] = None

# Lead schemas
class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    company: str
    industry: str
    budget: float
    source: str

class LeadUpdate(BaseModel):
    score: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None

# AI Request schemas
class ResumeAnalysisRequest(BaseModel):
    resume_text: str

class TicketClassificationRequest(BaseModel):
    ticket_text: str

class LeadScoringRequest(BaseModel):
    name: str
    company: str
    industry: str
    budget: float
    source: str

class ForecastRequest(BaseModel):
    data: List[float]
