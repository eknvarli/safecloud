import socket
import boto3

def scan_ports(ip, ports=[22, 80, 443, 3306, 5432]):
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except Exception:
            pass
    return open_ports


def check_s3(bucket_name):
    s3 = boto3.client("s3")
    try:
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        grants = acl["Grants"]
        for grant in grants:
            if "AllUsers" in str(grant):
                return {"bucket": bucket_name, "public": True}
        return {"bucket": bucket_name, "public": False}
    except Exception as e:
        return {"error": str(e), "public": False}