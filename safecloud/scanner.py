import socket
import boto3
import dns.resolver

DNSBL_PROVIDERS = [
    "zen.spamhaus.org",
    "bl.spamcop.net",
    "dnsbl.sorbs.net",
    "cbl.abuseat.org",
]

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

def grab_banner(ip, port, timeout=1):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode(errors="ignore")
        sock.close()
        return banner.strip()
    except Exception:
        return ""

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
    
def dnsbl_check(ip: str, providers: list | None = None) -> dict:
    if providers is None:
        providers = DNSBL_PROVIDERS
    
    res = {}
    try:
        parts = ip.split(".")
        if len(parts) != 4:
            for p in providers:
                res[p] = "unsupported-ip-version"
            return res
        rev = ".".join(reversed(parts))
    except Exception as e:
        for p in providers:
            res[p] = f"error: {e}"
        return res

    for provider in providers:
        query = f"{rev}.{provider}"
        try:
            answers = dns.resolver.resolve(query, "A")
            try:
                txt = dns.resolver.resolve(query, "TXT")
                txts = [t.to_text().strip('"') for t in txt]
            except Exception:
                txts = []
            res[provider] = {"listed": True, "txt": txts}
        except dns.resolver.NXDOMAIN:
            res[provider] = {"listed": False}
        except dns.resolver.NoAnswer:
            res[provider] = {"listed": False}
        except Exception as e:
            res[provider] = {"error": str(e)}
    return res
