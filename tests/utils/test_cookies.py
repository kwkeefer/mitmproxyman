from mitmproxyman.dataclasses import Cookie
from mitmproxyman.utils.cookies import (build_request_cookie_header,
                                        build_response_cookie_header)


def test_build_response_cookie_header(global_cookies: list[Cookie]):
    cookie_header = build_response_cookie_header(global_cookies[0])
    print(cookie_header)
    assert isinstance(cookie_header, str)


def test_build_response_cookie_header_include_header(global_cookies: list[Cookie]):
    cookie_header = build_response_cookie_header(
        global_cookies[0], include_header_key=True
    )

    assert cookie_header.startswith("Set-Cookie: ")

    cookie_header = build_response_cookie_header(
        global_cookies[0], include_header_key=False
    )

    assert not cookie_header.startswith("Set-Cookie: ")


def test_build_request_cookie_header(global_cookies: list[Cookie]):
    cookie_header = build_request_cookie_header(global_cookies)
    print(cookie_header)

    assert isinstance(cookie_header, str)


def test_build_request_cookie_header_include_header(global_cookies: list[Cookie]):
    cookie_header = build_request_cookie_header(global_cookies, include_header_key=True)

    assert cookie_header.startswith("Cookie: ")

    cookie_header = build_request_cookie_header(
        global_cookies, include_header_key=False
    )

    assert not cookie_header.startswith("Cookie: ")
