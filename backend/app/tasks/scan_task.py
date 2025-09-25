from app.services.scan_service import run_bandit_scan
from sqlalchemy.orm import Session

def run_scan(file_path: str, db: Session):
    return run_bandit_scan(file_path, db)
