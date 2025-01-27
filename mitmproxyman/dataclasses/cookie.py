import json
import re
from http.cookies import SimpleCookie
from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class Cookie:
    """Represents commonly used Cookie attributes as defined in
    https://datatracker.ietf.org/doc/html/rfc2109
    """

    name: str
    value: str
    domain: Optional[str] = None
    path: Optional[str] = None
    expires: Optional[str] = None  # Typically a timestamp
    max_age: Optional[int] = None  # Typically in seconds
    secure: Optional[bool] = False
    httponly: Optional[bool] = False
    samesite: Optional[str] = None  # 'Strict', 'Lax', or 'None'
    priority: Optional[str] = None  # Non-standard: 'Low', 'Medium', 'High'

    @property
    def simple_cookie(self) -> SimpleCookie:
        simple_cookie = SimpleCookie()
        simple_cookie[self.name] = self.value

        if self.domain is not None:
            simple_cookie[self.name]["domain"] = self.domain
        if self.path is not None:
            simple_cookie[self.name]["path"] = self.path
        if self.expires is not None:
            simple_cookie[self.name]["expires"] = self.expires
        if self.max_age is not None:
            simple_cookie[self.name]["max-age"] = self.max_age
        if self.secure:
            simple_cookie[self.name]["secure"] = True
        if self.httponly:
            simple_cookie[self.name]["httponly"] = True
        if self.samesite is not None:
            simple_cookie[self.name]["samesite"] = self.samesite

        return simple_cookie

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data: str) -> "Cookie":
        return Cookie(**json.loads(data))

    @staticmethod
    def from_request_header():
        # not implementing in this class because this class represents one cookie, whereas a Cookie: header can contain many
        raise NotImplementedError(
            "Use utils.cookies.create_cookies_from_request_header() instead"
        )

    @staticmethod
    def from_response_header(cookie_header: str) -> "Cookie":
        cookie_header = re.sub(r"^Set-Cookie: ", "", cookie_header)
        s = SimpleCookie()
        s.load(cookie_header)

        # todo: figure out a better way to do this
        key = list(s.keys())[0]

        # logic to ignore uncomon header attributes
        uncommon_header_attributes = ["version", "comment"]
        additional_attributes = dict()
        attr_keys = list(s[key].keys())
        attr_values = list(s[key].values())
        for i in range(len(attr_keys)):
            attr_key = attr_keys[i]

            # default value is '' which is a string and doesn't match our Cookie class typing
            if attr_key not in uncommon_header_attributes:
                if attr_values[i] == "":
                    attr_value = None
                else:
                    attr_value = attr_values[i]
                # trying to match http.cookie.Morsel attr to our Cookie attr
                if attr_keys[i] == "max-age":
                    attr_key = "max_age"
                    attr_value = int(attr_values[i])

                additional_attributes[attr_key] = attr_value
        return Cookie(name=key, value=s[key].value, **additional_attributes)

    def response_header(self, include_header_key: bool = False) -> str:
        """Creates a header string that can be used to set cookies in an HTTP response

        Args:
            include_header_key: if true "Set-Cookie:" will be added to the returned string

        Returns:
            cookie string
        """
        if include_header_key:
            header = "Set-Cookie:"
        else:
            header = ""

        return self.simple_cookie.output(header=header, sep=";").strip()

    def request_header(self, include_header_key: bool = False) -> str:
        if include_header_key:
            header = "Cookie: "
        else:
            header = ""

        return self.simple_cookie.output(header=header, attrs=[])
