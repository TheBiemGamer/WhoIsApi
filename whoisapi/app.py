from flask import Flask, jsonify, render_template_string, send_from_directory, request
import whois, re, os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>WHOIS Lookup</title>
      <link rel="icon" type="image/x-icon" href="favicon.ico">
      <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
      <style>
        /* Default (dark) theme variables */
        :root {
          --bg-color: #121212;
          --text-color: #ffffff;
          --input-bg: #1e1e1e;
          --button-bg: #007BFF;
          --button-hover: #0056b3;
          --result-bg: #1e1e1e;
          --link-color: #007BFF;
          --error-color: #ff4d4d;
          --shadow-color: rgba(0, 0, 0, 0.2);
        }
        /* Light theme overrides */
        body.light-theme {
          --bg-color: #f4f4f9;
          --text-color: #333;
          --input-bg: #ffffff;
          --button-bg: #007BFF;
          --button-hover: #0056b3;
          --result-bg: #f9f9f9;
          --link-color: #007BFF;
          --error-color: #ff4d4d;
          --shadow-color: rgba(0, 0, 0, 0.1);
        }
        
        body {
          font-family: Arial, sans-serif;
          background-color: var(--bg-color);
          color: var(--text-color);
          margin: 0;
          padding: 0;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          transition: background-color 0.3s, color 0.3s;
        }
        
        .container {
          background: var(--input-bg);
          padding: 30px;
          border-radius: 10px;
          box-shadow: 0 4px 10px var(--shadow-color);
          max-width: 600px;
          width: 100%;
          text-align: center;
          position: relative;
          animation: slideIn 0.8s ease-out;
        }
        
        @keyframes slideIn {
          from { transform: translateY(30px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }
        
        h1 {
          color: var(--button-bg);
          font-size: 2rem;
          margin-bottom: 20px;
          animation: fadeIn 1s ease-in-out;
        }
        
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        
        .form-group {
          margin-bottom: 20px;
        }
        
        input[type="text"] {
          width: 100%;
          padding: 15px;
          font-size: 16px;
          background-color: var(--input-bg);
          border: 1px solid var(--button-bg);
          border-radius: 5px;
          color: var(--text-color);
          box-sizing: border-box;
          transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
          border-color: var(--button-hover);
          outline: none;
        }
        
        button {
          background-color: var(--button-bg);
          color: var(--text-color);
          font-size: 16px;
          padding: 10px 20px;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          transition: background-color 0.3s, transform 0.2s;
        }
        
        button:hover {
          background-color: var(--button-hover);
          transform: scale(1.02);
        }
        
        /* Loading indicator: initially hidden (max-height 0, no margin) and then animated in */
        .loading {
          overflow: hidden;
          max-height: 0;
          opacity: 0;
          margin-top: 0;
          font-size: 1.5rem;
          color: var(--text-color);
          transition: max-height 0.5s ease, opacity 0.3s ease, margin-top 0.5s ease;
        }
        .loading.active {
          max-height: 60px;
          opacity: 1;
          margin-top: 20px;
        }
        
        /* Result container: initially hidden and then expands and fades in */
        .result {
          overflow: hidden;
          max-height: 0;
          opacity: 0;
          margin-top: 0;
          transition: max-height 0.5s ease, opacity 0.5s ease, margin-top 0.5s ease, padding 0.5s ease;
          padding: 0 15px;
          border: 1px solid var(--button-bg);
          border-radius: 5px;
          text-align: left;
          font-family: monospace;
        }
        .result.show {
          max-height: 800px; /* high enough to contain the content */
          opacity: 1;
          margin-top: 20px;
          padding: 15px;
        }
        
        .error {
          color: var(--error-color);
        }
        
        pre {
          white-space: pre-wrap;
          word-wrap: break-word;
          margin: 0;
        }
        
        /* Styling for the parsed WHOIS information */
        .whois-info {
          text-align: left;
          margin-top: 10px;
        }
        .whois-field {
          margin-bottom: 10px;
          display: flex;
          align-items: center;
        }
        .field-icon {
          margin-right: 10px;
          color: var(--button-bg);
          width: 24px;
          text-align: center;
        }
        .field-label {
          font-weight: bold;
          margin-right: 5px;
          min-width: 120px;
        }
        .field-value {
          flex: 1;
          word-wrap: break-word;
        }
        
        footer {
          margin-top: 20px;
          font-size: 1rem;
        }
        
        footer a {
          color: var(--link-color);
          text-decoration: none;
          margin: 0 10px;
        }
        
        footer a:hover {
          color: var(--button-hover);
        }
        
        .icon {
          font-size: 1.5rem;
          margin-right: 10px;
          color: var(--link-color);
        }
        
        .icon:hover {
          color: var(--button-hover);
        }
        
        .theme-switcher {
          position: absolute;
          top: 20px;
          right: 20px;
          cursor: pointer;
          font-size: 1.5rem;
          color: var(--text-color);
          transition: transform 0.3s ease;
        }
        
        .theme-switcher:hover {
          color: var(--button-hover);
        }
        
        .theme-switcher:active {
          transform: rotate(20deg);
        }
        
        /* Ensure spinner rotates (in case Font Awesome's default doesn't work) */
        .fas.fa-spinner {
          animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      </style>
    </head>
    <body>
      <i class="fas fa-adjust theme-switcher" title="Toggle Theme" onclick="toggleTheme()"></i>
      <div class="container">
        <h1>WHOIS Lookup</h1>
        <div class="form-group">
          <input type="text" id="domain" placeholder="Enter domain (e.g., example.com)" autofocus>
        </div>
        <button onclick="fetchWhois()">Fetch WHOIS</button>
        <div class="loading" id="loading"><i class="fas fa-spinner"></i> Fetching data...</div>
        <div class="result" id="result"></div>
        <footer>
          <a href="https://pypi.org/project/python-whois/" target="_blank" title="Python-Whois Library">
            <i class="fas fa-book icon"></i>
          </a>
          <a href="https://github.com/TheBiemGamer/WhoIsApi" target="_blank" title="Source Code">
            <i class="fa-brands fa-github icon"></i>
          </a>
        </footer>
      </div>
      
      <script>
        // Set dark theme as default
        document.body.classList.add('dark-theme');

        // This function attempts to parse a date string.
        // It first tries the standard ISO format. If that fails and the string contains slashes,
        // it rearranges the European-style date (dd/mm/yyyy) into an ISO-like format.
        function parseDateString(dateStr) {
          let parsed = Date.parse(dateStr);
          if (!isNaN(parsed)) {
            return new Date(parsed).toLocaleString();
          }
          // Check for European-style date format with slashes
          if (dateStr.indexOf('/') !== -1) {
            // Separate the date and time parts if available
            let parts = dateStr.split(',');
            let datePart = parts[0].trim();
            let timePart = parts[1] ? parts[1].trim() : "00:00:00";
            let dateComponents = datePart.split('/');
            if(dateComponents.length === 3) {
              let [day, month, year] = dateComponents;
              day = day.padStart(2, '0');
              month = month.padStart(2, '0');
              let isoString = `${year}-${month}-${day}T${timePart}`;
              parsed = Date.parse(isoString);
              if (!isNaN(parsed)) {
                return new Date(parsed).toLocaleString();
              }
            }
          }
          return dateStr;
        }

        // For fields defined as type "date", only use the first value (if an array) and format it.
        function formatDateField(value) {
          if (Array.isArray(value)) {
            return parseDateString(value[0]);
          }
          return parseDateString(value);
        }

        // For non-date fields, if the value is an array show all items joined by commas.
        function formatDefaultField(value) {
          if (Array.isArray(value)) {
            return value.join(', ');
          }
          return value;
        }

        // Parse the WHOIS JSON and build a formatted HTML summary.
        // We add a "type" property so that date fields are handled differently.
        function parseWhoisData(data) {
          const fields = [
            { key: "domain_name", label: "Domain Name", icon: "fa-globe", type: "default" },
            { key: "registrar", label: "Registrar", icon: "fa-building", type: "default" },
            { key: "creation_date", label: "Creation Date", icon: "fa-calendar-plus", type: "date" },
            { key: "expiration_date", label: "Expiration Date", icon: "fa-calendar-times", type: "date" },
            { key: "updated_date", label: "Updated Date", icon: "fa-calendar-check", type: "date" },
            { key: "name_servers", label: "Name Servers", icon: "fa-server", type: "default" },
            { key: "emails", label: "Emails", icon: "fa-envelope", type: "default" },
            { key: "status", label: "Status", icon: "fa-info-circle", type: "default" },
            { key: "dnssec", label: "DNSSEC", icon: "fa-shield-alt", type: "default" }
          ];
          
          let html = '<h3>WHOIS Data:</h3><div class="whois-info">';
          fields.forEach(field => {
            if (data[field.key]) {
              let formattedValue;
              if (field.type === "date") {
                formattedValue = formatDateField(data[field.key]);
              } else {
                formattedValue = formatDefaultField(data[field.key]);
              }
              html += `<div class="whois-field">
                <i class="fas ${field.icon} field-icon"></i>
                <span class="field-label">${field.label}:</span>
                <span class="field-value">${formattedValue}</span>
              </div>`;
            }
          });
          html += '</div>';
          return html;
        }

        // Fetch WHOIS data with smooth animations.
        async function fetchWhois() {
          const domain = document.getElementById('domain').value.trim();
          const resultDiv = document.getElementById('result');
          const loadingDiv = document.getElementById('loading');
          
          // Clear previous results and collapse the result div.
          resultDiv.innerHTML = '';
          resultDiv.classList.remove('show');
          
          // Show the loading spinner.
          loadingDiv.classList.add('active');

          if (!domain) {
            resultDiv.innerHTML = '<p class="error">Please enter a domain name.</p>';
            resultDiv.classList.add('show');
            loadingDiv.classList.remove('active');
            return;
          }

          try {
            const response = await fetch(`/whois/${domain}`);
            const data = await response.json();

            if (response.ok) {
              resultDiv.innerHTML = parseWhoisData(data);
            } else {
              resultDiv.innerHTML = `<p class="error">${data.error || 'An error occurred.'}</p>`;
            }
          } catch (error) {
            resultDiv.innerHTML = '<p class="error">Failed to fetch WHOIS data. Please try again.</p>';
          } finally {
            loadingDiv.classList.remove('active');
            setTimeout(() => {
              resultDiv.classList.add('show');
            }, 100);
          }
        }

        // Trigger lookup when the user presses "Enter"
        document.getElementById('domain').addEventListener('keypress', function (event) {
          if (event.key === 'Enter') {
            fetchWhois();
          }
        });

        // Toggle between dark and light themes.
        function toggleTheme() {
          const body = document.body;
          if (body.classList.contains('dark-theme')) {
            body.classList.remove('dark-theme');
            body.classList.add('light-theme');
          } else {
            body.classList.remove('light-theme');
            body.classList.add('dark-theme');
          }
        }
      </script>
    </body>
    </html>
    ''')

@app.route("/whois/<path:domain>")
def whois_via_path(domain):
    response_data, status_code = get_whois_response(domain)
    return jsonify(response_data), status_code

@app.route("/whois")
def whois_via_query():
    domain = request.args.get('domain')
    if not domain:
        return jsonify({"error": "Domain not provided. Please use the 'domain' parameter."}), 400
    response_data, status_code = get_whois_response(domain)
    return jsonify(response_data), status_code

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

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
        return {"error": "An error occurred while fetching WHOIS data", "details": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
