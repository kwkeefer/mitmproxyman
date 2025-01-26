import pytest

from mitmproxyman.dataclasses import Cookie


@pytest.fixture(scope="session")
def global_cookies():
    cookies_list = [
        Cookie(name="foo", value="bar", domain="example.com", path="/"),
        Cookie(
            name="dead",
            value="beef",
            secure=True,
            httponly=True,
            domain="test.example.com",
            path="/web/",
        ),
    ]

    yield cookies_list
