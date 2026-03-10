import os
from pathlib import Path

from techroot_lesson_parser.models import Tier
from techroot_lesson_parser.parser import parse_chapter, parse_lesson


def create_content_tree(content_root: str) -> list[Tier]:
    tiers = []
    tier_folders = sorted(
        [path for path in Path(content_root).glob("tier*") if path.is_dir()],
        key=lambda x: int(x.name.split("-")[1]),
    )

    for tier_path in tier_folders:
        tier = Tier(tier=int(tier_path.name.split("-")[1]), title=tier_path.name)

        chapter_folders = sorted(
            [path for path in Path(tier_path).glob("*") if path.is_dir()],
            key=lambda x: int(x.name.split("-")[0]),
        )

        for chapter_path in chapter_folders:
            chapter = parse_chapter(os.path.join(chapter_path, "_chapter.yaml"))

            lesson_folders = sorted(
                [path for path in Path(chapter_path).glob("*") if path.is_dir()],
                key=lambda x: int(x.name.split("-")[0]),
            )

            for lesson_path in lesson_folders:
                with open(os.path.join(lesson_path, "lesson.md")) as content:
                    lesson = parse_lesson(content.read())
                    chapter.lessons.append(lesson)

            tier.chapters.append(chapter)

        tiers.append(tier)
    return tiers


print(create_content_tree("tests/fixtures/valid"))
