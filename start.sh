uv run python manage.py migrate --noinput
# uv run gunicorn minilib.wsgi
uv run python manage.py runserver 0.0.0.0:8000
