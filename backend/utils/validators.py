"""
CarbonIQ Input Validation Utilities.

Provides reusable validation and sanitisation helpers used by Pydantic models,
service functions, and API routes.  All functions raise ``ValueError`` with a
descriptive message when validation fails.
"""

from __future__ import annotations

import html
import re
from typing import Sequence

# ---------------------------------------------------------------------------
# Numeric validation
# ---------------------------------------------------------------------------


def validate_positive_number(
    value: float | int,
    field_name: str,
    cap: float = 10_000.0,
) -> float:
    """Ensure *value* is a non-negative number, clamping if necessary.
    
    * Negative values are clamped to ``0``.
    * Values exceeding *cap* are clamped to *cap*.

    Args:
      value: The numeric value to validate.
      field_name: Human-readable field name (used in messages).
      cap: Upper bound; defaults to ``10 000``.
      value: float | int: 
      field_name: str: 
      cap: float:  (Default value = 10_000.0)

    Returns:
      : The validated (and possibly clamped) float value.

    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a number, got {type(value).__name__}.")

    if value < 0:
        value = 0.0
    if value > cap:
        value = cap

    return value


# ---------------------------------------------------------------------------
# Enum / choice validation
# ---------------------------------------------------------------------------


def validate_string_enum(
    value: str,
    allowed_values: Sequence[str],
    field_name: str,
) -> str:
    """Validate that *value* is one of *allowed_values* (case-insensitive).

    Args:
      value: The string to validate.
      allowed_values: Accepted values.
      field_name: Human-readable field name.
      value: str: 
      allowed_values: Sequence[str]: 
      field_name: str: 

    Returns:
      : The value in its canonical (lower-case) form.

    Raises:
      ValueError: If *value* is not in the allowed set.

    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")

    normalised = value.strip().lower()
    allowed_lower = [v.lower() for v in allowed_values]

    if normalised not in allowed_lower:
        raise ValueError(
            f"Invalid {field_name}: '{value}'. "
            f"Must be one of: {', '.join(allowed_values)}."
        )
    return normalised


# ---------------------------------------------------------------------------
# Email validation
# ---------------------------------------------------------------------------

_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def validate_email(email: str) -> str:
    """Validate a basic email format.

    Args:
      email: The email string to check.
      email: str: 

    Returns:
      : The email in lower-case, stripped of whitespace.

    Raises:
      ValueError: If the email does not match a basic pattern.

    """
    if not isinstance(email, str) or not email.strip():
        raise ValueError("Email must be a non-empty string.")

    cleaned = email.strip().lower()

    if not _EMAIL_RE.match(cleaned):
        raise ValueError(f"Invalid email format: '{email}'.")

    return cleaned


# ---------------------------------------------------------------------------
# String sanitisation
# ---------------------------------------------------------------------------

_HTML_TAG_RE = re.compile(r"<[^>]+>")
_SCRIPT_RE = re.compile(r"<script[\s\S]*?>[\s\S]*?</script>", re.IGNORECASE)


def sanitize_string(text: str, max_length: int = 5_000) -> str:
    """Strip HTML/script tags and escape remaining entities.

    Args:
      text: Raw user input.
      max_length: Maximum allowed length after sanitisation.
      text: str: 
      max_length: int:  (Default value = 5_000)

    Returns:
      : A safe, plain-text string.

    Raises:
      ValueError: If *text* is not a string.

    """
    if not isinstance(text, str):
        raise ValueError("Expected a string value for sanitisation.")

    # 1. Remove <script>…</script> blocks entirely
    cleaned = _SCRIPT_RE.sub("", text)

    # 2. Remove any remaining HTML tags
    cleaned = _HTML_TAG_RE.sub("", cleaned)

    # 3. Escape residual HTML entities
    cleaned = html.unescape(cleaned)

    # 4. Trim leading/trailing whitespace
    cleaned = cleaned.strip()

    # 5. Enforce max length
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]

    return cleaned
