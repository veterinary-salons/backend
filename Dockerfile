
FROM python:3.11-slim

RUN mkdir /app

COPY requirements.txt /app

RUN python -m pip install --upgrade pip

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./ /app
 
WORKDIR /app

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]
