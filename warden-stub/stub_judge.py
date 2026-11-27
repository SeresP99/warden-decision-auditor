import requests
from flask import Flask, request, jsonify
from common.internal_auth import INTERNAL_KEY_HEADER, internal_key_correct

app = Flask(__name__)


@app.get('/health')
def health():
    return jsonify({'status': 'ok'})


@app.before_request
def check_internal_key():
    if internal_key_correct(request):
        return None
    else:
        return jsonify({'decision': 'deny', 'reason': 'invalid_request', "rule_id": "invalid_internal_key"}), 401

@app.post('/decide')
def decide():
    try:
        payload = request.get_json()
        received_key = request.headers.get(INTERNAL_KEY_HEADER)
        headers = {INTERNAL_KEY_HEADER: received_key}
        real_judge_request = requests.post('http://localhost:8003/decide', json=payload, headers=headers, timeout=5)
        return jsonify(real_judge_request.json()), real_judge_request.status_code

    except requests.exceptions.JSONDecodeError as e:
        return jsonify({
            'decision': 'deny',
            'rule_id': 'bad_json',
            'reason': str(e)
        }), 503


    except requests.RequestException as e:
        return jsonify({
            'decision': 'deny',
            'rule_id': 'bad_request',
            'reason': str(e)
        }), 503


if __name__ == '__main__':
    app.run(port=8001)
