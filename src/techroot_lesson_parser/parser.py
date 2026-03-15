import yaml
import shlex
from techroot_lesson_parser.error_classes import ParseError
from techroot_lesson_parser.models import Chapter, Lesson, Step, StepType, ValidatorType


ATTR_TYPES = {
    # YAML frontmatter fields that need type coercion when parsed from step headers
    "wpm_goal": int,
    "estimated_minutes": int,
    "validator": ValidatorType,
}


def split_frontmatter(content: str) -> tuple[dict, str]:
    """Split a lesson file into YAML frontmatter and markdown body."""
    parts = content.split("---", 2)
    frontmatter = yaml.safe_load(parts[1])

    body = parts[2].strip()

    return frontmatter, body


def parse_steps(body: str) -> list[Step]:
    """Parse `::block` style step sections from the markdown body."""
    lines = body.split("\n")
    steps = []
    order = 0
    current_type = None
    current_attrs: dict = {}
    content_lines: list[str] = []

    for line in lines:
        stripped = line.strip()

        # Opening delimiter, e.g. '::typing target="ls" wpm_goal=30'
        if stripped.startswith("::") and stripped != "::":
            order += 1
            # `shlex` allows shell-like parsing so quoted values with spaces are preserved
            parts = shlex.split(stripped)
            current_type = parts[0][2:].lower()  # "::typing" -> "typing"

            if current_type not in StepType:
                raise ParseError(
                    f"This Step Type is not allowed: {current_type} at step {order}"
                )

            attributes: dict = {}

            # Parse key=value attributes in the header line
            for part in parts[1:]:
                if "=" in part:
                    key, value = part.split("=", 1)

                    if key in ATTR_TYPES:
                        value = ATTR_TYPES[key](value)
                    attributes[key] = value

            current_attrs = attributes
            content_lines = []

        # Closing delimiter '::' finalizes the current step
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
            # Regular markdown content inside a step
            content_lines.append(line)

    return steps


def parse_chapter(path: str) -> Chapter:
    """Load a chapter definition from its `_chapter.yaml` file."""
    with open(path) as f:
        obj = yaml.safe_load(f)
        return Chapter(**obj)


def parse_lesson(content: str) -> Lesson:
    """Parse a full lesson markdown document into a `Lesson` dataclass."""
    frontmatter, body = split_frontmatter(content)
    steps = parse_steps(body)

    return Lesson(**frontmatter, steps=steps)
