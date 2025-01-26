from http.cookies import SimpleCookie

from mitmproxyman.dataclasses import Cookie


def build_response_cookie_header(
    cookie: Cookie, include_header_key: bool = False
) -> str:
    """Creates a header string that can be used to set cookies in an HTTP response

    Args:
        cookie: Cookie object
        include_header_key: if true "Set-Cookie:" will be added to the returned string

    Returns:
        cookie string
    """
    simple_cookie = SimpleCookie()
    simple_cookie[cookie.name] = cookie.value

    if cookie.domain is not None:
        simple_cookie[cookie.name]["domain"] = cookie.domain
    if cookie.path is not None:
        simple_cookie[cookie.name]["path"] = cookie.path
    if cookie.expires is not None:
        simple_cookie[cookie.name]["expires"] = cookie.expires
    if cookie.max_age is not None:
        simple_cookie[cookie.name]["max-age"] = cookie.max_age
    if cookie.secure:
        simple_cookie[cookie.name]["secure"] = True
    if cookie.httponly:
        simple_cookie[cookie.name]["httponly"] = True
    if cookie.samesite is not None:
        simple_cookie[cookie.name]["samesite"] = cookie.samesite

    if include_header_key:
        header = "Set-Cookie:"
    else:
        header = ""

    return simple_cookie.output(header=header, sep=";").strip()


def build_request_cookie_header(
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
