from flask import Flask, jsonify, render_template, request
import whois
import re
import os
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ENABLE_RATE_LIMIT = os.getenv("ENABLE_RATE_LIMIT", "True").lower() == "true"

if ENABLE_RATE_LIMIT:
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=["5 per minute", "100 per hour", "500 per day"],
    )

    @limiter.request_filter
    def exempt_requests():
        """Allow exemptions (e.g., internal requests if needed)"""
        return False

    @app.errorhandler(429)
    def ratelimit_exceeded(e):
        return jsonify(
            {
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please slow down.",
            }
        ), 429
else:
    limiter = None


@app.route("/")
def index():
    return render_template("index.html")


# deprecated use whois_via_query instead
@app.route("/whois/<path:domain>")
@limiter.limit("1 per second")
def whois_via_path(domain):
    response_data, status_code = get_whois_response(domain)
    return jsonify(response_data), status_code


@app.route("/whois")
@limiter.limit("1 per second")
def whois_via_query():
    domain = request.args.get("domain")
    if not domain:
        return jsonify(
            {"error": "Domain not provided. Please use the 'domain' parameter."}
        ), 400
    response_data, status_code = get_whois_response(domain)
    return jsonify(response_data), status_code


def is_valid_domain(domain):
    domain_regex = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.(?!-)[A-Za-z]{2,}$"
    return re.match(domain_regex, domain)


def format_data(value):
    if isinstance(value, list):
        return [format_data(item) for item in value]
    elif isinstance(value, datetime):
        return value.isoformat()
    return value


def get_whois_response(domain):
    try:
        if not is_valid_domain(domain):
            return {"error": "Invalid domain name"}, 400

        data = whois.whois(domain)

        if not data or not data.get("domain_name"):
            return {"error": f"No WHOIS data found for {domain}"}, 404

        formatted_data = {key: format_data(value) for key, value in data.items()}
        return formatted_data, 200

    except Exception as e:
        return {
            "error": "An error occurred while fetching WHOIS data",
            "details": str(e),
        }, 500


if __name__ == "__main__":
    app.run(debug=True)
