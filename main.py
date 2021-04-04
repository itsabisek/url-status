from flask import Flask, request
from flask_cors import CORS
from logger_utils import bootstrap_logger
from utils import generate_payload, check_status, authenticate
from utils import STATUS_OK, STATUS_MALFORMED_QUERY_STRING, STATUS_CRAWL_ERROR, RESPONSE_OK, RESPONSE_UNAUTHORIZED

logger = bootstrap_logger(__name__)

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
            logger.exception("Exception while trying to crawl")
            return generate_payload(args['url'], None, STATUS_CRAWL_ERROR), RESPONSE_OK

    logger.warning("Query string is either malformed or doesn't exists")
    return generate_payload(None, None, STATUS_MALFORMED_QUERY_STRING), RESPONSE_OK

@app.errorhandler(403)
def forbidden_403(exec):
    logger.warning("Authenticaion failure!!")
    return generate_payload(None, None, STATUS_CRAWL_ERROR), RESPONSE_UNAUTHORIZED
