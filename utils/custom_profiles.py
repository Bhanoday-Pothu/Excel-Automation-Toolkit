# utils/custom_profiles.py

import json
from pathlib import Path


CUSTOM_PROFILES_FILE = Path("config") / "profiles.json"


def load_custom_profiles():
    """
    Load custom automation profiles from disk.
    """

    if not CUSTOM_PROFILES_FILE.exists():
        return {}

    try:
        with open(
            CUSTOM_PROFILES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, dict):
            return {}

        return data

    except (json.JSONDecodeError, OSError):
        return {}


def save_custom_profile(name, settings):
    """
    Save or update a custom automation profile.
    """

    name = name.strip()

    if not name:
        raise ValueError(
            "Profile name cannot be empty."
        )

    if not isinstance(settings, dict):
        raise ValueError(
            "Profile settings must be a dictionary."
        )

    profiles = load_custom_profiles()

    profiles[name] = settings.copy()

    CUSTOM_PROFILES_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        CUSTOM_PROFILES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            profiles,
            file,
            indent=4
        )


def delete_custom_profile(name):
    """
    Delete a custom automation profile.
    """

    profiles = load_custom_profiles()

    if name not in profiles:
        raise ValueError(
            f"Custom profile not found: {name}"
        )

    del profiles[name]

    CUSTOM_PROFILES_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        CUSTOM_PROFILES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            profiles,
            file,
            indent=4
        )


def get_custom_profile(name):
    """
    Return one custom profile.
    """

    profiles = load_custom_profiles()

    if name not in profiles:
        raise ValueError(
            f"Custom profile not found: {name}"
        )

    return profiles[name].copy()


def get_custom_profile_names():
    """
    Return all custom profile names.
    """

    return list(
        load_custom_profiles().keys()
    )