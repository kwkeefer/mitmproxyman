import json
from re import Pattern
from typing import Dict, List, Optional

from pydantic import Field, ValidationError
from pydantic.dataclasses import dataclass

from mitmproxyman.dataclasses.cookie import Cookie


@dataclass
class Profile:
    name: str = Field(description="name of the profile")
    cookies: List["Cookie"] = Field(description="cookies to add/modify")
    headers: Dict[str, str] = Field(
        default_factory=dict, description="headers to add/modify"
    )
    description: Optional[str] = Field(
        default=None, description="description of the profile"
    )
    scope: Optional[Pattern] = Field(
        default=None,
        description="A regex scope.  Only requests with a matching host will be modified.",
    )

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data: str) -> "Profile":
        d = json.loads(data)
        cookies = []
        for c in d.get("cookies", []):
            try:
                cookies.append(Cookie(**c))
            except ValidationError as e:
                print(f"Unable to load cookie: {c.get('name')}")
                print(e.errors())
        d["cookies"] = cookies
        return Profile(**d)
