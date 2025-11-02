from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum

class JobStatus(str, Enum):
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

class JobType(str, Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    INTERNSHIP = "INTERNSHIP"
    FREELANCE = "FREELANCE"
    OPEN_SOURCE = "OPEN_SOURCE"
    PROPOSAL = "PROPOSAL"

class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    contact_website: Optional[str] = None
    description: Optional[str] = None
    type: JobType = JobType.FULL_TIME
    status: JobStatus = JobStatus.WISHLIST
    technologies: List[str] = []
    requirements: List[str] = []
    benefits: List[str] = []
    comments: Optional[str] = None
    situation: Optional[str] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    contact_website: Optional[str] = None
    description: Optional[str] = None
    type: Optional[JobType] = None
    status: Optional[JobStatus] = None
    technologies: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    comments: Optional[str] = None
    situation: Optional[str] = None

class JobResponseCreate(BaseModel):
    status: str
    notes: Optional[str] = None

class JobResponseUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None

class JobResponse(BaseModel):
    id: int
    date: datetime
    status: str
    notes: Optional[str] = None

    class Config:
        orm_mode = True

class Job(JobCreate):
    id: int
    date_added: datetime
    priority: Priority
    score: int
    responses: List[JobResponse] = []

    class Config:
        orm_mode = True