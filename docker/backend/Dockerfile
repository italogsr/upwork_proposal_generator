FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY docker/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Copy startup script
COPY docker/backend/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose the port
EXPOSE 8000

# Start the API server
CMD ["/app/start.sh"]
