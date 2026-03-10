import json
from techroot_lesson_parser.builder import lesson_builder
from techroot_lesson_parser.error_classes import SeverityType, ValidationError


def test_builder_has_valid_path(tmp_path):
    result = lesson_builder(
        "tests/fixtures/valid/tier-1-interface/01-first-command/lesson.md",
        str(tmp_path),
    )

    output_file = tmp_path / "first-command.json"
    assert output_file.exists()

    data = json.loads(output_file.read_text())
    assert data["id"] == "first-command"
    assert data["title"] == "Your First Command"
    assert data["estimated_minutes"] == 5
    assert len(data["steps"]) == 5
    assert data["steps"][0]["content_html"] != ""
    assert "<p>" in data["steps"][0]["content_html"]


def test_builder_has_validation_errors(tmp_path):
    result = lesson_builder("tests/fixtures/invalid/missing-id.md", str(tmp_path))

    assert result[0] == ValidationError(
        message="Lesson ID is missing or wrong declared!",
        source="lesson:frontmatter -> id: ",
        severity=SeverityType.ERROR,
    )


def test_builder_has_parser_errors(tmp_path):
    result = lesson_builder("tests/fixtures/invalid/lesson.md", str(tmp_path))

    assert result[0] == ValidationError(
        message="This Step Type is not allowed: foo at step 1",
        source="Lesson Parsing",
        severity=SeverityType.ERROR,
    )
