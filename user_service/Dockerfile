FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    cp .env.backup .env || true

EXPOSE 8000

CMD ["sh", "./entrypoint.sh"]
