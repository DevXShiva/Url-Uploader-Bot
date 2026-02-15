# Stable Python image use karein (Debian-based)
FROM python:3.10-slim-buster

# Working directory set karein
WORKDIR /app

# System dependencies install karein (apt-get yahan kaam karega)
RUN apt-get update && \
    apt-get install -y ffmpeg jq python3-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Requirements file copy aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki saara code copy karein
COPY . .

# Bot start karein
CMD ["python3", "bot.py"]
