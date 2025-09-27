import os
import pytest
from click.testing import CliRunner
from safecloud import cli, scanner, crypto, utils

runner = CliRunner()

def test_s3check_private(monkeypatch):
    def mock_check_s3(bucket_name):
        return {"bucket": bucket_name, "public": False}
    monkeypatch.setattr(scanner, "check_s3", mock_check_s3)
    
    result = runner.invoke(cli.cli, ["s3check", "my-private-bucket"])
    assert result.exit_code == 0
    assert "Safe" in result.output

def test_s3check_public(monkeypatch):
    def mock_check_s3(bucket_name):
        return {"bucket": bucket_name, "public": True}
    monkeypatch.setattr(scanner, "check_s3", mock_check_s3)
    
    result = runner.invoke(cli.cli, ["s3check", "my-public-bucket"])
    assert result.exit_code == 0
    assert "WARNING" in result.output

def test_portscan(monkeypatch):
    def mock_scan_ports(ip):
        return [22, 80]
    monkeypatch.setattr(scanner, "scan_ports", mock_scan_ports)

    result = runner.invoke(cli.cli, ["portscan", "127.0.0.1"])
    assert result.exit_code == 0
    assert "Open ports" in result.output

def test_keygen(tmp_path):
    out_path = tmp_path / "test.key"
    result = runner.invoke(cli.cli, ["keygen", "--out", str(out_path)])
    assert result.exit_code == 0
    assert out_path.exists()
    assert "Key generated" in result.output

def test_encrypt_decrypt(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("secret data")
    key_file = tmp_path / "test.key"
    
    runner.invoke(cli.cli, ["keygen", "--out", str(key_file)])
    
    encrypted_file = tmp_path / "test.txt.enc"
    result_enc = runner.invoke(cli.cli, ["encrypt", str(test_file), "--out", str(encrypted_file), "--keyfile", str(key_file)])
    assert result_enc.exit_code == 0
    assert encrypted_file.exists()
    
    decrypted_file = tmp_path / "test_decrypted.txt"
    result_dec = runner.invoke(cli.cli, ["decrypt", str(encrypted_file), "--out", str(decrypted_file), "--keyfile", str(key_file)])
    assert result_dec.exit_code == 0
    assert decrypted_file.read_text() == "secret data"

def test_utils_is_valid_ip():
    from safecloud import utils
    assert utils.is_valid_ip("127.0.0.1") is True
    assert utils.is_valid_ip("256.0.0.1") is False
