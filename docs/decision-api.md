# Decision API

The contract both (stub and real) judges must match. The front door depends on this page, not on a particular rule file.

## Event in

Three kinds only. Extra fields are dropped and not stored.

## Internal Authentication

Internal environment variable gets passed for each module endpoint call. Name of header: X-Internal-Key

### login_attempt
```json
{
  "type": "login_attempt",
  "account": "ada",
  "success": false
}
```

### admin_action
```json
{
  "type": "admin_action",
  "account": "ada",
  "role": "user",
  "action": "delete_user"
}
```


### url_check
```json
{
  "type": "url_check",
  "url": "https://apple.evil.example"
}
```

## Reply out
Both judges return this shape and nothing else is required:
```json
{
  "decision": "deny",
  "rule_id": "too_many_failures",
  "reason": "5 failures in 10 minutes"
}
```