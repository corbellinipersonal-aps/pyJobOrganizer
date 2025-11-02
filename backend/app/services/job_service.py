"""
Service layer for Job operations.
"""
import time
from typing import Optional

# In-process cache for job stats
_stats_cache = None
_stats_cache_timestamp = 0
_STATS_TTL = 60
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload

from ..models.job import Job, JobResponse, DeletedJob, JobStatus, Priority
import os


async def get_all_jobs(db: AsyncSession, status: str = None, priority: str = None, sort_by: str = 'date_added', sort_order: str = 'desc', limit: int = 100, offset: int = 0):
    query = select(Job).options(selectinload(Job.responses))

    # Filtering
    if status:
        query = query.where(Job.status == status)
    if priority:
        query = query.where(Job.priority == priority)

    # Sorting
    sort_column_map = {
        'date_added': Job.date_added,
        'date_modified': Job.date_modified,
        'priority': Job.priority,
        'company': Job.company,
        'score': Job.score
    }

    sort_column = sort_column_map.get(sort_by, Job.date_added)

    if sort_order == 'desc':
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Pagination
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    jobs = result.scalars().all()

    return jobs

async def get_job(db: AsyncSession, job_id: int):
    query = select(Job).options(selectinload(Job.responses)).where(Job.id == job_id)
    result = await db.execute(query)
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job

async def create_job(db: AsyncSession, job_data):
    job = Job(
        **job_data.dict(),
        date_added=datetime.utcnow()
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job

async def update_job(db: AsyncSession, job_id: int, job_data):
    job = await get_job(db, job_id)
    update_data = job_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(job, field, value)

    job.date_modified = datetime.utcnow()
    await db.commit()
    await db.refresh(job)
    return job

async def delete_job(db: AsyncSession, job_id: int):
    job = await get_job(db, job_id)
    deleted = DeletedJob(
        title=job.title,
        company=job.company,
        location=job.location,
        contact_website=job.contact_website,
        deleted_at=datetime.utcnow()
    )
    db.add(deleted)
    await db.delete(job)
    await db.commit()
    return {"message": "Job deleted successfully"}

async def create_job_response(db: AsyncSession, job_id: int, response_data):
    job = await get_job(db, job_id)
    response = JobResponse(
        job_id=job_id,
        **response_data.dict()
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def import_jobs_from_markdown(db: AsyncSession, file_path: str = "JOBS_SOURCE.md"):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"{file_path} file not found")

    deleted_result = await db.execute(select(DeletedJob))
    deleted_jobs = deleted_result.scalars().all()
    deleted_signatures = {(job.title, job.company, job.location) for job in deleted_jobs}

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    jobs_data = parse_markdown_jobs(content)
    imported_count = 0
    for job_data in jobs_data:
        job_signature = (job_data["title"], job_data["company"], job_data["location"])
        if job_signature in deleted_signatures:
            continue
        existing_query = select(Job).where(
            and_(
                Job.title == job_data["title"],
                Job.company == job_data["company"],
                Job.location == job_data["location"]
            )
        )
        existing_job = (await db.execute(existing_query)).scalar_one_or_none()
        if existing_job:
            continue
        priority_result = calculate_priority(job_data)
        job = Job(**job_data, priority=priority_result["priority"], score=priority_result["score"], date_added=datetime.utcnow())
        db.add(job)
        imported_count += 1
    await db.commit()
    return {"message": f"Successfully imported {imported_count} jobs"}


async def get_job_stats(db: AsyncSession):
    # In-process cache
    global _stats_cache, _stats_cache_timestamp
    now = time.time()
    if _stats_cache and (now - _stats_cache_timestamp) < _STATS_TTL:
        return _stats_cache
    # Use database aggregation for counts
    total_query = select(func.count()).select_from(Job)
    total_result = await db.execute(total_query)
    total_count = total_result.scalar_one()

    status_query = select(Job.status, func.count()).group_by(Job.status)
    status_result = await db.execute(status_query)
    status_counts = {row[0].value: row[1] for row in status_result.all()}

    priority_query = select(Job.priority, func.count()).group_by(Job.priority)
    priority_result = await db.execute(priority_query)
    priority_counts = {row[0].value: row[1] for row in priority_result.all()}

    stats = {
        "total_jobs": total_count,
        "status_counts": status_counts,
        "priority_counts": priority_counts
    }
    _stats_cache = stats
    _stats_cache_timestamp = now
    return stats
