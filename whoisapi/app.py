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
        
        .result {
          margin-top: 20px;
          padding: 15px;
          background-color: var(--result-bg);
          border: 1px solid var(--button-bg);
          border-radius: 5px;
          text-align: left;
          font-family: monospace;
          min-height: 50px;
          max-height: 400px;
          overflow-y: auto;
          opacity: 0;
          transition: opacity 0.5s ease;
        }
        
        .result.show {
          opacity: 1;
        }
        
        .error {
          color: var(--error-color);
        }
        
        pre {
          white-space: pre-wrap;
          word-wrap: break-word;
          margin: 0;
        }
        
        /* Loading spinner animation using opacity */
        .loading {
          margin-top: 20px;
          font-size: 1.5rem;
          color: var(--text-color);
          opacity: 0;
          transition: opacity 0.3s ease;
        }
        
        .loading.active {
          opacity: 1;
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

        // Fetch WHOIS data with smooth animations
        async function fetchWhois() {
          const domain = document.getElementById('domain').value.trim();
          const resultDiv = document.getElementById('result');
          const loadingDiv = document.getElementById('loading');
          
          // Clear previous results and remove the fade-in class
          resultDiv.innerHTML = '';
          resultDiv.classList.remove('show');
          
          // Show loading spinner (fade in)
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
              resultDiv.innerHTML = '<h3>WHOIS Data:</h3><pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } else {
              resultDiv.innerHTML = `<p class="error">${data.error || 'An error occurred.'}</p>`;
            }
          } catch (error) {
            resultDiv.innerHTML = '<p class="error">Failed to fetch WHOIS data. Please try again.</p>';
          } finally {
            // Hide loading spinner and fade in the result display
            loadingDiv.classList.remove('active');
            setTimeout(() => {
              resultDiv.classList.add('show');
            }, 100); // slight delay for a smoother transition
          }
        }

        // Allow pressing "Enter" to trigger the lookup
        document.getElementById('domain').addEventListener('keypress', function (event) {
          if (event.key === 'Enter') {
            fetchWhois();
          }
        });

        // Toggle between dark and light themes
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
