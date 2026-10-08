# utils/profiles.py
from utils.custom_profiles import (
    get_custom_profile_names,
    get_custom_profile
)
PROFILES = {
    "Standard Cleaning": {
        "remove_duplicates": True,
        "remove_blank_rows": True,
        "validate_data": True,
        "format_excel": True,
        "create_summary": True,
        "create_charts": True,
        "export_csv": True,
        "generate_pdf": True,
        "create_zip": True,
    },

    "Sales Data": {
        "remove_duplicates": True,
        "remove_blank_rows": True,
        "validate_data": True,
        "format_excel": True,
        "create_summary": True,
        "create_charts": True,
        "export_csv": True,
        "generate_pdf": True,
        "create_zip": True,
    },

    "Customer Data": {
        "remove_duplicates": True,
        "remove_blank_rows": True,
        "validate_data": True,
        "format_excel": True,
        "create_summary": True,
        "create_charts": False,
        "export_csv": True,
        "generate_pdf": True,
        "create_zip": True,
    },

    "Financial Data": {
        "remove_duplicates": True,
        "remove_blank_rows": True,
        "validate_data": True,
        "format_excel": True,
        "create_summary": True,
        "create_charts": True,
        "export_csv": True,
        "generate_pdf": True,
        "create_zip": True,
    },
}


def get_profile_names():
    """Return all built-in and custom automation profile names."""

    built_in_names = list(PROFILES.keys())

    custom_names = get_custom_profile_names()

    return built_in_names + custom_names


def get_profile(name):
    """Return a copy of the selected automation profile."""

    if name in PROFILES:
        return PROFILES[name].copy()

    try:
        return get_custom_profile(name)

    except ValueError:
        raise ValueError(
            f"Unknown automation profile: {name}"
        )


def is_valid_profile(name):
    """Check whether an automation profile exists."""
    return name in PROFILES