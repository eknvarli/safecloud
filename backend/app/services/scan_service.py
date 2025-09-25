import subprocess
import json
from app.models import ScanResult
from sqlalchemy.orm import Session

def run_bandit_scan(file_path: str, db: Session):
    try:
        result = subprocess.run(
            ["bandit", "-f", "json", "-q", file_path],
            capture_output=True,
            text=True,
            check=False
        )

        output = json.loads(result.stdout)
        results = output.get("results", [])

        saved_results = []
        for item in results:
            scan_result = ScanResult(
                filename=item.get("filename"),
                line_number=item.get("line_number"),
                issue_text=item.get("issue_text"),
                issue_severity=item.get("issue_severity"),
                test_name=item.get("test_name"),
                test_id=item.get("test_id")
            )
            db.add(scan_result)
            db.commit()
            
            saved_results.append({
                "filename": scan_result.filename,
                "line_number": scan_result.line_number,
                "issue_text": scan_result.issue_text,
                "issue_severity": scan_result.issue_severity,
                "test_name": scan_result.test_name,
                "test_id": scan_result.test_id
            })

        return saved_results

    except json.JSONDecodeError:
        return {"error": "Bandit JSON output could not be parsed."}
    except Exception as e:
        return {"error": str(e)}
