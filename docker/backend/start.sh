#!/bin/bash

echo "Waiting for database to be ready..."
# Wait for PostgreSQL to be ready
until PGPASSWORD="$DATABASE_PASSWORD" psql -h db -U "$DATABASE_USER" -d upwork_proposal_generator -c "\q"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - creating tables"
# Create database tables
python create_tables.py

echo "Starting API server..."
exec uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
