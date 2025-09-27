from cryptography.fernet import Fernet
from pathlib import Path

DEFAULT_KEY_PATH = Path.home() / ".safecloud" / "safecloud.key"

def ensure_key_dir():
    p = DEFAULT_KEY_PATH.parent
    p.mkdir(parents=True, exist_ok=True)

def generate_key(path: str = None) -> bytes:
    ensure_key_dir()

    key = Fernet.generate_key()
    key_path = Path(path) if path else DEFAULT_KEY_PATH
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_bytes(key)

    return key

def load_key(path: str = None) -> bytes:
    key_path = Path(path) if path else DEFAULT_KEY_PATH
    if not key_path.exists():
        raise FileNotFoundError(f"Key not found: {key_path}")
    return key_path.read_bytes()

def encrypt_file(infile: str, outfile: str = None, key: bytes | None = None, key_path: str = None) -> str:
    if key is None:
        key = load_key(key_path)
    
    f = Fernet(key)
    infile_p = Path(infile)
    data = infile_p.read_bytes()
    token = f.encrypt(data)
    out = Path(outfile) if outfile else infile_p.with_suffix(infile_p.suffix + ".enc")
    out.write_bytes(token)

    return str(out)

def decrypt_file(infile: str, outfile: str = None, key: bytes | None = None, key_path: str = None) -> str:
    if key is None:
        key = load_key(key_path)
    f = Fernet(key)
    infile_p = Path(infile)
    token = infile_p.read_bytes()
    data = f.decrypt(token)

    if outfile:
        out = Path(outfile)
    else:
        if infile_p.suffix == ".enc":
            out = infile_p.with_suffix("")
        else:
            name = infile_p.name
            if name.endswith(".enc"):
                out = infile_p.with_name(name[:-4])
            else:
                out = infile_p.with_name(name + ".dec")
    
    out.write_bytes(data)
    return str(out)