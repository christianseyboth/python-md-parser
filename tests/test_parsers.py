from techroot_lesson_parser.models import Chapter, Lesson, Step, StepType, ValidatorType
from techroot_lesson_parser.parser import (
    parse_chapter,
    parse_lesson,
    parse_steps,
    split_frontmatter,
)


def test_parser_chapter():
    result = parse_chapter("tests/fixtures/valid/tier-1-interface/_chapter.yaml")

    assert result == Chapter(
        id="terminal-basics",
        title="Terminal Basics",
        tier=1,
        description="Your first steps in the terminal.",
    )


def test_parse_steps():

    with open("tests/fixtures/valid/tier-1-interface/01-first-command/lesson.md") as f:
        content = f.read()
        frontmatter, body = split_frontmatter(content)
    result = parse_steps(body)

    assert result == [
        Step(
            type=StepType.TEXT,
            order=1,
            content_md="Every system starts with a blinking cursor.\nThis is where your journey begins.",
            content_html="",
            target=None,
            wpm_goal=None,
            expected_output=None,
            validator=ValidatorType.EXACT,
        ),
        Step(
            type=StepType.TYPING,
            order=2,
            content_md="Type the command exactly as shown.",
            content_html="",
            target="ls -la /home/user",
            wpm_goal=30,
            expected_output=None,
            validator=ValidatorType.EXACT,
        ),
        Step(
            type=StepType.TEXT,
            order=3,
            content_md="`ls` lists files. The `-la` flag shows _all_ files with details.\nSimple — but now you've spoken to the machine.",
            content_html="",
            target=None,
            wpm_goal=None,
            expected_output=None,
            validator=ValidatorType.EXACT,
        ),
        Step(
            type=StepType.TERMINAL,
            order=4,
            content_md="Now try it yourself. List the contents of an empty directory:",
            content_html="",
            target=None,
            wpm_goal=None,
            expected_output="total 0",
            validator=ValidatorType.CONTAINS,
        ),
        Step(
            type=StepType.CHECKPOINT,
            order=5,
            content_md="You just ran your first command.\nMost people never open a terminal. You did.",
            content_html="",
            target=None,
            wpm_goal=None,
            expected_output=None,
            validator=ValidatorType.EXACT,
        ),
    ]


def test_parse_lesson():
    with open("tests/fixtures/valid/tier-1-interface/01-first-command/lesson.md") as f:
        content = f.read()

        result = parse_lesson(content)

        assert result == Lesson(
            id="first-command",
            title="Your First Command",
            estimated_minutes=5,
            prerequisites=[],
            story={
                "scene": "rain_terminal",
                "audio": "ambient_rain",
                "narrative": "The screen flickers. A cursor blinks.",
            },
            steps=[
                Step(
                    type=StepType.TEXT,
                    order=1,
                    content_md="Every system starts with a blinking cursor.\nThis is where your journey begins.",
                    content_html="",
                    target=None,
                    wpm_goal=None,
                    expected_output=None,
                    validator=ValidatorType.EXACT,
                ),
                Step(
                    type=StepType.TYPING,
                    order=2,
                    content_md="Type the command exactly as shown.",
                    content_html="",
                    target="ls -la /home/user",
                    wpm_goal=30,
                    expected_output=None,
                    validator=ValidatorType.EXACT,
                ),
                Step(
                    type=StepType.TEXT,
                    order=3,
                    content_md="`ls` lists files. The `-la` flag shows _all_ files with details.\nSimple — but now you've spoken to the machine.",
                    content_html="",
                    target=None,
                    wpm_goal=None,
                    expected_output=None,
                    validator=ValidatorType.EXACT,
                ),
                Step(
                    type=StepType.TERMINAL,
                    order=4,
                    content_md="Now try it yourself. List the contents of an empty directory:",
                    content_html="",
                    target=None,
                    wpm_goal=None,
                    expected_output="total 0",
                    validator=ValidatorType.CONTAINS,
                ),
                Step(
                    type=StepType.CHECKPOINT,
                    order=5,
                    content_md="You just ran your first command.\nMost people never open a terminal. You did.",
                    content_html="",
                    target=None,
                    wpm_goal=None,
                    expected_output=None,
                    validator=ValidatorType.EXACT,
                ),
            ],
        )
