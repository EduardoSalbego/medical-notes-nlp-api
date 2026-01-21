from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class HealthCheck(BaseModel):
    status: str = "ok"

@app.get("/")
def read_root():
    return {"status": "online", "service": "medical-notes-ai"}