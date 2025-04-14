#!/bin/bash

# Check if .env file exists, if not create it from .env.docker
if [ ! -f .env ]; then
    echo "Creating .env file from .env.docker template..."
    cp .env.docker .env
    echo "Please edit the .env file to add your Groq API key and other configuration."
    exit 1
fi

# Check if GROQ_API_KEY is set in .env
if grep -q "GROQ_API_KEY=your_groq_api_key_here" .env; then
    echo "Please set your GROQ_API_KEY in the .env file."
    exit 1
fi

# Build and start the containers
echo "Building and starting Docker containers..."
docker-compose up -d

# Display access information
echo ""
echo "Upwork Proposal Generator is now running!"
echo ""
echo "Access the application at:"
echo "- API Documentation: http://localhost:8000/docs"
echo "- Streamlit Frontend: http://localhost:8501"
echo "- Flask Frontend: http://localhost:8502"
echo ""
