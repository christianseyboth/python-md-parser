from techroot_lesson_parser.error_classes import SeverityType
from techroot_lesson_parser.validator import (
    detect_circular_dependencies,
    detect_orphaned_prerequisites,
)


def test_detect_dependencies_happy():
    graph = {
        "first-command": [],
        "navigating-files": ["first-command"],
        "bash-basics": ["navigating-files"],
    }

    result = detect_circular_dependencies(graph)
    assert result == []


def test_detect_dependencies():
    graph = {
        "first-command": ["navigating-files"],
        "navigating-files": ["first-command"],
        "bash-basics": ["navigating-files"],
    }

    result = detect_circular_dependencies(graph)
    assert any(e.severity == SeverityType.ERROR for e in result)


def test_detect_dependencies_key_error():
    graph = {
        "first-command": [],
        "navigating-files": ["second-command"],
        "bash-basics": ["navigating-files"],
    }

    result = detect_orphaned_prerequisites(graph)

    assert any(
        "Orphan found" in e.message and e.severity == SeverityType.ERROR for e in result
    )
