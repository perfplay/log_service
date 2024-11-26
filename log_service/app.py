from flask import Flask, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

LOG_FILE = os.path.join(os.path.dirname(__file__), "request_logs.txt")

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

def main():
    app.run(host='0.0.0.0', port=29501)