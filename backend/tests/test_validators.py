import pytest
from utils.validators import validate_positive_number, validate_string_enum, validate_email, sanitize_string

def test_validate_positive_number_valid():
    assert validate_positive_number(10, "test") == 10

def test_validate_positive_number_negative():
    assert validate_positive_number(-5, "test") == 0

def test_validate_positive_number_zero():
    assert validate_positive_number(0, "test") == 0

def test_validate_positive_number_huge():
    assert validate_positive_number(15000, "test") == 10000

def test_validate_string_enum_valid():
    assert validate_string_enum("car", ["car", "bus"], "test") == "car"

def test_validate_string_enum_invalid():
    with pytest.raises(ValueError):
        validate_string_enum("train", ["car", "bus"], "test")

def test_validate_email_valid():
    assert validate_email("test@example.com") == "test@example.com"

def test_validate_email_invalid():
    with pytest.raises(ValueError):
        validate_email("invalid-email")

def test_sanitize_string_html():
    assert sanitize_string("<b>Hello</b>") == "Hello"

def test_sanitize_string_script_tags():
    assert sanitize_string("<script>alert('xss')</script>Hi") == "Hi"

def test_sanitize_string_clean():
    assert sanitize_string("Hello World") == "Hello World"
