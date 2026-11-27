# NEXT

## Done (2026-11-27)
- Shared internal key check (internal_key_correct) in common/internal_auth.py, used as a before_request hook in judge and stub
- Stub now checks the key before reading the body; old inline check removed
- Renamed warden-stub to warden_stub so it can be imported
- Added examples/login_allow.json
- Pytest auth tests for judge and stub (no key, wrong key, right key) using Flask's test client
- Curl check: front door end-to-end allow, stub/judge 401 without key, health 200

## Next
1. Stub right-key test: fake the forward to the judge with unittest.mock.patch so it runs without the judge up
2. Log book: check the internal key (not on /health), plus pytest tests
3. Front door: pass the judge's 400/401 through instead of turning them into 503
4. Fix the old tests so pytest runs in one go (PYTHONPATH=. and no live-server dependence)
5. Docs: reword the internal-auth line; mention the stub-to-judge hop, 400s and 503s