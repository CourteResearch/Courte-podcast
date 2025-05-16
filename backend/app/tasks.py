from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def process_video_task(job_id):
    # Placeholder for video processing logic
    print(f"Processing job {job_id}")
