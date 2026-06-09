# Build/test environment only — GUI requires display server (X11/Wayland)
FROM python:3.11-slim

ENV PYTHONPATH=/app
WORKDIR /app

# Install system dependencies for tkinter and matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    tk-dev \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Smoke test: verify imports (GUI will not render in Docker)
CMD ["python", "scripts/docker_smoke_test.py"]
