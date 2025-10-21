FROM python:3.11-slim

# —— Security: Create non-root user ——————————————————————————————
RUN groupadd -r appuser && useradd -r -g appuser appuser

# —— Runtime env ————————————————————————————————————————————————
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

WORKDIR /app

# —— Deps ————————————————————————————————————————————————————————
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install curl

# —— App —————————————————————————————————————————————————————————
COPY app ./app
COPY scripts ./scripts

# —— Security: Create directories and set permissions ————————————
RUN mkdir -p /app/EVIDENCE /app/solutions /app/logs && \
    chown -R appuser:appuser /app && \
    chmod +x /app/scripts/*.sh

# —— Security: Switch to non-root user ———————————————————————————
USER appuser

# —— Healthcheck ——————————————————————————————————————————————————
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

EXPOSE 8000

# —— S06: One-liner integration ———————————————————————————————————
# Инициализация БД на старте контейнера (простая семинарская логика)
CMD python scripts/init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000