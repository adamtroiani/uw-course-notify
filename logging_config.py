from logging.config import dictConfig

LOGGING_CFG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)-8s - %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": str(".debug/server.txt"),
            "mode": "a",
            "encoding": "utf-8",
        }
    },
    "root": { 
        "level": "INFO",
        "handlers": ["file"],
    },
}

def init_logging() -> None:
    dictConfig(LOGGING_CFG)
