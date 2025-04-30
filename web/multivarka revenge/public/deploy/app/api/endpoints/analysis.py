from asyncio import sleep
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.db.base import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Job
from app.service.analyze import analyze_columns

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("/{job_id}")
async def start_analysis(job_id: str, session: AsyncSession = Depends(get_session)):
    job = await session.get(Job, job_id)
    if not job:
        return JSONResponse({"error": "Job not found"}, status_code=404)

    job.status = "processing"
    try:
        results = await analyze_columns(job.table_name)

        job.results = results
        job.message = "Analysis completed successfully"
        job.status = "completed"
    except Exception as e:
        job.message = str(e)
        job.status = "failed"
        job.results = []
    await session.commit()
    