import hmac
import os
from dotenv import load_dotenv

INTERNAL_KEY_HEADER = "X-Internal-Key"

load_dotenv()
INTERNAL_KEY = os.environ.get("WARDEN_INTERNAL_KEY")
if not INTERNAL_KEY:
    raise SystemExit("WARDEN_INTERNAL_KEY is not set")


def internal_key_correct(request):
    if request.path == "/health":
        return True

    received_key = request.headers.get(INTERNAL_KEY_HEADER, "")
    return hmac.compare_digest(received_key or "", INTERNAL_KEY)