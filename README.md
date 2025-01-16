# WHOIS Lookup API

This is a simple WHOIS lookup API built with Flask, allowing users to query domain WHOIS data. The API uses the [python-whois](https://pypi.org/project/python-whois/) module to retrieve WHOIS information.

### Features:
- A basic web interface to enter a domain name and fetch its WHOIS data.
- Support for dark and light themes.
- Handles invalid or missing WHOIS data with appropriate error messages.
- The API endpoint is `/whois/<domain>` for retrieving WHOIS data for a given domain.

---

## Setup Instructions

Follow these steps to get the project running locally.

### Prerequisites
- [Docker](https://www.docker.com/) (for containerized setup)
- [Python 3.9+](https://www.python.org/) (for local setup)

### 1. Clone the repository

```bash
git clone https://github.com/TheBiemGamer/WhoIsApi.git
cd WhoIsApi
```

### 2. Docker Setup (Optional)

To build and run the project in a Docker container, follow these steps:

```bash
docker build -t whois-api .
docker run -p 5000:5000 whois-api
```

Visit `http://localhost:5000` to access the WHOIS lookup interface.

### 3. Running Locally

To run the app locally, install the dependencies:

```bash
pip install -r requirements.txt
```

Then run the app:

```bash
cd whoisapi
flask run
```

Visit `http://localhost:5000` to access the WHOIS lookup interface.

---

## API Endpoint

**GET** `/whois/<domain>`

- `domain`: The domain name (e.g., `example.com`) whose WHOIS data is to be fetched.

Example response:

```json
{
  "domain_name": "example.com",
  "registrar": "Registrar Name",
  "creation_date": "2020-01-01T00:00:00",
  "expiration_date": "2025-01-01T00:00:00",
  "updated_date": "2021-01-01T00:00:00",
  "name_servers": ["ns1.example.com", "ns2.example.com"]
}
```

Error response (Invalid domain):

```json
{
  "error": "Invalid domain name"
}
```

Error response (No WHOIS data found):

```json
{
  "error": "No WHOIS data found for example.com"
}
```

---

## Credits

This project relies on the **[python-whois](https://pypi.org/project/python-whois/)** library for retrieving WHOIS data. The library is a Python wrapper for querying WHOIS information from a domain.

- [Python-Whois Library](https://pypi.org/project/python-whois/) - A Python package that interacts with WHOIS servers and fetches domain registration information.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

If you'd like to contribute to this project, feel free to fork it and create a pull request. Any improvements or suggestions are welcome!

---

## Author

- [TheBiemGamer](https://github.com/TheBiemGamer)