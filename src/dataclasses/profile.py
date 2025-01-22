from pydantic import Field
from pydantic.dataclasses import dataclass

from re import Pattern
from typing import Dict, Optional


@dataclass
class Profile:
    name: str = Field(description="name of the profile")
    cookies: Dict[str, str] = Field(
        default_factory=dict, description="cookies to add/modify"
    )
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
