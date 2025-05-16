from pydantic import BaseModel

class Job(BaseModel):
    id: str
    status: str
    output_path: str
