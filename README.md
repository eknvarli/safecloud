# SafeCloud

SafeCloud is a web-based security scanning application built using **FastAPI**, **SQLite**, and designed with extensibility in mind. It provides features to scan files for security issues, track scan history, and can be integrated with additional storage or caching backends like **PostgreSQL** and **Redis**.

---

## Features

* **File Security Scanning**: Upload files and receive automated security analysis.
* **Scan History**: Maintain a record of scanned files along with detailed results.
* **Modular Architecture**: Easy to extend with additional databases, caching systems, or scanning algorithms.
* **Development Ready**: Comes with a Bash script to setup the dev environment using **Pipenv**.
* **Dockerized**: Optional Docker setup for containerized deployment.

---

## Technology Stack

* **Backend**: FastAPI
* **Database**: SQLite (default), supports PostgreSQL
* **ORM**: SQLAlchemy
* **Task Management**: Synchronous tasks for scanning (can be extended to async or Celery)
* **Caching**: Optional Redis integration
* **Python Environment**: Pipenv

---

## Installation

### Prerequisites

* Python 3.13+
* Pipenv
* Docker (optional for containerized deployment)

### Setup with Pipenv

```bash
git clone https://github.com/yourusername/safecloud.git
cd safecloud/backend

# Install dependencies
pipenv install

# Activate pipenv shell
pipenv shell

# Run the development server
pipenv run uvicorn app.main:app --reload
```

### Docker Setup

1. Build the Docker image:

```bash
docker build -t safecloud:latest .
```

2. Run the container:

```bash
docker run -p 8000:8000 safecloud:latest
```

---

## Usage

### Endpoints

* **POST /scan/run**

  * Upload a file for scanning.
  * Request:

    ```bash
    curl -X POST "http://localhost:8000/scan/run" -F "file=@yourfile.txt"
    ```
  * Response: JSON containing scan results.

* **GET /scan/history**

  * Retrieve scan history.
  * Optional query parameters:

    * `filename`: filter by filename
    * `severity`: filter by issue severity
  * Request:

    ```bash
    curl "http://localhost:8000/scan/history"
    ```

---

## Development

* Tests are located in `backend/tests`.
* Run tests using:

```bash
pytest -v
```

* Development helper script is included:

```bash
./dev.sh
```

---

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/my-feature`).
5. Open a Pull Request.

---

## License

GPLv3.0 License
