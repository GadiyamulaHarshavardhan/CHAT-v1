# ── Base image ──────────────────────────────────────
FROM python:3.11-slim

# Prevent Python from writing .pyc files & enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ── System dependencies ─────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ────────────────────────────────
WORKDIR /app

# ── Install Python deps (cached layer) ──────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy project ─────────────────────────────────────
COPY . .

# ── Make entrypoint executable ───────────────────────
RUN chmod +x /app/entrypoint.sh

# ── Expose Daphne port ───────────────────────────────
EXPOSE 8000

# ── Entrypoint ───────────────────────────────────────
ENTRYPOINT ["/app/entrypoint.sh"]
