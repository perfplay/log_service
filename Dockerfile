FROM python:3.12

WORKDIR /app

COPY log_service /app/log_service
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:29501", "log_service.app:app"]
