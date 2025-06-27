import logging
import uuid
from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar('request_id', default=str(uuid.uuid4()))


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        if request_id.get():
            record.request_id = request_id.get()
        return True
