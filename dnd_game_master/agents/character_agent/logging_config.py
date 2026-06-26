import logging.config

LOGGER_NAME = "Character A2A Server"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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

    "root": {
        "handlers": ["stream"],
        "level": "INFO",
    }
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)