import json
from re import Pattern
from typing import TYPE_CHECKING, Dict, List, Optional

from pydantic import Field
from pydantic.dataclasses import dataclass

if TYPE_CHECKING:
    from .cookie import Cookie


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
        return Profile(**json.loads(data))
