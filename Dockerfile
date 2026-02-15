# Debian 11 (Bullseye) stable aur light image hai
FROM python:3.10-slim-bullseye

# Environment variables set karein takki logs turant dikhein
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# System dependencies install karein
# libffi-dev aur libssl-dev tgcrypto ke liye zaroori hain
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    jq \
    python3-dev \
    build-essential \
    libffi-dev \
    libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Pip upgrade aur requirements install karein
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pura project code copy karein
COPY . .

# bot.py hi app.py (Flask) ko thread ke through start karega
# Isse Render ka port binding error nahi aayega
CMD ["python3", "bot.py"]
