FROM python:3.12-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "backlog_tracker_django.wsgi:application", "--bind", "0.0.0.0:8000"]