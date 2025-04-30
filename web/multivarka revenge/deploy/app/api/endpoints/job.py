from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.db.base import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Job
from app.schemas.job import JobRead


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobRead)
async def get_job(job_id: str, session: AsyncSession = Depends(get_session)):
    job = await session.get(Job, job_id)
    if not job:
        return JSONResponse({"error": "Job not found"}, status_code=404)
    return JobRead.model_validate(job)