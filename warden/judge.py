from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({'status': 'ok'})

@app.get("/decide")
def decide():
     return jsonify({"decision": "allow/deny", "rule_id": "1", "reason": "..."})

if __name__ == "__main__":
     app.run(port=8003)