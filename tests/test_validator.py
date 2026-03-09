from techroot_lesson_parser.error_classes import SeverityType
from techroot_lesson_parser.models import Lesson, Step, StepType, ValidatorType
from techroot_lesson_parser.validator import lesson_validator


def _base_valid_lesson() -> Lesson:
    """Return a minimal valid lesson that produces no errors."""
    step = Step(
        type=StepType.TEXT,
        order=1,
        content_md="content",
    )
    return Lesson(
        id="lesson-id",
        title="Lesson Title",
        estimated_minutes=5,
        prerequisites=[],
        story=None,
        steps=[step],
    )


def test_valid_lesson_has_no_validation_errors():
    lesson = _base_valid_lesson()

    errors = lesson_validator(lesson)

    assert errors == []


def test_missing_lesson_id_produces_error():
    lesson = _base_valid_lesson()
    lesson.id = ""

    errors = lesson_validator(lesson)

    assert any(
        e.message == "Lesson ID is missing or wrong declared!"
        and e.severity == SeverityType.ERROR
        for e in errors
    )


def test_missing_title_produces_error():
    lesson = _base_valid_lesson()
    lesson.title = ""

    errors = lesson_validator(lesson)

    assert any(
        e.message == "Lesson Title is missing or wrong declared!"
        and e.severity == SeverityType.ERROR
        for e in errors
    )


def test_non_positive_estimated_minutes_produces_error():
    lesson = _base_valid_lesson()
    lesson.estimated_minutes = 0

    errors = lesson_validator(lesson)

    assert any(
        e.message == "Lessons estimated minutes must be a positive number"
        and e.severity == SeverityType.ERROR
        for e in errors
    )


def test_missing_steps_produces_error():
    lesson = _base_valid_lesson()
    lesson.steps = []

    errors = lesson_validator(lesson)

    assert any(
        e.message == "At least one Lesson Step must be defined"
        and e.severity == SeverityType.ERROR
        for e in errors
    )


def test_step_without_content_produces_error():
    lesson = _base_valid_lesson()
    lesson.steps[0].content_md = None

    errors = lesson_validator(lesson)

    assert any(
        e.message == "Step content must be set!" and e.severity == SeverityType.ERROR
        for e in errors
    )


def test_typing_step_without_target_produces_error():
    step = Step(
        type=StepType.TYPING,
        order=1,
        content_md="content",
        target=None,
    )
    lesson = _base_valid_lesson()
    lesson.steps = [step]

    errors = lesson_validator(lesson)

    assert any(
        e.message == "Typing-Target must be set!" and e.severity == SeverityType.ERROR
        for e in errors
    )


def test_terminal_step_without_expected_output_produces_error():
    step = Step(
        type=StepType.TERMINAL,
        order=1,
        content_md="content",
        expected_output=None,
    )
    lesson = _base_valid_lesson()
    lesson.steps = [step]

    errors = lesson_validator(lesson)

    assert any(
        e.message == "Terminal-Expected-Output must be set!"
        and e.severity == SeverityType.ERROR
        for e in errors
    )


def test_terminal_step_with_invalid_validator_produces_error():
    # abusing type: ignore because validator field is typed as ValidatorType
    step = Step(
        type=StepType.TERMINAL,
        order=1,
        content_md="content",
        expected_output="output",
    )
    # type: ignore[attr-defined]
    step.validator = "not-a-validator"  # type: ignore[assignment]
    lesson = _base_valid_lesson()
    lesson.steps = [step]

    errors = lesson_validator(lesson)

    assert any(
        e.message == "Terminal Step Validator is not correct"
        and e.severity == SeverityType.ERROR
        for e in errors
    )


def test_terminal_step_with_invalid_regex_adds_error():
    step = Step(
        type=StepType.TERMINAL,
        order=1,
        content_md="content",
        expected_output="[unclosed",  # invalid regex
        validator=ValidatorType.REGEX,
    )
    lesson = _base_valid_lesson()
    lesson.steps = [step]

    errors = lesson_validator(lesson)

    assert any(
        "Regex Validation failed, error:" in e.message
        and e.severity == SeverityType.ERROR
        for e in errors
    )


def test_step_with_non_positive_wpm_goal_produces_error():
    step = Step(
        type=StepType.TYPING,
        order=1,
        content_md="content",
        target="target",
        wpm_goal=0,
    )
    lesson = _base_valid_lesson()
    lesson.steps = [step]

    errors = lesson_validator(lesson)

    assert any(
        e.message == "wpm goal must be a positive number, actual: 0"
        and e.severity == SeverityType.ERROR
        for e in errors
    )
