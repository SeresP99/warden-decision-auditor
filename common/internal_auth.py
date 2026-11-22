import os
from dotenv import load_dotenv

INTERNAL_KEY_HEADER = "X-Internal-Key"

load_dotenv()
INTERNAL_KEY = os.environ.get("WARDEN_INTERNAL_KEY")
if not INTERNAL_KEY:
    raise SystemExit("WARDEN_INTERNAL_KEY is not set")