import logging

from pythonjsonlogger import jsonlogger


class ErrorHandlingJSONFormatter(jsonlogger.JsonFormatter):
    def format(self, record: logging.LogRecord) -> str:
        try:
            return super().format(record)
        except Exception as exc:
            record.msg = "Logging error"
            record.args = ()
            record.levelno = logging.ERROR
            record.levelname = logging.getLevelName(logging.ERROR)
            record.exc_info = (type(exc), exc, exc.__traceback__)

            return super().format(record)
