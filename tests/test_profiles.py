from utils.profiles import (
    get_profile_names,
    get_profile,
    is_valid_profile,
)


def test_get_profile_names():
    names = get_profile_names()

    assert "Standard Cleaning" in names
    assert "Sales Data" in names
    assert "Customer Data" in names
    assert "Financial Data" in names


def test_get_sales_profile():
    profile = get_profile("Sales Data")

    assert profile["remove_duplicates"] is True
    assert profile["remove_blank_rows"] is True
    assert profile["validate_data"] is True
    assert profile["format_excel"] is True
    assert profile["create_summary"] is True
    assert profile["create_charts"] is True
    assert profile["export_csv"] is True
    assert profile["generate_pdf"] is True
    assert profile["create_zip"] is True


def test_customer_profile_disables_charts():
    profile = get_profile("Customer Data")

    assert profile["create_charts"] is False


def test_valid_profile():
    assert is_valid_profile("Sales Data") is True
    assert is_valid_profile("Customer Data") is True


def test_invalid_profile():
    assert is_valid_profile("Unknown Profile") is False


def test_unknown_profile_raises_error():
    try:
        get_profile("Unknown Profile")
        assert False
    except ValueError as error:
        assert "Unknown automation profile" in str(error)


def test_get_profile_returns_copy():
    profile = get_profile("Sales Data")

    profile["remove_duplicates"] = False

    original_profile = get_profile("Sales Data")

    assert original_profile["remove_duplicates"] is True