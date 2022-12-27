FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements-linux.txt .
RUN pip install -r requirements-linux.txt
COPY . .

CMD python manage.py runserver 0.0.0.0:8000
