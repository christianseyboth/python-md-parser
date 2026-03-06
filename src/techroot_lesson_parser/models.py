from dataclasses import dataclass, field
from enum import Enum
from pydoc import text


class StepType(Enum):
    TEXT = "text"
    TYPING = "typing"
    TERMINAL = "terminal"
    CHECKPOINT = "checkpoint"


class ValidatorType(Enum):
    EXACT = "exact"
    CONTAINS = "contains"
    REGEX = "regex"


@dataclass
class Lesson:
    id: str
    title: str
    estimated_minutes: int
    prerequisites: list[str] = field(default_factory=list)
    story: dict | None = None
    steps: list = field(default_factory=list)


@dataclass
class Step:
    type: StepType
    order: int
    content_md: str
    content_html: str = ""

    # typing steps
    target: str | None = None
    wpm_goal: int | None = None

    # terminal steps
    expected_output: str | None = None
    validator: ValidatorType = ValidatorType.EXACT


@dataclass
class Chapter:
    id: str
    title: str
    tier: int
    description: str
    lessons: list[Lesson] = field(default_factory=list)
