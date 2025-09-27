import os
import json
import pyfiglet
import ipaddress


def load_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def print_banner():
    banner = pyfiglet.figlet_format("SAFECLOUD")
    print(banner)

def is_valid_ip(ip_str: str) -> bool:
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def parse_ports(ports_str: str):
    if not ports_str:
        return None
    ports = set()
    parts = ports_str.split(",")
    for p in parts:
        p = p.strip()
        if "-" in p:
            try:
                start, end = map(int, p.split("-", 1))
                if start <= end:
                    ports.update(range(start, end+1))
            except Exception:
                continue
        else:
            try:
                ports.add(int(p))
            except Exception:
                continue
    return sorted(ports)