import json
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
    expires: Optional[int] = None  # Typically a timestamp
    max_age: Optional[int] = None  # Typically in seconds
    secure: Optional[bool] = False
    httponly: Optional[bool] = False
    samesite: Optional[str] = None  # 'Strict', 'Lax', or 'None'
    priority: Optional[str] = None  # Non-standard: 'Low', 'Medium', 'High'

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data: str) -> "Cookie":
        return Cookie(**json.loads(data))
