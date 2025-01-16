from flask import Flask, jsonify
import whois, re
from datetime import datetime

app = Flask(__name__)

@app.route("/whois/<path:domain>")
def who_is(domain):
    try:
        if not is_valid_domain(domain):
            return jsonify({"error": "Invalid domain name"}), 400
        
        data = whois.whois(domain)
        
        if not data or not data.get("domain_name"):
            return jsonify({"error": f"No WHOIS data found for {domain}"}), 404
        
        return jsonify(data)
    
    except Exception as e:
        return jsonify({"error": "An error occured while fetching WHOIS data", "details": str(e)}), 500
    
def is_valid_domain(domain):
    domain_regex = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.(?!-)[A-Za-z]{2,}$"
    return re.match(domain_regex, domain)

def format_data(value):
    if isinstance(value, list):
        return [format_data(item) for item in value]
    elif isinstance(value, datetime):
        return value.isoformat()
    return value

if __name__ == "__main__":
    app.run(debug=True)