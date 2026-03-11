from dataclasses import asdict
import json
from techroot_lesson_parser.content_tree import create_content_tree
from techroot_lesson_parser.models import Tier


def test_content_tree_return_type():
    result = create_content_tree("tests/fixtures/valid")

    assert all(isinstance(item, Tier) for item in result)


def test_content_tree_frontmatter():
    result = create_content_tree("tests/fixtures/valid")

    assert result[0].tier == 1
    assert result[0].title == "tier-1-interface"
    assert result[0].chapters[0].id == "terminal-basics"
    assert result[0].chapters[0].lessons[0].title == "Your First Command"
    assert result[0].chapters[0].lessons[1].title == "List file system"
