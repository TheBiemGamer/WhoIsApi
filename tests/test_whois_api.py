import pytest
from whoisapi.app import app, limiter
from unittest.mock import patch

@pytest.fixture
def client():
    app.config["TESTING"] = True
    limiter.enabled = False
    with app.test_client() as client:
        yield client

@pytest.fixture
def client_rate_limit():
    app.config["TESTING"] = True
    limiter.enabled = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test if homepage loads successfully."""
    response = client.get("/")
    assert response.status_code == 200

def test_valid_domain(client):
    """Test WHOIS lookup with a valid domain."""
    with patch("whois.whois") as mock_whois:
        mock_whois.return_value = {"domain_name": "example.com"}
        response = client.get("/whois?domain=example.com")
        assert response.status_code == 200
        assert response.json["domain_name"] == "example.com"

def test_invalid_domain(client):
    """Test WHOIS lookup with an invalid domain.
    
    Expecting a 400 error due to domain validation.
    """
    response = client.get("/whois?domain=invalid_domain")
    assert response.status_code == 400
    assert "error" in response.json

def test_missing_domain(client):
    """Test WHOIS lookup without providing a domain."""
    response = client.get("/whois")
    assert response.status_code == 400
    assert response.json["error"] == "Domain not provided. Please use the 'domain' parameter."

def test_no_whois_data(client):
    """Test WHOIS lookup when no data is found."""
    with patch("whois.whois") as mock_whois:
        mock_whois.return_value = {}
        response = client.get("/whois?domain=unknown.com")
        assert response.status_code == 404
        assert response.json["error"] == "No WHOIS data found for unknown.com"

def test_rate_limit(client_rate_limit):
    """Test rate limit enforcement."""
    with patch("whois.whois") as mock_whois:
        mock_whois.return_value = {"domain_name": "example.com"}
        
        response = client_rate_limit.get("/whois?domain=example.com")
        assert response.status_code == 200
        
        response = client_rate_limit.get("/whois?domain=example.com")
        assert response.status_code == 429
        assert response.json["error"] == "Rate limit exceeded"

if __name__ == "__main__":
    pytest.main()