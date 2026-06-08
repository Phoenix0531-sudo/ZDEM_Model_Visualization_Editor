FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required by PySide6
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libegl1-mesa \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default: verify imports (GUI will not run in Docker)
CMD ["python", "-c", "from zdem_editor.core.models import ZDEMModel; print('Import OK')"]
