import hmac

import requests
from flask import Flask, request, jsonify
from common.internal_auth import INTERNAL_KEY, INTERNAL_KEY_HEADER

app = Flask(__name__)


@app.get('/health')
def health():
    return jsonify({'status': 'ok'})


@app.post('/decide')
def decide():
    try:
        payload = request.get_json()
        received_key = request.headers.get(INTERNAL_KEY_HEADER)
        headers = str({INTERNAL_KEY_HEADER: received_key})
        if not hmac.compare_digest(received_key or "", INTERNAL_KEY):
            raise requests.RequestException
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
        }), 401


if __name__ == '__main__':
    app.run(port=8001)
