import dataclasses
import os
import markdown
import json
from enum import Enum
from techroot_lesson_parser.error_classes import (
    ParseError,
    SeverityType,
    ValidationError,
)
from techroot_lesson_parser.parser import parse_lesson
from techroot_lesson_parser.validator import lesson_validator


def lesson_builder(lesson_path: str, output_folder: str):

    with open(lesson_path) as f:
        lesson_content = f.read()

        try:
            lesson = parse_lesson(lesson_content)
        except ParseError as e:
            return [
                ValidationError(
                    message=str(e), source="Lesson Parsing", severity=SeverityType.ERROR
                )
            ]

        val_errs = lesson_validator(lesson)

        if any(e.severity == SeverityType.ERROR for e in val_errs):
            return val_errs

        # HTML Creation in Steps
        for step in lesson.steps:
            step.content_html = markdown.markdown(step.content_md)

        # Write JSON
        json_output = json.dumps(
            dataclasses.asdict(lesson),
            default=lambda x: x.value if isinstance(x, Enum) else x,
        )

        os.makedirs(output_folder, exist_ok=True)
        with open(os.path.join(output_folder, f"{lesson.id}.json"), "w") as json_file:
            json_file.write(json_output)

        return val_errs
