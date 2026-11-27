import json
from pathlib import Path
from warden.judge import app
from common.internal_auth import INTERNAL_KEY_HEADER, INTERNAL_KEY

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"
login_deny_example_path = EXAMPLES_DIR / "login_attempt.json"
login_allow_example_path = EXAMPLES_DIR / "login_allow.json"
test_judge = app.test_client()


def test_no_internal_key():
    payload = json.loads(login_allow_example_path.read_text())
    response = test_judge.post("/decide", json=payload)
    response_body = response.get_json()
    assert response.status_code == 401
    assert response_body["rule_id"] == "invalid_internal_key"

def test_wrong_internal_key():
    payload = json.loads(login_allow_example_path.read_text())
    headers = {INTERNAL_KEY_HEADER: "wrong"}
    response = test_judge.post("/decide", json=payload, headers=headers)
    response_body = response.get_json()
    assert response.status_code == 401
    assert response_body["rule_id"] == "invalid_internal_key"

def test_correct_internal_key():
    payload = json.loads(login_allow_example_path.read_text())
    headers = {INTERNAL_KEY_HEADER: INTERNAL_KEY}
    payload[INTERNAL_KEY_HEADER] = INTERNAL_KEY
    response = test_judge.post("/decide", json=payload, headers=headers)
    response_body = response.get_json()
    assert response.status_code == 200
    assert response_body["rule_id"] == "none"
    assert response_body["decision"] == "allow" or "deny"