# utils/profile_settings.py

from utils.profiles import get_profile


def create_profile_settings(profile_name):
    """
    Create a mutable settings dictionary
    from an existing automation profile.
    """

    profile = get_profile(profile_name)

    return {
        "remove_duplicates": profile["remove_duplicates"],
        "remove_blank_rows": profile["remove_blank_rows"],
        "validate_data": profile["validate_data"],
        "format_excel": profile["format_excel"],
        "create_summary": profile["create_summary"],
        "create_charts": profile["create_charts"],
        "export_csv": profile["export_csv"],
        "generate_pdf": profile["generate_pdf"],
        "create_zip": profile["create_zip"],
    }


def validate_profile_settings(settings):
    """
    Validate that all required automation settings exist
    and contain boolean values.
    """

    required_settings = [
        "remove_duplicates",
        "remove_blank_rows",
        "validate_data",
        "format_excel",
        "create_summary",
        "create_charts",
        "export_csv",
        "generate_pdf",
        "create_zip",
    ]

    for setting in required_settings:

        if setting not in settings:
            raise ValueError(
                f"Missing profile setting: {setting}"
            )

        if not isinstance(settings[setting], bool):
            raise ValueError(
                f"Profile setting must be True or False: {setting}"
            )

    return True