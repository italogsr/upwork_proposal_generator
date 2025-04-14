# Docker Setup for Upwork Proposal Generator

This document provides instructions for running the Upwork Proposal Generator using Docker containers.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Container Architecture

The application is split into the following containers:

1. **db**: PostgreSQL database
2. **backend**: FastAPI backend service
3. **streamlit**: Streamlit frontend
4. **flask**: Flask frontend (alternative UI)

## Quick Start

### Option 1: Using the Helper Script

```bash
./docker-run.sh
```

This script will:
- Create a `.env` file from the template if it doesn't exist
- Check if your Groq API key is set
- Build and start the containers

### Option 2: Manual Setup

1. Create a `.env` file based on the provided template:
   ```bash
   cp .env.docker .env
   ```

2. Edit the `.env` file and add your Groq API key and other required configuration:
   ```
   # Required settings
   GROQ_API_KEY=your_groq_api_key_here
   JWT_SECRET_KEY=your_secret_key_for_jwt_tokens
   FLASK_SECRET_KEY=your_secret_key_for_flask

   # Database settings (these are already configured for Docker)
   DATABASE_USER=your_database_user
   DATABASE_PASSWORD=your_database_password
   DATABASE_HOST=db
   DATABASE_PORT=5432
   ```

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

## Accessing the Application

Once the containers are running, you can access:

- **API Documentation**: http://localhost:8000/docs
- **Streamlit Frontend**: http://localhost:8501
- **Flask Frontend**: http://localhost:8502

## Common Commands

### View Container Logs

```bash
docker-compose logs -f backend  # For backend logs
docker-compose logs -f streamlit  # For Streamlit frontend logs
docker-compose logs -f flask  # For Flask frontend logs
docker-compose logs -f db  # For database logs
```

### Stop the Containers

```bash
docker-compose down
```

To stop the containers and remove the volumes (this will delete all data):

```bash
docker-compose down -v
```

### Rebuild Containers After Code Changes

```bash
docker-compose build
docker-compose up -d
```

## Container Details

### Database Container

- PostgreSQL 16 database with persistent storage
- Automatically initialized with the correct schema using `docker/db/init.sql`
- Credentials are set via environment variables in the `.env` file
- Data is stored in a Docker volume for persistence between restarts

### Backend Container

- FastAPI application serving the API endpoints
- Connects to the database and Groq LLM
- Waits for the database to be ready before starting
- Creates necessary database tables using `create_tables.py`
- Exposes port 8000
- API documentation available at http://localhost:8000/docs

### Streamlit Frontend Container

- Streamlit UI for the primary user interface
- Waits for the backend to be ready before starting
- Connects to the backend API
- Exposes port 8501
- Accessible at http://localhost:8501

### Flask Frontend Container

- Flask UI providing an alternative web interface
- Waits for the backend to be ready before starting
- Bootstrap-based responsive design
- Connects to the backend API
- Exposes port 8502
- Accessible at http://localhost:8502

## Development with Docker

The Docker setup is configured for development, with the following features:

- Source code is mounted as volumes, so changes are reflected immediately
- Backend API runs with hot-reloading enabled
- Database data persists between container restarts

To apply changes:

1. For code changes: Simply edit the files in the `src` directory, and the changes will be applied automatically
2. For dependency changes: Update the `docker/requirements.txt` file and rebuild the containers
