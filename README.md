# Log Service

A lightweight service for logging JSON requests and exposing Prometheus metrics.

## Features
- Logs incoming POST requests.
- Provides `/metrics` endpoint for Prometheus.
- Uses Bearer token authorization.

## Quick Start

1. **Clone the repository:**

`git clone <REPOSITORY_URL> cd log_service`

2. **Set your Bearer token in `nginx/nginx.conf`:**

`"Bearer YOUR_TOKEN_HERE" "true";`

3. **Run with Docker Compose:**

`docker-compose up --build -d`

4. **Test the service:**

```bash
curl -X POST http://127.0.0.1:29501
-H "Authorization: Bearer my_secret_token"
-H "Content-Type: application/json"
-d '{"device_id": "123111", "user_id": "456111", "error": "Test error"}'

curl http://127.0.0.1:29502/metrics
```

## Environment Variables
- `GUNICORN_WORKERS` (default: `4`)
- `APP_BIND` (default: `0.0.0.0:29501`)
- `METRICS_BIND` (default: `0.0.0.0:29502`)

Configure these in `docker-compose.yml`.

## Local Development
Install dependencies with Poetry:
`poetry install`

Run locally:
`poetry run python log_service/app.py`


## License
MIT License
