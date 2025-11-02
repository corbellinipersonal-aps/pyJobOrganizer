"""
Core configuration using environment variables.
Supports development and production environments.
"""
from dotenv import load_dotenv
import os
from typing import List

# Load environment variables from .env file
load_dotenv()

# Environment detection
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

def is_production() -> bool:
    """Check if running in production"""
    return ENVIRONMENT == "production"

def is_development() -> bool:
    """Check if running in development"""
    return ENVIRONMENT == "development"

# Database URL for SQLAlchemy
if is_production():
    # Production: Use Render's DATABASE_URL (required)
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL must be set in production")
else:
    # Development: Use local PostgreSQL
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost/job_organizer"
    )

# CORS origins for the frontend applications
if is_production():
    # Production: Only allow deployed frontend
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "https://job-organizer-reflex.onrender.com"
    ).split(",")
else:
    # Development: Allow local development servers
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000,http://localhost:8001"
    ).split(",")

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG" if is_development() else "INFO")
