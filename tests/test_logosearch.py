import pytest
from src.logosearch.api import get_logo_url

class TestLogoSearch:
    def test_get_logo_url_basic(self):
        """Test basic functionality of get_logo_url"""
        logo_url = get_logo_url("btc", size="medium")
        print(logo_url)
        assert isinstance(logo_url, str), "Logo URL should be a string"
        assert logo_url.startswith("http"), "Logo URL should be a valid URL"
    