from flask import Flask, request, jsonify
import json
from datetime import datetime, timedelta
import os
from prometheus_client import Gauge, generate_latest, REGISTRY
from threading import Thread, Lock

# cleaning metrics
def clear_default_metrics():
    collectors = list(REGISTRY._names_to_collectors.keys())
    for collector_name in collectors:
        try:
            REGISTRY.unregister(REGISTRY._names_to_collectors[collector_name])
        except KeyError:
            continue

clear_default_metrics()

# metrics vars
metrics_app = Flask(__name__)

last_updated = datetime.min
cached_line_count = 0
cache_lock = Lock()

CACHE_REFRESH_INTERVAL = timedelta(seconds=10)

# logfile vars
app = Flask(__name__)

log_line_count = Gauge("pp_service_request_log_lines", "Number of lines in the log file")

LOG_FILE = os.path.join(os.path.dirname(__file__), "request_logs.txt")


def count_log_lines():
    if not os.path.exists(LOG_FILE):
        return 0
    with open(LOG_FILE, 'r', encoding='utf-8') as log_file:
        return sum(1 for _ in log_file)


def update_metrics():
    global last_updated, cached_line_count
    with cache_lock:
        now = datetime.now()
        if now - last_updated >= CACHE_REFRESH_INTERVAL:
            cached_line_count = count_log_lines()
            log_line_count.set(cached_line_count)
            last_updated = now


@app.route('/', methods=['POST'])
def process_request():
    try:
        request_data = request.get_json()

        with open(LOG_FILE, 'a', encoding='utf-8') as log_file:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "data": request_data
            }
            log_file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

        return jsonify({"status": "success", "message": "Request logged"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@metrics_app.route('/metrics', methods=['GET'])
def metrics():
    update_metrics()
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}


def run_metrics_server():
    metrics_app.run(host='0.0.0.0', port=29502)


def main():
    metrics_thread = Thread(target=run_metrics_server)
    metrics_thread.daemon = True
    metrics_thread.start()

    app.run(host='0.0.0.0', port=29501)


if __name__ == '__main__':
    main()
