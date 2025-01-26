import os
import tomllib
from glob import glob
from typing import Any

from mitmproxyman.dataclasses.profile import Profile

_example_toml = """
default_project = "example"

[project.example]
profiles = "~/.config/mitmproxyman/profiles/example/*.json"
"""


def _init_config() -> None:
    """Creates a new config file if one doesn't already exist"""
    config_path = _get_config_path()
    if not os.path.exists(config_path):
        os.makedirs(f"{_get_config_home()}/mitmproxyman", exist_ok=True)
        with open(config_path, "w") as f:
            f.write(_example_toml)


def _get_config_path() -> str:
    """Returns the path of the mitmproxyman.toml file

    Returns:
        path to config file
    """
    return f"{_get_config_home()}/mitmproxyman/mitmproxyman.toml"


def _get_config_home() -> str:
    """Returns the path for the system's config home

    Returns:
        path of config home
    """
    config_home = os.environ.get("XDG_CONFIG_HOME")
    if not config_home:
        config_home = os.path.expanduser("~/.config")
    return config_home


def load_project(project_conf: dict[str, Any]) -> list[Profile]:
    """Loads a project from the mitmproxyman.toml file.
    (note for now this is only loading "profiles" ... will likely
    be expanded as mitmproxyman gets more capabilities)

    Args:
        project_conf: a dictionary object representing a project in mitmproxyman.toml

    Returns:
        a list of Profile objects
    """
    profile_files = glob(os.path.expanduser(project_conf["profiles"]))
    profiles = []
    for p in profile_files:
        with open(p) as f:
            profiles.append(Profile.from_json(f.read()))
    return profiles


def get_project_configuration():
    config_path = _get_config_path()
    if os.path.exists(config_path):
        with open(config_path) as f:
            conf = tomllib.loads(f.read())
            project_name = conf["default_project"]
            project_conf = conf["project"][project_name]
            project = load_project(project_conf)
            return project

    else:
        print(f"Config not found.  Creating example config at {config_path}")
        _init_config()


profiles = get_project_configuration()
print(profiles)
