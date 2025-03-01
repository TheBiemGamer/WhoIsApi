FROM python:3.9-slim
LABEL org.opencontainers.image.source https://github.com/thebiemgamer/whoisapi

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:5000", "whoisapi.app:app"]