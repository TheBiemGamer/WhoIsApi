# WhoIs API

[![Tests](https://github.com/TheBiemGamer/WhoIsApi/actions/workflows/test.yml/badge.svg)](https://github.com/TheBiemGamer/WhoIsApi/actions/workflows/test.yml)  
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FTheBiemGamer%2FWhoIsApi)

<img src="/assets/WhoIs.png" alt="WhoIs API" width="500">

A simple WHOIS lookup API built with Flask that allows users to query domain registration data. It uses the [python-whois](https://pypi.org/project/python-whois/) module to retrieve WHOIS information.

---

## Features

- **Web Interface:** Easily enter a domain name to use the API.
- **Theming:** Enjoy both dark and light themes in the UI.
- **Endpoints:**  
  - `/whois?domain=<domain>`
  - `/whois/<domain>`
- **Rate Limiting:** Enabled by default. To edit, copy `.env.example` to `.env` and adjust the setting.

---

## Table of Contents

- [Installation via Docker (Online)](#installation-via-docker-online)
- [Local Setup Instructions](#local-setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#1-clone-the-repository)
  - [Docker Setup (Build Locally)](#2-docker-setup-build-locally)
  - [Running Locally Without Docker](#3-running-locally-without-docker)
- [API Endpoint](#api-endpoint)
- [Credits](#credits)
- [License](#license)
- [Contributing](#contributing)
- [Author](#author)

---

## Installation via Docker (Online)

You can run the pre-built Docker image from GitHub's Container Registry without needing to clone the repository:

```bash
docker run -p 5000:5000 ghcr.io/thebiemgamer/whoisapi:latest
```

After running the container, visit [http://localhost:5000](http://localhost:5000) to access the API.

---

## Local Setup Instructions

### Prerequisites

- [Docker](https://www.docker.com/) *(optional — for containerized deployment)*
- [Python 3.9+](https://www.python.org/) *(for local development)*

### 1. Clone the Repository

For local development, clone the repository:

```bash
git clone https://github.com/TheBiemGamer/WhoIsApi.git
cd WhoIsApi
```

### 2. Docker Setup (Build Locally)

If you prefer to build your own Docker image:

```bash
docker build -t whois-api .
docker run -p 5000:5000 whois-api
```

Visit [http://localhost:5000](http://localhost:5000) after the container starts.

### 3. Running Locally Without Docker

If you'd like to run the app directly on your machine:

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Application**

   - **Using Flask's Development Server:**

    ```bash
    cd whoisapi
    flask run
    ```

   - **Using Gunicorn for a Production-like Environment:**

    ```bash
    gunicorn -w 4 -b 0.0.0.0:5000 whoisapi.app:app
    ```

Then, open your browser at [http://localhost:5000](http://localhost:5000).

---

## API Endpoint

### GET `/whois/<domain>` or `/whois?domain=<domain>`

Query WHOIS data for a specified domain.

#### Parameters

- **domain**: The domain name to look up (e.g., `example.com`).

#### Example Request

```
GET /whois/example.com
```

or

```
GET /whois?domain=example.com
```

#### Example Response

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

#### Error Responses

- **Invalid Domain Name:**

  ```json
  {
    "error": "Invalid domain name"
  }
  ```

- **No WHOIS Data Found:**

  ```json
  {
    "error": "No WHOIS data found for example.com"
  }
  ```

---

## Credits

This project uses the [python-whois](https://pypi.org/project/python-whois/) library to fetch WHOIS information.  
- **python-whois:** A Python wrapper for querying WHOIS servers and retrieving domain registration data.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Contributing

Contributions are welcome! If you’d like to contribute, please fork the repository and submit a pull request with your improvements or suggestions.

---

## Author

- [TheBiemGamer](https://github.com/TheBiemGamer)

---