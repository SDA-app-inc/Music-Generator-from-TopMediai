import logging
from logging import Logger

from app.core.logging.filters import RequestIdFilter

logger: Logger = logging.getLogger("MusicAI-service")

logger.addFilter(RequestIdFilter())
