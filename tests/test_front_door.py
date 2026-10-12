import json
from pathlib import Path

import requests

from ingest.upstream import post_json

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"
login_example_path = EXAMPLES_DIR / "login_attempt.json"

def test_login_attempt_front_door_failure_closed():
    response = requests.post("http://localhost:8000/events", json=json.loads(login_example_path.read_text()))
    assert response.status_code == 503

def test_login_attempt_front_door_happy_path():
    response = requests.post("http://localhost:8000/events", json=json.loads(login_example_path.read_text()))
    assert response.status_code == 200