from dataclasses import dataclass, field
from enum import Enum

"""Core dataclasses and enums representing lessons, steps, chapters and manifest."""


class StepType(Enum):
    TEXT = "text"
    TYPING = "typing"
    TERMINAL = "terminal"
    CHECKPOINT = "checkpoint"


class ValidatorType(Enum):
    EXACT = "exact"
    CONTAINS = "contains"
    REGEX = "regex"


# Parser Dataclasses
@dataclass
class Lesson:
    """Single lesson as parsed from a markdown file."""

    id: str
    title: str
    estimated_minutes: int
    prerequisites: list[str] = field(default_factory=list)
    story: dict | None = None
    steps: list = field(default_factory=list)


@dataclass
class Step:
    """Single step within a lesson, with both markdown and rendered HTML content."""

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
    """Logical grouping of lessons within a tier."""

    id: str
    title: str
    tier: int
    description: str
    lessons: list[Lesson] = field(default_factory=list)


@dataclass
class Tier:
    """Top‑level container that groups chapters by difficulty or progression level."""

    tier: int
    title: str
    chapters: list[Chapter] = field(default_factory=list)


@dataclass
class ManifestStats:
    total_lessons: int
    total_estimated_minutes: int
    lessons_with_story: int


@dataclass
class ManifestLesson:
    id: str
    title: str
    order: int
    estimated_minutes: int
    has_story: bool


@dataclass
class ManifestChapter:
    id: str
    title: str
    description: str
    lessons: list[ManifestLesson] = field(default_factory=list)


@dataclass
class ManifestTier:
    tier: int
    title: str
    chapters: list[ManifestChapter] = field(default_factory=list)


@dataclass
class Manifest:
    version: str
    generated_at: str
    stats: ManifestStats
    tiers: list[ManifestTier] = field(default_factory=list)
