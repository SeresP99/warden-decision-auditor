from flask import Flask, request, jsonify
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
    return jsonify({'request_id': request_id, 'status': 'accepted'})

if __name__ == '__main__':
    app.run(port=8000)