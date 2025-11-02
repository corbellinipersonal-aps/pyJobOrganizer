from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from .db.database import get_db, init_db
from .models.job import Job as JobModel
from .schemas.job import Job, JobCreate, JobUpdate
from .services import job_service

app = FastAPI(title="Job Organizer API", version="1.0.0")

# CORS configuration - environment-aware
from .core.config import CORS_ORIGINS, is_production

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # Environment-specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "details": exc.errors()}
    )

@app.exception_handler(Exception)
async def unexpected_exception_handler(request, exc):
    logging.getLogger("uvicorn.error").error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/api/jobs", response_model=List[Job])
async def get_jobs(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    sort_by: str = Query('date_added', description="Sort jobs by 'date_added', 'priority', or 'company'"),
    sort_order: str = Query('desc', description="Sort order: 'asc' or 'desc'"),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    return await job_service.get_all_jobs(db, status, priority, sort_by, sort_order, limit, offset)

@app.get("/api/jobs/{job_id}", response_model=Job)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    return await job_service.get_job(db, job_id)

@app.post("/api/jobs", response_model=Job)
async def create_job(job_data: JobCreate, db: AsyncSession = Depends(get_db)):
    return await job_service.create_job(db, job_data)

@app.patch("/api/jobs/{job_id}", response_model=Job)
async def update_job(
    job_id: int, 
    job_data: JobUpdate, 
    db: AsyncSession = Depends(get_db)
):
    return await job_service.update_job(db, job_id, job_data)

@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: int, db: AsyncSession = Depends(get_db)):
    await job_service.delete_job(db, job_id)
    return {"message": "Job deleted successfully"}

@app.get("/api/stats")
async def get_job_stats(db: AsyncSession = Depends(get_db)):
    return await job_service.get_job_stats(db)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
