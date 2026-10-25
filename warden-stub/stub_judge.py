import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.get('/health')
def health():
    return jsonify({'status': 'ok'})


@app.post('/decide')
def decide():
    try:
        payload = request.get_json
        real_judge_request = requests.post('http://localhost:8003/decide', json=payload())
        return jsonify(real_judge_request.json())

    except requests.exceptions.JSONDecodeError as e:
        return jsonify({
            'decision': 'deny',
            'rule_id': 'bad_json',
            'reason': str(e)
        })


    except requests.RequestException as e:
        return jsonify({
            'decision': 'deny',
            'rule_id': 'bad_request',
            'reason': str(e)
        })


if __name__ == '__main__':
    app.run(port=8001)
