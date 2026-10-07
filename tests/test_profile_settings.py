from utils.profile_settings import (
    create_profile_settings,
    validate_profile_settings,
)


def test_create_sales_profile_settings():

    settings = create_profile_settings("Sales Data")

    assert settings["remove_duplicates"] is True
    assert settings["remove_blank_rows"] is True
    assert settings["validate_data"] is True
    assert settings["format_excel"] is True
    assert settings["create_summary"] is True
    assert settings["create_charts"] is True
    assert settings["export_csv"] is True
    assert settings["generate_pdf"] is True
    assert settings["create_zip"] is True


def test_customer_profile_settings():

    settings = create_profile_settings("Customer Data")

    assert settings["create_charts"] is False


def test_settings_are_independent():

    settings = create_profile_settings("Sales Data")

    settings["create_charts"] = False

    new_settings = create_profile_settings("Sales Data")

    assert new_settings["create_charts"] is True


def test_valid_settings():

    settings = create_profile_settings("Sales Data")

    assert validate_profile_settings(settings) is True


def test_missing_setting():

    settings = create_profile_settings("Sales Data")

    del settings["create_charts"]

    try:
        validate_profile_settings(settings)
        assert False
    except ValueError as error:
        assert "Missing profile setting" in str(error)


def test_invalid_setting_type():

    settings = create_profile_settings("Sales Data")

    settings["create_charts"] = "yes"

    try:
        validate_profile_settings(settings)
        assert False
    except ValueError as error:
        assert "must be True or False" in str(error)