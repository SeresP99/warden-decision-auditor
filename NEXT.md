# NEXT

## Done (2026-11-24)
- Judge returns 401 on a missing or wrong internal key
- Stub judge checks the incoming key (401 if bad) and forwards it to the real judge
- Stub passes the real judge's status code through; 503 when the judge is down, times out, or sends bad JSON
- Judge returns 400 with rule_id invalid_event for unknown event types
- Tested with curl: no key -> 401, wrong key -> 401, right key -> judge answers
- Integration test: login_attempt via front door (8000) -> stub -> judge -> allow

## Next
1. Check the key before request.get_json() in the stub, so a keyless bad body gets 401, not 400
2. Log book: check the internal key too
3. Docs: reword the first internal-auth line; mention the stub-to-judge hop, 400s and 503s
4. Add pytest tests for no key / wrong key / right key (replace manual curl)
5. Keep test events in files and send with curl -d @event.json