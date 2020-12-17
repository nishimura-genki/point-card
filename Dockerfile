FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1]

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

ENV PORT 8080

CMD exec gunicorn --bind 0.0.0.0:${PORT} config.wsgi:application