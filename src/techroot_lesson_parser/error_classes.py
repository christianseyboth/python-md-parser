from dataclasses import dataclass
from enum import Enum


class ParseError(Exception):
    pass


class SeverityType(Enum):
    WARNING = "warning"
    ERROR = "error"


@dataclass
class ValidationError:
    message: str
    source: str
    severity: SeverityType
