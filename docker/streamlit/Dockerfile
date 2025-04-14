FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY docker/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port
EXPOSE 8501

# Copy startup script
COPY docker/streamlit/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Start the Streamlit server
CMD ["/app/start.sh"]
