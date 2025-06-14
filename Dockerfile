FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y tesseract-ocr && pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["./scripts/run.sh"]
