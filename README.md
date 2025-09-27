# SafeCloud CLI

SafeCloud is a powerful CLI tool for security checks, file encryption, IP analysis, and AI-based log analysis. It integrates advanced features such as port scanning, S3 bucket auditing, DNSBL checks, and local AI log scanning without requiring API keys.

---

## Features

* **S3 Bucket Check**: Detect if an AWS S3 bucket is publicly accessible.
* **Port Scan**: Scan for open ports on a target IP.
* **IP Check**: Validate IP/hostname, reverse DNS lookup, optional banner grabbing, port scanning, and DNSBL blacklist check.
* **Key Generation**: Generate encryption keys.
* **Encrypt/Decrypt Files**: AES-based encryption/decryption using generated keys.
* **AI Log Analysis**: Analyze logs locally for security threats using GPT4All (no API key required).

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/eknvarli/safecloud.git
cd safecloud
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Make CLI globally accessible:

```bash
python setup.py install
```

---

## Usage

### 1. S3 Bucket Check

```bash
safecloud s3check <bucket_name>
```

Checks if the specified bucket is public or private.

### 2. Port Scan

```bash
safecloud portscan <ip>
```

Scans the target IP for common open ports.

### 3. IP Check

```bash
safecloud ipcheck <target> --ports 22,80,443 --banner --blacklist
```

Performs reverse DNS lookup, port scan, optional banner grabbing, and DNSBL blacklist checks.

### 4. Key Generation

```bash
safecloud keygen --out ~/.safecloud/mykey.key
```

Generates an encryption key to the specified path.

### 5. Encrypt a File

```bash
safecloud encrypt myfile.txt --out myfile.txt.enc --keyfile ~/.safecloud/mykey.key
```

Encrypts a file using the specified key.

### 6. Decrypt a File

```bash
safecloud decrypt myfile.txt.enc --out myfile_decrypted.txt --keyfile ~/.safecloud/mykey.key
```

Decrypts a previously encrypted file.

### 7. AI Log Analysis

```bash
safecloud logai sample.log
```

Uses a local GPT4All model to analyze logs for potential threats and anomalies.

---

## AI Model Setup

SafeCloud uses the GPT4All model locally. The CLI automatically downloads the model to `~/.safecloud/models/` if not found.

Supported AI model:

* `gpt4all-lora-quantized.bin`

Note: Ensure you have a stable internet connection for the initial download.

---

## Example Commands

```bash
safecloud s3check my-test-bucket
safecloud portscan 8.8.8.8
safecloud ipcheck 8.8.8.8 --ports 22,80,443 --banner --blacklist
safecloud keygen --out ~/.safecloud/mykey.key
safecloud encrypt test.txt --keyfile ~/.safecloud/mykey.key
safecloud decrypt test.txt.enc --keyfile ~/.safecloud/mykey.key
safecloud logai sample.log
```

---

## License

GPLv3.0 License