from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=JSONResponse)
def read_root():
    return {"message": "PodVision Studio 3D MVP Backend"}

from uuid import uuid4
from app.models.job import Job
from app.jobs_store import jobs

from fastapi import UploadFile, File, Form
import shutil
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/submit-job")
async def submit_job(
    audio_file: UploadFile = File(...),
    speaker_mapping: str = Form(...)
):
    logger.info("submit_job endpoint called")
    job_id = str(uuid4())
    logger.info(f"Received new job submission: {job_id}")

    # Ensure the temporary audio directory exists
    temp_audio_dir = "temp_audio"
    os.makedirs(temp_audio_dir, exist_ok=True)

    # Save uploaded audio file
    audio_save_path = os.path.join(temp_audio_dir, f"audio_{job_id}.mp3")
    with open(audio_save_path, "wb") as buffer:
        shutil.copyfileobj(audio_file.file, buffer)
    logger.info(f"Saved audio file for job {job_id} at {audio_save_path}")
    # Parse speaker mapping
    mapping = json.loads(speaker_mapping)
    job = Job(id=job_id, status="processing", output_path="")
    jobs[job_id] = job
    logger.info(f"Created job entry for {job_id}")

    # Asynchronous processing: trigger Celery task
    from tasks import process_video_task
    logger.info(f"Dispatching Celery task for job {job_id}")
    process_video_task.delay(job_id, audio_save_path, mapping)

    return JSONResponse(content={"job_id": job_id}, status_code=status.HTTP_200_OK)

@app.get("/job-status/{job_id}")
def job_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return JSONResponse(content={"error": "Job not found"}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(
        content={
            "status": job.status,
            "output_path": job.output_path,
            "progress": job.progress,
        },
        status_code=status.HTTP_200_OK,
    )

@app.get("/download/{job_id}")
def download_video(job_id: str):
    job = jobs.get(job_id)
    if not job or not job.output_path or job.status != "completed":
        return JSONResponse(content={"error": "Video not available"}, status_code=status.HTTP_404_NOT_FOUND)
    return FileResponse(path=job.output_path, filename=f"podcast_{job_id}.mp4", media_type="video/mp4")
