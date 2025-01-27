import re
from http.cookies import SimpleCookie

from mitmproxyman.dataclasses.cookie import Cookie


def create_request_header_from_cookies(
    cookies: list[Cookie], include_header_key: bool = False
) -> str:
    """Creates a cookie header string for HTTP requests

    Args:
        cookies: a list of one or more cookie objects

    Returns:
        Cookie string
    """
    if include_header_key:
        header = "Cookie: "
    else:
        header = ""

    return header + "; ".join([f"{c.name}={c.value}" for c in cookies])


def create_cookies_from_request_header(cookies_header: str) -> list[Cookie]:
    cookies_header = re.sub(r"^Cookie: ", "", cookies_header)
    s = SimpleCookie()
    s.load(cookies_header)

    cookies = []
    for k in s.keys():
        cookies.append(Cookie(name=k, value=s[k].value))
    return cookies


def merge_and_replace_cookies(
    original_cookies: list[Cookie], new_cookies: list[Cookie]
):
    new_cookies_keys = {c.name for c in new_cookies}  # Use a set for faster lookups

    original_with_matches_removed = [
        c for c in original_cookies if c.name not in new_cookies_keys
    ]

    return original_with_matches_removed + new_cookies
