import json

import utils.custom_profiles as custom_profiles


def test_load_custom_profiles_when_file_missing(tmp_path, monkeypatch):

    profile_file = tmp_path / "profiles.json"

    monkeypatch.setattr(
        custom_profiles,
        "CUSTOM_PROFILES_FILE",
        profile_file
    )

    assert custom_profiles.load_custom_profiles() == {}


def test_save_and_load_custom_profile(tmp_path, monkeypatch):

    profile_file = tmp_path / "profiles.json"

    monkeypatch.setattr(
        custom_profiles,
        "CUSTOM_PROFILES_FILE",
        profile_file
    )

    settings = {
        "remove_duplicates": True,
        "remove_blank_rows": False,
        "validate_data": True,
        "format_excel": True,
        "create_summary": True,
        "create_charts": False,
        "export_csv": True,
        "generate_pdf": True,
        "create_zip": False,
    }

    custom_profiles.save_custom_profile(
        "My Sales Report",
        settings
    )

    loaded = custom_profiles.load_custom_profiles()

    assert "My Sales Report" in loaded
    assert loaded["My Sales Report"] == settings


def test_get_custom_profile(tmp_path, monkeypatch):

    profile_file = tmp_path / "profiles.json"

    monkeypatch.setattr(
        custom_profiles,
        "CUSTOM_PROFILES_FILE",
        profile_file
    )

    settings = {
        "create_charts": False
    }

    custom_profiles.save_custom_profile(
        "Test Profile",
        settings
    )

    result = custom_profiles.get_custom_profile(
        "Test Profile"
    )

    assert result == settings


def test_get_custom_profile_names(tmp_path, monkeypatch):

    profile_file = tmp_path / "profiles.json"

    monkeypatch.setattr(
        custom_profiles,
        "CUSTOM_PROFILES_FILE",
        profile_file
    )

    custom_profiles.save_custom_profile(
        "Profile A",
        {"create_charts": True}
    )

    custom_profiles.save_custom_profile(
        "Profile B",
        {"create_charts": False}
    )

    names = custom_profiles.get_custom_profile_names()

    assert "Profile A" in names
    assert "Profile B" in names


def test_update_existing_custom_profile(tmp_path, monkeypatch):

    profile_file = tmp_path / "profiles.json"

    monkeypatch.setattr(
        custom_profiles,
        "CUSTOM_PROFILES_FILE",
        profile_file
    )

    custom_profiles.save_custom_profile(
        "My Profile",
        {"create_charts": True}
    )

    custom_profiles.save_custom_profile(
        "My Profile",
        {"create_charts": False}
    )

    result = custom_profiles.get_custom_profile(
        "My Profile"
    )

    assert result["create_charts"] is False


def test_delete_custom_profile(tmp_path, monkeypatch):

    profile_file = tmp_path / "profiles.json"

    monkeypatch.setattr(
        custom_profiles,
        "CUSTOM_PROFILES_FILE",
        profile_file
    )

    custom_profiles.save_custom_profile(
        "Delete Me",
        {"create_charts": True}
    )

    custom_profiles.delete_custom_profile(
        "Delete Me"
    )

    assert custom_profiles.load_custom_profiles() == {}


def test_invalid_custom_profile_name(tmp_path, monkeypatch):

    profile_file = tmp_path / "profiles.json"

    monkeypatch.setattr(
        custom_profiles,
        "CUSTOM_PROFILES_FILE",
        profile_file
    )

    try:
        custom_profiles.save_custom_profile(
            "",
            {"create_charts": True}
        )

        assert False

    except ValueError as error:

        assert "cannot be empty" in str(error)