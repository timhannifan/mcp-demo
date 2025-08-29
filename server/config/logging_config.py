"""Centralized logging configuration for the application."""

import logging
import sys


def setup_logging(
    level: str | int = "INFO",
    format_string: str | None = None,
) -> None:
    """Set up logging configuration for the entire application.

    Args:
        level: Logging level as string or integer (default: "INFO")
        format_string: Custom format string (optional)
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Convert string level to integer if needed
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    # Remove any existing handlers to avoid duplicates
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configure basic logging
    logging.basicConfig(
        level=level, format=format_string, handlers=[logging.StreamHandler(sys.stdout)]
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name.

    Args:
        name: Usually __name__ of the calling module

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


# Initialize logging when module is imported
setup_logging()
