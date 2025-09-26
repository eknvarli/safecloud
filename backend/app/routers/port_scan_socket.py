import asyncio 
import json
import re
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app import models
from app.database import get_db


router = APIRouter(prefix="/scan", tags=["port-scan-socket"])


class PortScanCreate(BaseModel):
    host: str
    port: int = Field(..., ge=1, le=65535)
    timeout: Optional[float] = 3.0
    probe_http: Optional[bool] = False



class PortScanResult(BaseModel):
    id: Optional[int]
    host: str
    port: int
    open: bool
    service: Optional[str] = None
    version: Optional[str] = None
    vulnerabilities: Optional[List[str]] = None
    raw_output: Optional[str] = None
    scanned_at: Optional[datetime] = None


def analyze_banner(banner: str) -> (Optional[str], Optional[str], List[str]):
    service = None
    version = None
    vulns = []

    b = banner or ""
    lower = b.lower()
    
    m = re.search(r"SSH-([\w\-_\.]+)", b)
    if m:
        service = "ssh"
        version = m.group(1)
        if re.search(r"OpenSSH[_ ]?([0-6]\.)", version, re.IGNORECASE):
            vulns.append("Eski OpenSSH sürümü tespit edildi — potansiyel CVE'ler olabilir.")

    if not service and re.search(r"ftp", lower) or re.match(r"220", b):
        service = "ftp"
        m = re.search(r"ftp[ /-]?([0-9\.]+)", lower)
        if m:
            version = m.group(1)

    if not service and ("http/" in b or b.startswith("GET") or b.startswith("HEAD") or "server:" in lower):
        service = "http"
        m = re.search(r"server:\s*([^\r\n]+)", lower)
        if m:
            version = m.group(1).strip()

        if "apache" in lower and ("2.2" in lower or "2.0" in lower):
            vulns.append("Eski Apache sürümü tespit edildi (2.2/2.0).")

    if not service and re.search(r"smtp", lower) or re.match(r"220", b):
        if "smtp" in lower or "esmtp" in lower:
            service = "smtp"

    if not service and b.startswith("+OK") and "redis" in lower:
        service = "redis"

    if not service and "mysql" in lower or re.search(r"\x00", banner):
        if "mysql" in lower:
            service = "mysql"
            m = re.search(r"mysql.*?ver(?:sion)?[:/ ]?([0-9\.\-]+)", lower)
            if m:
                version = m.group(1)

    return service, version, vulns


async def scan_with_socket_async(host: str, port: int, timeout: float = 3.0, probe_http: bool = False) -> dict:
    res = {"open": False, "raw": "", "service": None, "version": None, "vulns": []}

    try:
        conn_task = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(conn_task, timeout=timeout)
        res["open"] = True

        try:
            banner_bytes = await asyncio.wait_for(reader.read(4096), timeout=0.8)
            if banner_bytes:
                try:
                    banner = banner_bytes.decode(errors="ignore")
                except:
                    banner = str(banner_bytes)
                res["raw"] += banner
        except asyncio.TimeoutError:
            banner = ""

        if probe_http:
            try:
                http_head = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: SafeCloudScanner/1.0\r\nConnection: close\r\n\r\n"
                writer.write(http_head.encode())
                await writer.drain()
                resp = await asyncio.wait_for(reader.read(8192), timeout=1.2)
                if resp:
                    try:
                        r = resp.decode(errors="ignore")
                    except:
                        r = str(resp)
                    res["raw"] += r
            except Exception:
                pass

        try:
            extra = await asyncio.wait_for(reader.read(4096), timeout=0.3)
            if extra:
                try:
                    extra_s = extra.decode(errors="ignore")
                except:
                    extra_s = str(extra)
                res["raw"] += extra_s
        except asyncio.TimeoutError:
            pass

        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

        service, version, vulns = analyze_banner(res["raw"])
        res["service"] = service
        res["version"] = version
        res["vulns"] = vulns

    except (asyncio.TimeoutError, ConnectionRefusedError) as e:
        res["open"] = False
        res["raw"] = str(e)
    except Exception as e:
        res["open"] = False
        res["raw"] = str(e)

    return res


def save_scan_db(db: Session, host: str, port: int, scan: dict):
    db_item = models.PortScan(
        host=host,
        port=port,
        open=bool(scan.get("open")),
        service=scan.get("service"),
        version=scan.get("version"),
        vulnerabilities=json.dumps(scan.get("vulns") or []),
        raw_output=scan.get("raw")
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def maybe_alert(db_item):
    vulns = json.loads(db_item.vulnerabilities or "[]")
    critical = any(("cve" in v.lower() or "critical" in v.lower()) for v in vulns)
    if critical:
        pass


@router.post("/port", response_model=PortScanResult)
async def port_scan_socket_endpoint(item: PortScanCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    host = item.host
    port = item.port
    timeout = item.timeout or 3.0
    probe_http = bool(item.probe_http)

    if not host:
        raise HTTPException(status_code=400, detail="Host gerekli.")

    scan_result = await scan_with_socket_async(host, port, timeout=timeout, probe_http=probe_http)

    db_item = save_scan_db(db, host, port, scan_result)

    background_tasks.add_task(maybe_alert, db_item)

    return PortScanResult(
        id=db_item.id,
        host=db_item.host,
        port=db_item.port,
        open=db_item.open,
        service=db_item.service,
        version=db_item.version,
        vulnerabilities=json.loads(db_item.vulnerabilities or "[]"),
        raw_output=db_item.raw_output,
        scanned_at=db_item.scanned_at
    )