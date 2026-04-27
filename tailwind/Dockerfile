# Use official Python 3.11 slim image for a lightweight, secure container
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Upgrade pip and install fundamental dependencies
RUN pip install --upgrade pip

# Copy only the requirements first to cache the layer (speeds up future builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Expose port (Render overrides this, but good practice for local Docker tests)
EXPOSE 8000

# Production ASGI server: gunicorn + uvicorn worker
# Render injects $PORT at runtime; default to 8000 for local Docker testing
CMD gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}
