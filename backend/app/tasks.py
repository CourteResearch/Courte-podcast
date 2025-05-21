from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

from app.services.video_processor_3d import create_3d_video_from_audio
from app.models.job import Job
import os

# jobs dict will be imported from jobs_store
from app.jobs_store import jobs

import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import os

@celery.task
def process_video_task(job_id, audio_save_path, mapping):
    logger.info(f"Started processing job {job_id}")

    # Ensure the output videos directory exists
    output_videos_dir = "output_videos"
    os.makedirs(output_videos_dir, exist_ok=True)

    output_video_path = os.path.join(output_videos_dir, f"output_{job_id}.mp4")
    job = jobs.get(job_id)
    try:
        # Simulate progress updates
        for p in range(0, 101, 20):
            if job:
                job.progress = p
                logger.info(f"Job {job_id} progress: {p}%")
            time.sleep(1)  # Simulate work
        create_3d_video_from_audio(audio_save_path, output_video_path, mapping)
        if job:
            job.status = "completed"
            job.output_path = output_video_path
            job.progress = 100
            logger.info(f"Job {job_id} completed. Output: {output_video_path}")
    except Exception as e:
        if job:
            job.status = "failed"
            job.output_path = ""
            job.progress = 0
        logger.error(f"Video processing failed for job {job_id}: {e}")
