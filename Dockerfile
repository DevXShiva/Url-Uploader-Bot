# Stable image use karein
FROM python:3.10-slim-buster

WORKDIR /app

# Error 100 se bachne ke liye mirrors ko clean aur update karein
RUN apt-get update --fix-missing && \
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

# Bot run karein
CMD ["python3", "bot.py"]
