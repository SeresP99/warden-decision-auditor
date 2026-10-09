# Threat model

## Who calls it

Practice callers on a local laptop. Each caller has an API key. No public internet exposure in this version.

## What we protect

- **Decision integrity** — the stored allow/deny result and the rule that produced it. The hash chain makes an edited line detectable.
- **Caller identity** — only holders of a valid API key can submit events.
- **Absence of secrets** — passwords, tokens, and keys are stripped before anything is written to the log.

## What we accept

- A person with shell access to the machine can read or alter files.
- The log uses a hash chain, not cryptographic signatures.
- No high availability; if a program is down the front door fails closed.
- Practice data only. No real personal data, no live phishing pages, no crawling.

## Abuse cases we handle

- Request with a missing or wrong API key → rejected at the front door.
- Judge or log book unreachable → front door denies the request (fail closed).
- Someone edits a stored log line → the verify check fails.
- Password or key appears in an event → stripped or refused before the write.

## Abuse cases we do not handle

- A local attacker who can already read the process memory or the disk.
- Network attackers (the service is not exposed).
- Sophisticated lookalike domains beyond the simple hostname rules.