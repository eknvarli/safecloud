#!/bin/bash
# SafeCloud dev script using pipenv

echo "Installing dependencies..."
pipenv install

echo "Activating pipenv shell..."
echo "Running database migrations..."

echo "Starting FastAPI server..."
pipenv run uvicorn app.main:app --reload