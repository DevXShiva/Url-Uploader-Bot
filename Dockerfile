# Debian 11 (Bullseye) use kar rahe hain jo stable hai
FROM python:3.10-slim-bullseye

WORKDIR /app

# Repository list ko clean karke update karne ka sahi tarika
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    jq \
    python3-dev \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Requirements install karein
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pura code copy karein
COPY . .

# Bot ko run karein
CMD ["python3", "bot.py"]
