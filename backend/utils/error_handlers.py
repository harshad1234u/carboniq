"""
CarbonIQ Error Handling.

Defines a custom exception hierarchy and FastAPI exception handlers that
return consistent, user-safe JSON error responses.  Internal details are
logged but never leaked to the client.
"""

from __future__ import annotations

import logging
import traceback
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

logger = logging.getLogger("carboniq.errors")


# ---------------------------------------------------------------------------
# Custom exception hierarchy
# ---------------------------------------------------------------------------


class CarbonIQError(Exception):
    """Base exception for all CarbonIQ application errors."""

    def __init__(
        self,
        message: str = "An application error occurred.",
        status_code: int = 400,
        detail: dict[str, Any] | None = None,
    ) -> None:
        """Docstring."""
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}


class NotFoundError(CarbonIQError):
    """ """

    def __init__(self, resource: str = "Resource") -> None:
        """Docstring."""
        super().__init__(
            message=f"{resource} not found.",
            status_code=404,
        )


class AuthenticationError(CarbonIQError):
    """ """

    def __init__(self, message: str = "Authentication failed.") -> None:
        """Docstring."""
        super().__init__(message=message, status_code=401)


class ForbiddenError(CarbonIQError):
    """ """

    def __init__(self, message: str = "Access denied.") -> None:
        """Docstring."""
        super().__init__(message=message, status_code=403)


# ---------------------------------------------------------------------------
# FastAPI exception handlers
# ---------------------------------------------------------------------------


async def _carboniq_error_handler(
    request: Request,
    exc: CarbonIQError,
) -> JSONResponse:
    """Handle ``CarbonIQError`` and its subclasses."""
    logger.warning("CarbonIQError: %s | path=%s", exc.message, request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "detail": exc.detail},
    )


async def _validation_error_handler(
    request: Request,
    exc: ValidationError,
) -> JSONResponse:
    """Handle Pydantic ``ValidationError`` – return 400 with field details."""
    errors = []
    for err in exc.errors():
        errors.append(
            {
                "field": " -> ".join(str(loc) for loc in err.get("loc", [])),
                "message": err.get("msg", "Invalid value"),
                "type": err.get("type", "value_error"),
            }
        )
    logger.warning("ValidationError: %s | path=%s", errors, request.url.path)
    return JSONResponse(
        status_code=400,
        content={"error": "Validation failed.", "details": errors},
    )


async def _value_error_handler(
    request: Request,
    exc: ValueError,
) -> JSONResponse:
    """Handle plain ``ValueError`` – return 400 with the message."""
    logger.warning("ValueError: %s | path=%s", exc, request.url.path)
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)},
    )


async def _generic_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle any uncaught exception – log full traceback, return safe 500."""
    logger.error(
        "Unhandled exception on %s: %s\n%s",
        request.url.path,
        exc,
        traceback.format_exc(),
    )
    return JSONResponse(
        status_code=500,
        content={"error": "An internal server error occurred. Please try again later."},
    )


# ---------------------------------------------------------------------------
# Registration helper
# ---------------------------------------------------------------------------


def register_error_handlers(app: FastAPI) -> None:
    """Attach all CarbonIQ exception handlers to *app*.

    Args:
      app: The FastAPI application instance.
      app: FastAPI: 

    Returns:

    """
    app.add_exception_handler(CarbonIQError, _carboniq_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ValidationError, _validation_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ValueError, _value_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, _generic_error_handler)  # type: ignore[arg-type]
