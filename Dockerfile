# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy 3D assets
COPY 3d_assets/ /app/3d_assets/

# Install Blender and FFmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    blender \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy the backend directory contents into the container at /app
COPY backend/. /app

# Expose the port the app runs on
EXPOSE 8000

# Define environment variables for Celery broker and result backend
ENV CELERY_BROKER_URL=redis://redis:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis:6379/0

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
