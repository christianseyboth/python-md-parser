import yaml
import shlex
from techroot_lesson_parser.error_classes import ParseError
from techroot_lesson_parser.models import Chapter, Lesson, Step, StepType, ValidatorType


ATTR_TYPES = {"wpm_goal": int, "estimated_minutes": int, "validator": ValidatorType}


def split_frontmatter(content: str) -> tuple[dict, str]:
    parts = content.split("---", 2)
    frontmatter = yaml.safe_load(parts[1])

    body = parts[2].strip()

    return frontmatter, body


def parse_steps(body: str) -> list[Step]:
    lines = body.split("\n")
    steps = []
    order = 0
    current_type = None
    current_attrs = {}
    content_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("::") and stripped != "::":
            order += 1
            parts = shlex.split(
                stripped
            )  # shlex erkennt Werte mit Leerzeichen in "" -> shell-artiges Parsing
            current_type = parts[0][2:].lower()  # "::typing" -> "typing"

            if current_type not in StepType:
                raise ParseError(
                    f"This Step Type is not allowed: {current_type} at step {order}"
                )

            attributes = {}

            for part in parts[1:]:
                if "=" in part:
                    key, value = part.split("=", 1)

                    if key in ATTR_TYPES:
                        value = ATTR_TYPES[key](value)
                    attributes[key] = value

            current_attrs = attributes
            content_lines = []

        elif stripped == "::":
            steps.append(
                Step(
                    type=StepType(current_type),
                    order=order,
                    content_md="\n".join(content_lines).strip(),
                    **current_attrs,
                )
            )

            current_attrs = {}
            current_type = None

        else:
            content_lines.append(line)

    return steps


# Create Chapter
def parse_chapter(path: str) -> Chapter:
    with open(path) as f:
        obj = yaml.safe_load(f)
        return Chapter(**obj)


# Create Lesson Object
def parse_lesson(content: str) -> Lesson:
    frontmatter, body = split_frontmatter(content)
    steps = parse_steps(body)

    return Lesson(**frontmatter, steps=steps)
