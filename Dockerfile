FROM python:3.10-slim

# Устанавливаем системные зависимости, если нужны (для asyncmy иногда полезно)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

# CMD оставляем как есть — он правильный
CMD ["python3", "-m", "src.server"]
