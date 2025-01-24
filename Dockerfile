FROM python:3.12

WORKDIR /app

COPY log_service /app/log_service
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV GUNICORN_WORKERS=4
ENV APP_BIND="0.0.0.0:29501"
ENV METRICS_BIND="0.0.0.0:29502"
ENV PYTHONUNBUFFERED=1

EXPOSE 29501 29502

CMD ["gunicorn -w $GUNICORN_WORKERS -b $APP_BIND log_service.app:app & gunicorn -w 1 -b $METRICS_BIND log_service.app:metrics_app"]
