"""
Shadow Cut Structured Observability & Logging Configuration.
Sets up structlog with JSON output in production and colored console in development.
"""

import sys
import logging
import structlog


def configure_logging(environment: str = "production", log_level: str = "INFO") -> None:
    """Configure structlog processors and standard library redirection."""
    level = getattr(logging, log_level.upper(), logging.INFO)

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if environment.lower() == "development":
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True)
        ]
    else:
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer()
        ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Return a configured structlog logger instance."""
    return structlog.get_logger(name)
