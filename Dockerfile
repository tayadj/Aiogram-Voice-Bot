FROM python:3.12.6-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/src/data

RUN alembic upgrade head

WORKDIR /app

CMD ["python", "src/main.py"]
