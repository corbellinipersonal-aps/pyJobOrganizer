from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from .job import JobStatus, JobType, Priority

class JobResponseOut(BaseModel):
    id: int
    job_id: int
    date: datetime
    status: str
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True

class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: str
    contact_website: Optional[str] = None
    description: Optional[str] = None
    type: JobType
    status: JobStatus
    priority: Priority
    technologies: List[str] = []
    requirements: List[str] = []
    benefits: List[str] = []
    comments: Optional[str] = None
    situation: Optional[str] = None
    date_added: datetime
    responses: List[JobResponseOut] = []
    
    class Config:
        from_attributes = True