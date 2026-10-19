from flask import Flask, request, jsonify
from datetime import datetime, timezone
from canonical_hash import canonical, hash_entry

app = Flask(__name__)
log = []
previous_entry_hash = '0'


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/verify")
def verify():
    intact = True
    for i in range(len(log) - 1, -1, -1):
        if i == 0 and log[i]['prev_hash'] != '0':
            intact = False
            break
        elif log[i]['prev_hash'] != hash_entry(log[i - 1]) and i != 0:
            intact = False
            break

    return jsonify({"status": "ok", "log_integrity": "intact" if intact else "compromised"}), 200


@app.post("/log")
def add():
    global previous_entry_hash

    entry = request.get_json(silent=True) or {}
    entry['time'] = datetime.now(timezone.utc).isoformat()
    entry['prev_hash'] = previous_entry_hash
    previous_entry_hash = hash_entry(entry)
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
