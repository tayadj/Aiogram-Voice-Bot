FROM python:3.12.6-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN alembic -c ./src/data/alembic.ini upgrade head

WORKDIR /app

CMD ["python", "src/main.py"]