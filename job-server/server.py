from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid, threading, time

app = FastAPI()
jobs = {}

class JobPayload(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str

@app.post("/submit-job")
def submit_job(payload: JobPayload):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"id": job_id, "status": "pending", **payload.dict()}
    return {"job_id": job_id}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": job["status"]}

def worker():
    while True:
        for job in jobs.values():
            if job["status"] == "pending":
                job["status"] = "running"
                time.sleep(1)
                job["status"] = "done"
        time.sleep(2)

threading.Thread(target=worker, daemon=True).start()

