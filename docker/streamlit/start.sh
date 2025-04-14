#!/bin/bash

echo "Waiting for backend to be ready..."
until curl -s http://backend:8000/health > /dev/null; do
    echo "Backend not ready yet, waiting..."
    sleep 2
done
echo "Backend is ready, starting Streamlit..."

exec streamlit run src/frontend/app.py --server.port=8501 --server.address=0.0.0.0
