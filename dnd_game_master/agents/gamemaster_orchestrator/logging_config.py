import logging.config


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "%(asctime)s |%(levelname)s| %(name)s - %(message)s"
        }
    },

    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        }
    },

    "root": {
        "handlers": ["stdout"],
        "level": "WARNING",
    }
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
    logging.getLogger("strands").setLevel(logging.DEBUG)