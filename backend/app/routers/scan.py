from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.tasks.scan_task import run_scan
from app.database import get_db
import shutil, os
from fastapi import Query
from app.models import ScanResult


router = APIRouter()

@router.post("/run")
async def run_scan_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db)):
    temp_file_path = f"./temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = run_scan(temp_file_path, db)

    os.remove(temp_file_path)
    return {"results": results}

@router.get("/history")
def get_scan_history(
    filename: str | None = Query(None, description="Filter by filename"),
    severity: str | None = Query(None, description="Filter by issue severity"),
    db: Session = Depends(get_db)
):
    query = db.query(ScanResult)

    if filename:
        query = query.filter(ScanResult.filename.contains(filename))
    if severity:
        query = query.filter(ScanResult.issue_severity == severity)

    results = query.order_by(ScanResult.created_at.desc()).all()

    history = [
        {
            "filename": r.filename,
            "line_number": r.line_number,
            "issue_text": r.issue_text,
            "issue_severity": r.issue_severity,
            "test_name": r.test_name,
            "test_id": r.test_id,
            "created_at": r.created_at.isoformat()
        }
        for r in results
    ]

    return {"results": history}