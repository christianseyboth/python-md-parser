from dataclasses import asdict
import json
from techroot_lesson_parser.content_tree import create_content_tree
from techroot_lesson_parser.models import Tier


def test_content_tree_return_type():
    result = create_content_tree("tests/fixtures/valid")

    assert all(isinstance(item, Tier) for item in result)


def test_content_tree_frontmatter():
    result = create_content_tree("tests/fixtures/valid")
    tier = asdict(result[0])

    assert tier["tier"] == 1
    assert tier["title"] == "tier-1-interface"
    assert tier["chapters"][0]["id"] == "terminal-basics"
    assert tier["chapters"][0]["lessons"][0]["title"] == "Your First Command"
    assert tier["chapters"][0]["lessons"][1]["title"] == "List file system"
