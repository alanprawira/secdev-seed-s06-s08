
FROM python:3.11.9-slim

# —— Runtime env ————————————————————————————————————————————————
ENV PYTHONDONTWRITEBYTECODE=1         PYTHONUNBUFFERED=1         PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

# —— Deps ————————————————————————————————————————————————————————
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# —— App —————————————————————————————————————————————————————————
COPY app ./app
COPY scripts ./scripts

EXPOSE 8000

# Инициализация БД на старте контейнера (простая семинарская логика)
CMD python scripts/init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000

HEALTHCHECK --interval=10s --timeout=3s --retries=5 CMD python -c "import urllib.request as u; u.urlopen('http://127.0.0.1:8000/').read()" || exit 1

RUN useradd -m -u 10001 appuser && chown -R appuser:appuser /app
USER appuser
