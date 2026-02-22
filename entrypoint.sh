#!/bin/bash
set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Chat App — Starting up..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 1. Wait for PostgreSQL ───────────────────────────
echo "⏳ Waiting for PostgreSQL at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
while ! nc -z "${POSTGRES_HOST:-db}" "${POSTGRES_PORT:-5432}"; do
  sleep 1
done
echo "✅ PostgreSQL is ready!"

# ── 2. Wait for Redis ───────────────────────────────
echo "⏳ Waiting for Redis at ${REDIS_HOST}:${REDIS_PORT}..."
while ! nc -z "${REDIS_HOST:-redis}" "${REDIS_PORT:-6379}"; do
  sleep 1
done
echo "✅ Redis is ready!"

# ── 3. Run database migrations ───────────────────────
echo "🔄 Running migrations..."
python manage.py migrate --noinput

# ── 4. Create superuser if it doesn't exist ──────────
echo "👤 Checking superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
username = '${DJANGO_SUPERUSER_USERNAME:-admin}'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email='${DJANGO_SUPERUSER_EMAIL:-admin@example.com}',
        password='${DJANGO_SUPERUSER_PASSWORD:-admin}'
    )
    print(f'✅ Superuser \"{username}\" created!')
else:
    print(f'ℹ️  Superuser \"{username}\" already exists.')
"

# ── 5. Collect static files ─────────────────────────
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true

# ── 6. Start Daphne (ASGI server) ───────────────────
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 Starting Daphne on 0.0.0.0:8000"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
exec daphne -b 0.0.0.0 -p 8000 chatproject.asgi:application
