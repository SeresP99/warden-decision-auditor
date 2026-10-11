from flask import Flask, request, jsonify
import requests
import secrets

from ingest.upstream import post_json

app = Flask(__name__)


@app.get('/health')
def health():
    return jsonify({'status': 'ok'})


@app.post('/events')
def events():
    data = request.get_json(silent=True) or {}
    if "type" not in data:
        return jsonify({'error': 'missing_type'}), 400

    request_id = 'req_' + secrets.token_hex(4)


    judge_resp = post_json('http://localhost:8001/decide', data, request_id)
    if judge_resp.error is not None:
        return jsonify({'error': judge_resp.error.message}), judge_resp.error.code
    else:
        decision = judge_resp.json

    try:
        auditor_resp = requests.post(
            "http://localhost:8002/log",
            json={
                "request_id": request_id,
                "event_type": data.get("type"),
                "decision": decision.get("decision"),
                "rule_id": decision.get("rule_id"),
                "reason": decision.get("reason"),
            },
            timeout=2,
        )
        if auditor_resp.status_code != 201:
            raise requests.RequestException()
    except requests.exceptions.JSONDecodeError as e:
        return jsonify({
            'error': str(e),
            'request_id': request_id
        }), 500
    except requests.RequestException as e:
        return jsonify({
            'error': str(e),
            'request_id': request_id
        }), 503

    


    return jsonify({'request_id': request_id, 'status': decision})


if __name__ == '__main__':
    app.run(port=8000)
