import json
import yaml
from src.dataclasses.profile import Profile


def load_profile_from_json(file_path: str) -> Profile:
    with open(file_path, "r") as file:
        data = json.load(file)
    return Profile(**data)


def load_profile_from_yaml(file_path: str) -> Profile:
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return Profile(**data)


def load_profile(file_path: str) -> Profile:
    if file_path.endswith(".json"):
        return load_profile_from_json(file_path)
    elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
        return load_profile_from_yaml(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
