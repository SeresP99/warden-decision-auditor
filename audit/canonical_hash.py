import json
import hashlib

def canonical(entry: dict) -> str:
    return json.dumps(entry, sort_keys=True, separators=(',', ':'))

def hash_entry(entry: dict) -> str:
    return hashlib.sha256(canonical(entry).encode('utf-8')).hexdigest()
