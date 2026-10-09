from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get('/health')
def health():
    return jsonify({'status': 'ok'})

@app.post('/decide')
def decide():
    # ignores the body for now, always denies
    return jsonify({
        'decision': 'deny',
        'rule_id': 'stub_deny',
        'reason': 'stub judge always denies'
    })

if __name__ == '__main__':
    app.run(port=8001)