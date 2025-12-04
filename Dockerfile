FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt && \
    find /install -name "*.pyc" -exec rm -f {} \;

FROM python:3.12-slim

RUN useradd -m -r appuser && \
    mkdir /app && chown -R appuser /app

COPY --from=builder /install /usr/local

WORKDIR /app
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

