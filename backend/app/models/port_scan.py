from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class PortScan(Base):
    __tablename__ = "port_scans"
    id = Column(Integer, primary_key=True, index=True)
    host = Column(String(255), index=True, nullable=False)
    port = Column(Integer, nullable=False)
    open = Column(Boolean, nullable=False, default=False)
    service = Column(String(100), nullable=True)
    version = Column(String(200), nullable=True)
    vulnerabilities = Column(Text, nullable=True)
    raw_output = Column(Text, nullable=True)
    scanned_at = Column(DateTime(timezone=True), server_default=func.now())
