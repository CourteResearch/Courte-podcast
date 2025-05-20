from pydantic import BaseModel

class Job(BaseModel):
    id: str
    status: str
    output_path: str
    progress: int = 0  # 0-100 percent
