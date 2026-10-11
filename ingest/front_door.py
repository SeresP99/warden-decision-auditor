from flask import Flask, request, jsonify
import requests
import secrets

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

    try:
        judge_resp = requests.post(
            'http://localhost:8001/decide',
            json=data,
            timeout=2)
        if judge_resp.status_code != 200:
            raise requests.RequestException()
        decision = judge_resp.json()
        
    except requests.exceptions.JSONDecodeError as e:
        return jsonify({
            'error': str(e),
            'request_id': request_id
        }), 500
    except requests.RequestException as e:
        return jsonify({
            'error': str(e),
            'request_id': request_id,
        }), 503

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
