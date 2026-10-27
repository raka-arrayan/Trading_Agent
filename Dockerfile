# Gunakan base image Python 3.12 slim yang ringan dan resmi
FROM python:3.12-slim

# Hindari pembuatan file .pyc dan aktifkan log output unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Jakarta

# Tetapkan direktori kerja
WORKDIR /app

# Install dependensi sistem dasar untuk zona waktu & font visualisasi
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Salin requirements dan install library python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode proyek ke dalam kontainer
COPY . .

# Default command: menjalankan daily news collector
CMD ["python", "scripts/daily_news_collector.py"]
