from turtle import title
from error_classes import SeverityType, ValidationError
from techroot_lesson_parser.models import Lesson, StepType, ValidatorType
from techroot_lesson_parser.parser import parse_lesson
import re


def lesson_validator(obj: Lesson) -> list[ValidationError]:
    val_errs = []

    # Frontmatter Validation
    if not isinstance(obj.id, str) or len(obj.id) == 0:
        val_errs.append(
            ValidationError(
                message="Lesson ID is missing or wrong declared!",
                source=f"lesson:frontmatter -> id: {obj.id}",
                severity=SeverityType.ERROR,
            )
        )

    if not isinstance(obj.title, str) or len(obj.title) == 0:
        val_errs.append(
            ValidationError(
                message="Lesson Title is missing or wrong declared!",
                source=f"lesson:frontmatter -> title: {obj.title}",
                severity=SeverityType.ERROR,
            )
        )

    if not isinstance(obj.estimated_minutes, int) or obj.estimated_minutes <= 0:
        val_errs.append(
            ValidationError(
                message="Lessons estimated minutes must be a positive number",
                source=f"lesson:frontmatter -> estimated_minutes: {obj.estimated_minutes}",
                severity=SeverityType.ERROR,
            )
        )

    if len(obj.steps) == 0:
        val_errs.append(
            ValidationError(
                message="At least one Lesson Step must be defined",
                source=f"lesson: frontmatter -> steps: {obj.steps}",
                severity=SeverityType.ERROR,
            )
        )
    else:
        # Step Validation
        for step in obj.steps:
            if step.content_md is None:
                val_errs.append(
                    ValidationError(
                        message="Step content must be set!",
                        source=f"lesson: {obj.title} -> step: {step.order}",
                        severity=SeverityType.ERROR,
                    )
                )
            # Step Type Validation
            if step.type == StepType.TYPING and not step.target:
                val_errs.append(
                    ValidationError(
                        message="Typing-Target must be set!",
                        source=f"lesson: {obj.title} -> step: {step.order}",
                        severity=SeverityType.ERROR,
                    )
                )
            # Terminal
            if step.type == StepType.TERMINAL and step.expected_output is None:
                val_errs.append(
                    ValidationError(
                        message="Terminal-Expected-Output must be set!",
                        source=f"lesson: {obj.title} -> step: {step.order}",
                        severity=SeverityType.ERROR,
                    )
                )

            if step.type == StepType.TERMINAL and step.validator not in ValidatorType:
                val_errs.append(
                    ValidationError(
                        message="Terminal Step Validator is not correct",
                        source=f"lesson: {obj.title} -> step: {step.order}",
                        severity=SeverityType.ERROR,
                    )
                )
            if (
                step.type == StepType.TERMINAL
                and step.validator == ValidatorType.REGEX
                and step.expected_output is not None
            ):
                try:
                    pattern = re.compile(step.expected_output)
                except re.error as e:
                    val_errs.append(
                        ValidationError(
                            message=f"Regex Validation failed, error: {e}",
                            source=f"lesson: {obj.title} -> step: {step.order}",
                            severity=SeverityType.ERROR,
                        )
                    )

            # wpm-goal
            if step.wpm_goal is not None and step.wpm_goal <= 0:
                val_errs.append(
                    ValidationError(
                        message=f"wpm goal must be a positive number, actual: {step.wpm_goal}",
                        source=f"lesson: {obj.title} -> step: {step.order}",
                        severity=SeverityType.ERROR,
                    )
                )

    return val_errs


file = open("tests/fixtures/invalid/lesson.md")
content = file.read()

result = parse_lesson(content)

print(lesson_validator(result))
