import logging.config

LOGGER_NAME = "Dice Roll MCP Server"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)s | %(name)s - %(message)s"
        }
    },

    "handlers": {
        "stream": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        }
    },

    "loggers": {
        LOGGER_NAME: {
            "handlers": ["stream"],
            "level": "INFO",
            "propagate": False
        }
    }
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)