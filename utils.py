import os
import json
import requests
import base64
from flask import request, abort

STATUS_OK = 1
STATUS_MALFORMED_QUERY_STRING = 2
STATUS_CRAWL_ERROR = 3
RESPONSE_OK = 200
RESPONSE_UNAUTHORIZED = 403

def generate_payload(url, output, error):
    p = json.dumps(
        dict(
            url=url,
            output=output,
            error=error
        )
    )
    print(p)
    return p

def check_status(url):
    def _append_protocol(url):
        if "http://" not in url or "https://" not in url:
            url = f"https://{url}"
        return url
    
    url = _append_protocol(url)
    print(f"Making request - {url}")
    resp = requests.get(url)
    return resp.status_code

def authenticate(service_func):
    def wrapper(*args, **kwargs):
        username = request.authorization and request.authorization.username
        password = request.authorization and request.authorization.password
        check_username = os.environ.get('AUTH_USER', "username")
        check_pass = os.environ.get("AUTH_PASS", "password")
        if not username == check_username or not password == check_pass:
            abort(403)
        return service_func(*args, **kwargs)
    return wrapper
