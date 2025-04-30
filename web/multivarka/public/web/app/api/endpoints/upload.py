import hashlib
import logging
from operator import is_
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_session
from app.db.models import Job
from app.service.load_csv import load_csv_to_clickhouse


router = APIRouter(tags=["upload"])


@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(description="CSV file to upload"),
    session: AsyncSession = Depends(get_session),
):
    if file.content_type != "text/csv":
        return JSONResponse({"error": "Invalid file type"}, status_code=400)
    if file.size > 1024 * 1024:
        return JSONResponse({"error": "File size limit exceeded 1M"}, status_code=400)
    
    md5 = hashlib.md5()
    
    while chunk := await file.read(4096):
        md5.update(chunk)
    md5 = md5.hexdigest()

    is_uploaded = await session.execute(
        select(Job).where(Job.md5 == md5)
    )
    is_uploaded = is_uploaded.scalars().first()
    if is_uploaded:
        return JSONResponse({"error": "File already uploaded"}, status_code=400)

    try:
        await file.seek(0)
        df = pd.read_csv(file.file, sep="\\")
        table_name = await load_csv_to_clickhouse(df)
        job = Job(
            table_name=table_name,
            md5=md5
        )
        session.add(job)
        await session.commit()

        return JSONResponse({
            "job_id": job.id,
            "table_name": table_name
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
