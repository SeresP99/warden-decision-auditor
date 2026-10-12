import requests

class UpstreamResult:
    def __init__(self, request_id, response=None, error=None, body=None):
        self.request_id = request_id
        self.full_response = response
        self.error = error
        self.json = body

    @property
    def ok(self):
        return self.error is None

def post_json(url: str, payload: dict, request_id, expected_status: int = 200, timeout = 2):
    call_result = UpstreamResult(request_id)
    try:
        call_result.full_response = requests.post(url, json=payload, timeout=timeout)
        if call_result.full_response.status_code != expected_status:
            raise requests.RequestException(f"Request failed and closed with status code {call_result.full_response.status_code}")
        call_result.json = call_result.full_response.json()

    except requests.exceptions.JSONDecodeError as e:
        call_result.error = { 'message': str(e), 'code': 503 }


    except requests.RequestException as e:
        call_result.error = {'message': str(e), 'code': 503}

    return call_result