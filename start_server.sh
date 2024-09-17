#!/bin/bash

# Navigate to the 'root/api' directory
cd "$(dirname "$0")/api"

# Run the FastAPI server using uvicorn with reload enabled
uvicorn api:app --reload --host 0.0.0.0 --port 8080
