from enum import Enum


class Environment(str, Enum):
    LOCAL = "local"
    TESTING = "testing"
    DEVELOPMENT = "development"
    PRODUCTION = "production"

    @property
    def is_debug(self):
        return self in (self.LOCAL, self.DEVELOPMENT, self.TESTING)

    @property
    def is_testing(self):
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self in (self.DEVELOPMENT, self.PRODUCTION)
