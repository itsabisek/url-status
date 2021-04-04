import json
import requests
from flask import Flask, request
from flask_cors import CORS

STATUS_OK = 1
STATUS_MALFORMED_QUERY_STRING = 2
STATUS_CRAWL_ERROR = 3
RESPONSE_OK = 200

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"Origins": '*'}})

@app.route("/api/check", methods=["GET"])
def check():
    args = request.args
    if 'url' in args:
        try:
            output = _check_status(args['url'])
            return __generate_payload(args['url'], output, STATUS_OK), RESPONSE_OK
        except:
            return __generate_payload(args['url'], None, STATUS_CRAWL_ERROR), RESPONSE_OK

    return __generate_payload(None, None, STATUS_MALFORMED_QUERY_STRING), RESPONSE_OK

def __generate_payload(url, output, error):
    p = json.dumps(
        dict(
            url=url,
            output=output,
            error=error
        )
    )
    print(p)
    return p

def _check_status(url):
    def _append_protocol(url):
        if "http://" not in url or "https://" not in url:
            url = f"https://{url}"
        return url
    
    url = _append_protocol(url)
    print(f"Making request - {url}")
    resp = requests.get(url)
    return resp.status_code