from flask import Flask, request
from flask_cors import CORS
from utils import generate_payload, check_status, authenticate
from utils import STATUS_OK, STATUS_MALFORMED_QUERY_STRING, STATUS_CRAWL_ERROR, RESPONSE_OK, RESPONSE_UNAUTHORIZED

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"Origins": '*'}})

@app.route("/api/check", methods=["GET"])
@authenticate
def check():
    args = request.args
    if 'url' in args:
        try:
            output = check_status(args['url'])
            return generate_payload(args['url'], output, STATUS_OK), RESPONSE_OK
        except:
            return generate_payload(args['url'], None, STATUS_CRAWL_ERROR), RESPONSE_OK

    return generate_payload(None, None, STATUS_MALFORMED_QUERY_STRING), RESPONSE_OK

@app.errorhandler(403)
def forbidden_403(exec):
    return generate_payload(None, None, STATUS_CRAWL_ERROR), RESPONSE_UNAUTHORIZEDq
