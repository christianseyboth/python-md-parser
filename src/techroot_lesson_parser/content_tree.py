import os
from pathlib import Path

from techroot_lesson_parser.models import Tier


def create_content_tree(content_root: str) -> list[Tier]:
    tier_folders = sorted(
        [path for path in Path(content_root).glob("tier*") if path.is_dir()],
        key=lambda x: int(x.name.split("-")[1]),
    )

    return tier_folders


print(create_content_tree("tests/fixtures/valid"))
