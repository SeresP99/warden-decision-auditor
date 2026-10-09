# Warden Decision Auditor

Events in. Allow or deny out. Decision saved so you can check it later.

Three small programs. One public door.

```text
caller
  |
  |  POST /events          (only public port)
  v
front door  ---- request id, event ---->  judge
  |                                          |
  |                                          | allow or deny, rule id, reason
  | <----------------------------------------+
  |
  |  same decision, no password
  v
log book  ---- stores the line, fingerprints the previous line
  |
  |  GET /decisions/{request_id}
  v
caller, or you, reading it back
```

### Six-line demo (planned)

1. Send a bad login attempt to the front door.
2. The judge denies it with rule too_many_failures.
3. The log line is written with a request id and no password.
4. Look up the request id and see the same id in all three logs.
5. Edit one log line.
6. The verify check fails.

### Layout

`ingest/` — front door (only public port)  
`warden/` — real judge  
`warden-stub/` — stub judge  
`audit/` — log book  
`examples/` — sample events  
`docs/decision-api.md` — the contract both judges must match  
`docs/threat-model.md` — what we protect and what we accept
