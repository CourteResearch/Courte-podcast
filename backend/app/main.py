from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "PodVision Studio 3D MVP Backend"}
