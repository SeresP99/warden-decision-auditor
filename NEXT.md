# NEXT

## Done (2026-11-22)
- Shared header name in common/internal_auth.py (X-Internal-Key)
- Key loaded from .env via python-dotenv; exits if WARDEN_INTERNAL_KEY is missing
- .env.example added, .env ignored
- decision-api.md documents the header, env var and 401
- Judge: before_request checks the key (skips /health)

## Next
1. Commit the judge check, then run all three and confirm a request without the key gets 401.
2. Front door: pass {INTERNAL_KEY_HEADER: INTERNAL_KEY} to both post_json calls (if not done).
3. Stub judge: forward the key when it calls the real judge.
4. Log book: check the key too.
5. Docs: reword the first internal-auth line; mention the stub-to-judge hop.