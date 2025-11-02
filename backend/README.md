# Job Organizer Backend

A FastAPI-based backend service for managing job applications with smart priority calculation.

## Features

- RESTful API for job management
- Smart priority calculation based on multiple factors
- Database seeding from markdown files
- Automatic OpenAPI documentation
- Async SQLAlchemy with PostgreSQL
- CORS support for frontend integration

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   Copy `.env.example` to `.env` and update the database URL:
   ```bash
   cp .env.example .env
   ```

3. **Database Setup**
   Make sure PostgreSQL is running and create a database:
   ```sql
   CREATE DATABASE joborganizer;
   ```

4. **Seed Database**
   Run the seeding script to populate with sample data:
   ```bash
   python seed.py
   ```

5. **Run the Server**
   ```bash
   python main.py
   ```
   
   Or with uvicorn:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## API Endpoints

- `GET /api/jobs` - List all jobs with optional filtering
- `GET /api/jobs/{id}` - Get a specific job
- `POST /api/jobs` - Create a new job
- `PATCH /api/jobs/{id}` - Update a job
- `DELETE /api/jobs/{id}` - Delete a job
- `POST /api/jobs/{id}/responses` - Add a response to a job
- `POST /api/import/markdown` - Import jobs from JOBS_SOURCE.md
- `GET /api/stats` - Get job statistics

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Priority Calculation

The system automatically calculates job priority based on:
- Location (major tech cities score higher)
- Technologies used
- Company reputation
- Seniority level
- Benefits offered
- Compensation indicators

## Database Schema

- **jobs**: Main job information
- **job_responses**: Application responses and communications
- **deleted_jobs**: Tracks deleted jobs to prevent re-import