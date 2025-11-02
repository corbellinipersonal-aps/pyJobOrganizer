from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, ARRAY, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from ..db.database import Base

class JobStatus(enum.Enum):
    WISHLIST = "WISHLIST"
    APPLIED = "APPLIED"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    DISCARDED = "DISCARDED"
    ACTIVE = "ACTIVE"
    ALPHA = "ALPHA"
    PRIMARY = "PRIMARY"
    IDEA = "IDEA"
    POTENTIAL = "POTENTIAL"

class JobType(enum.Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    INTERNSHIP = "INTERNSHIP"
    FREELANCE = "FREELANCE"
    OPEN_SOURCE = "OPEN_SOURCE"
    PROPOSAL = "PROPOSAL"

class Priority(enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = (
        Index('ix_jobs_status', 'status'),
        Index('ix_jobs_priority', 'priority'),
        Index('ix_jobs_date_added', 'date_added'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    contact_website = Column(String)
    description = Column(Text)
    type = Column(Enum(JobType), default=JobType.FULL_TIME)
    status = Column(Enum(JobStatus), default=JobStatus.WISHLIST)
    priority = Column(Enum(Priority), default=Priority.MEDIUM)
    score = Column(Integer, default=0)
    technologies = Column(ARRAY(String), default=[])
    requirements = Column(ARRAY(String), default=[])
    benefits = Column(ARRAY(String), default=[])
    comments = Column(Text)
    situation = Column(Text)
    date_added = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    responses = relationship("JobResponse", back_populates="job", cascade="all, delete-orphan")

class JobResponse(Base):
    __tablename__ = "job_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)
    notes = Column(Text)
    
    # Relationships
    job = relationship("Job", back_populates="responses")

class DeletedJob(Base):
    __tablename__ = "deleted_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=False)
    contact_website = Column(String)
    deleted_at = Column(DateTime, default=datetime.utcnow)