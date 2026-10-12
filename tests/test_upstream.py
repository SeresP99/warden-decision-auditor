import json
from pathlib import Path

from ingest.upstream import post_json


EXAMPLES_DIR = Path(__file__).parent.parent / "examples"
login_example_path = EXAMPLES_DIR / "login_attempt.json"

def test_login_attempt_successful_status_code():
    payload = json.loads(login_example_path.read_text())
    request_id = "test_id"

    judge_resp = post_json('http://localhost:8001/decide', payload, request_id)
    if judge_resp.error is not None:
        assert False
    else:
        decision = judge_resp.json

    assert judge_resp.full_response.status_code == 200

    auditor_resp = post_json("http://localhost:8002/log",
                             {
                                 "request_id": request_id,
                                 "event_type": payload.get("type"),
                                 "decision": decision.get("decision"),
                                 "rule_id": decision.get("rule_id"),
                                 "reason": decision.get("reason"),
                             },
                             request_id,
                             201
                             )

    if auditor_resp.error is not None:
        assert False

    assert auditor_resp.full_response.status_code == 201


def test_login_attempt_failure_status_judge_down():
    payload = json.loads(login_example_path.read_text())
    request_id = "test_id"

    judge_resp = post_json('http://localhost:8001/decide', payload, request_id)

    assert judge_resp.error is not None
    assert judge_resp.error.get('code') == 503


def test_login_attempt_failure_status_auditor_down():
    payload = json.loads(login_example_path.read_text())
    request_id = "test_id"

    judge_resp = post_json('http://localhost:8001/decide', payload, request_id)
    if judge_resp.error is not None:
        assert False
    else:
        decision = judge_resp.json

    assert judge_resp.full_response.status_code == 200

    auditor_resp = post_json("http://localhost:8002/log",
                             {
                                 "request_id": request_id,
                                 "event_type": payload.get("type"),
                                 "decision": decision.get("decision"),
                                 "rule_id": decision.get("rule_id"),
                                 "reason": decision.get("reason"),
                             },
                             request_id,
                             201
                             )

    assert auditor_resp.error is not None
    assert auditor_resp.error.get('code') == 503