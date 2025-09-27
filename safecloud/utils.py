import os
import json
import pyfiglet

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
