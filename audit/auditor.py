from flask import Flask, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)
log = []

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/log")
def add():
    entry = request.get_json(silent=True) or {}
    entry['time'] = datetime.now(timezone.utc).isoformat()
    log.append(entry)
    return jsonify({"status": "logged"}), 201

@app.get("/decisions/<request_id>")
def get(request_id):
    for entry in log:
        if entry.get('request_id') == request_id:
            return jsonify(entry)
    return jsonify({"status": "not_found"}), 404

if __name__ == "__main__":
    app.run(port=8002)