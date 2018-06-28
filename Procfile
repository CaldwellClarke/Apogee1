web: gunicorn apogee1.wsgi.py
web: python manage.py makemigrations
web: python manage.py migrate
web: python manage.py runserver 0.0.0.0:$PORT