from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.db.base import get_session
from app.db.models import Job
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.table import get_table


router = APIRouter(prefix="/table",tags=["table"])

@router.get("/{job_id}")
async def get_table_data(job_id: str, session: AsyncSession = Depends(get_session)):
    job = await session.get(Job, job_id)
    if not job:
        return JSONResponse({"error": "Job not found"}, status_code=404)
    
    table_data = await get_table(job.table_name)

    return table_data