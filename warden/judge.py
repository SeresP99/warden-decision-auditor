import datetime
from collections import defaultdict

from flask import Flask, jsonify, request

app = Flask(__name__)

failure_store = defaultdict(list)


def check_login_attempt(event):
    account = event['account']
    success = event['success']
    login_attempt = {"datetime": datetime.datetime.now(), "success": success}
    failure_store[account].append(login_attempt)

    if len(failure_store[account]) > 5:
        return "deny"

    elif success:
        failure_store[account].clear()

    return "allow"


def check_admin_action(event):
    return 0


def check_url(event):
    return 0


@app.get("/health")
def health():
    return jsonify({'status': 'ok'})


@app.post("/decide")
def decide():
    event = request.get_json(silent=True) or {}
    event_type = event.get('type')

    match event_type:
        case 'login_attempt':
            check_login_attempt(event)
        case _:
            return jsonify({'decision': 'deny', 'reason': 'Invalid Request', "rule_id": "invalid request"})

    return jsonify({"decision": "allow", "rule_id": "1", "reason": "..."})


if __name__ == "__main__":
    app.run(port=8003)
