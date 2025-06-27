from app.core.logging.formatters import ErrorHandlingJSONFormatter

JSON_LOG_FORMAT: str = """
    asctime: %(asctime)s
    filename: %(filename)s
    funcName: %(funcName)s
    levelname: %(levelname)s
    message: %(message)s
    name: %(name)s
"""
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': ErrorHandlingJSONFormatter,
            'format': JSON_LOG_FORMAT,
        }
    },
    'handlers': {
        "default": {
            "formatter": "json",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "json",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    'loggers': {
        'root': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,
        },
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "ERROR", "propagate": False},
        "tortoise": {"handlers": ["default"], "level": "ERROR", "propagate": False},
    },
}
