"""Logging configuration helpers."""

from __future__ import annotations

import logging
from logging.config import dictConfig

from langchain_rag.config import Settings, get_settings

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def configure_logging(settings: Settings | None = None) -> None:
    """Configure root logging based on application settings.

    Args:
        settings: Optional settings instance. When omitted the cached
            :func:`get_settings` value is used.
    """
    settings = settings or get_settings()
    level = settings.log_level.upper()

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {"format": _LOG_FORMAT},
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": level,
                },
            },
            "root": {
                "handlers": ["console"],
                "level": level,
            },
        }
    )


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger."""
    return logging.getLogger(name)
