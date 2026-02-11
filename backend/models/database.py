"""Database models for AI Office Manager"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings

Base = declarative_base()

# Database engine
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Employee(Base):
    """Employee model for HR module"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    department = Column(String)
    position = Column(String)
    hire_date = Column(DateTime)
    salary = Column(Float)
    performance_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Attendance(Base):
    """Attendance records"""
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, index=True)
    date = Column(DateTime)
    status = Column(String)  # Present, Absent, Leave
    hours_worked = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class LeaveRequest(Base):
    """Leave request model"""
    __tablename__ = "leave_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, index=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    leave_type = Column(String)
    reason = Column(Text)
    status = Column(String, default="Pending")  # Pending, Approved, Rejected
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class SupportTicket(Base):
    """Customer support ticket model"""
    __tablename__ = "support_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    email = Column(String)
    subject = Column(String)
    message = Column(Text)
    category = Column(String)
    priority = Column(String)
    status = Column(String, default="Open")  # Open, In Progress, Resolved, Closed
    ai_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Task(Base):
    """Task model for admin module"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    assigned_to = Column(String)
    due_date = Column(DateTime)
    priority = Column(String)
    status = Column(String, default="Pending")  # Pending, In Progress, Completed
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Lead(Base):
    """Sales lead model"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    company = Column(String)
    industry = Column(String)
    budget = Column(Float)
    source = Column(String)
    score = Column(Float, default=0.0)
    status = Column(String, default="New")  # New, Contacted, Qualified, Converted, Lost
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
