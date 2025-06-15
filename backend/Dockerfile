FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app/backend

RUN apt-get update && apt-get install -y postgresql-client

# Copy just the requirements file first (for cache-friendly installs)
# Now copy only the backend code (not the whole project)
COPY backend /app/backend
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

