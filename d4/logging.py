import structlog
from environs import Env


# add logging before app has booted
env = Env()
DEBUG = env.bool("DEBUG", default=False)


def timestamper(logger, log_method, event_dict):
    """
    Add timestamps to logs conditionally

    Structlog provides a Timestamper processor.  However, we only want to
    timestamp logs locally since Production stamps logs for us.  This mirrors
    how the Timestamper processor stamps events internally.
    """
    if not DEBUG:
        return event_dict

    # mirror how structlogs own Timestamper calls _make_stamper
    stamper = structlog.processors._make_stamper(fmt="iso", utc=True, key="timestamp")
    return stamper(event_dict)


pre_chain = [
    # Add the log level and a timestamp to the event_dict if the log entry
    # is not from structlog.
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    timestamper,
]

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        timestamper,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.ExceptionPrettyPrinter(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
)

logging_config_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
            "foreign_pre_chain": pre_chain,
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "formatter",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
        "gunicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django_structlog": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "jobserver": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
