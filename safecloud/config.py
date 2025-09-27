import os

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "default")

DEFAULT_PORTS = [22, 80, 443, 3306, 5432]

REPORT_DIR = os.getenv("SAFECL_REPORT_DIR", "./reports")

if not os.path.exists(REPORT_DIR):
    os.makedirs(REPORT_DIR)
