# WhoIs API

[![Tests](https://github.com/TheBiemGamer/WhoIsApi/actions/workflows/test.yml/badge.svg)](https://github.com/TheBiemGamer/WhoIsApi/actions/workflows/test.yml)

<img src="/assets/WhoIs.png" alt="WhoIs API" width="500">

This is a simple WHOIS lookup API built with Flask, allowing users to query domain WHOIS data. The API uses the [python-whois](https://pypi.org/project/python-whois/) module to retrieve WHOIS information.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FTheBiemGamer%2FWhoIsApi)

### Features:
- A web interface to enter a domain name and use the API.
- Dark and light themes in the UI.
- The API endpoint is `/whois?domain=<domain>` (alias `/whois/<domain>`).
- Rate limiting copy the `.env.example` to `.env` for enabling and disabling (enabled by default).

---

## Setup Instructions

Follow these steps to get the project running locally.

### Prerequisites
- [Docker](https://www.docker.com/) (for containerized)
- [Python 3.9+](https://www.python.org/) (for local)

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

Then visit `http://localhost:5000`.

### 3. Running Locally

To run the app locally, install the dependencies:

```bash
pip install -r requirements.txt
```

Then run the app either with flask:

```bash
cd whoisapi
flask run
```

Or with something more production ready like waitress:

```bash
waitress-serve whoisapi.app:app
```

Then visit `http://localhost:5000`.

---

## API Endpoint

**GET** `/whois/<domain>` or `/whois?domain=<domain>`

- `domain`: The domain name (e.g., `example.com`).

Example response (for `example.com`):

```json
{
  "address": null,
  "city": null,
  "country": null,
  "creation_date": "1995-08-14T04:00:00",
  "dnssec": "signedDelegation",
  "domain_name": "EXAMPLE.COM",
  "emails": null,
  "expiration_date": "2025-08-13T04:00:00",
  "name": null,
  "name_servers": [
    "A.IANA-SERVERS.NET",
    "B.IANA-SERVERS.NET"
  ],
  "org": null,
  "referral_url": null,
  "registrant_postal_code": null,
  "registrar": "RESERVED-Internet Assigned Numbers Authority",
  "registrar_url": "http://res-dom.iana.org",
  "reseller": null,
  "state": null,
  "status": [
    "clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited",
    "clientTransferProhibited https://icann.org/epp#clientTransferProhibited",
    "clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited"
  ],
  "updated_date": "2024-08-14T07:01:34",
  "whois_server": "whois.iana.org"
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

- [python-whois](https://pypi.org/project/python-whois/) - A Python package that interacts with WHOIS servers and fetches domain registration information.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

If you'd like to contribute to this project, feel free to fork it and create a pull request. Any improvements or suggestions are welcome!

---

## Author

- [TheBiemGamer](https://github.com/TheBiemGamer)
