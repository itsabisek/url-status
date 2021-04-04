import os
import json
import requests
import base64
from logger_utils import bootstrap_logger
from flask import request, abort

logger = bootstrap_logger(__name__)

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
    logger.info(f"Dumping payload data {p}")
    return p

def check_status(url):
    def _append_protocol(url):
        if "http://" not in url or "https://" not in url:
            url = f"https://{url}"
        return url
    
    url = _append_protocol(url)
    logger.info(f"Making request to - {url}")
    resp = requests.get(url)
    logger.info(f"Response - {resp}")
    return resp.status_code

def authenticate(service_func):
    def wrapper(*args, **kwargs):
        username = request.authorization and request.authorization.username
        password = request.authorization and request.authorization.password
        check_username = os.environ.get('AUTH_USER', "username")
        check_pass = os.environ.get("AUTH_PASS", "password")
        logger.info(f"Authentication - {username is None} | {password is None} | {check_username is "username"} | {check_pass is "password"}")
        if not username == check_username or not password == check_pass:
            abort(403)
        return service_func(*args, **kwargs)
    return wrapper
