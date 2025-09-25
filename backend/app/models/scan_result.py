from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    line_number = Column(Integer)
    issue_text = Column(Text)
    issue_severity = Column(String)
    test_name = Column(String)
    test_id = Column(String)
    package_name = Column(String, nullable=True)
    affected_versions = Column(String, nullable=True)
    vulnerability_id = Column(String, nullable=True)
    cvss_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
