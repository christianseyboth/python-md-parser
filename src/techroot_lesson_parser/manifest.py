import dataclasses
import json
import os
from datetime import datetime
from enum import Enum

from techroot_lesson_parser.content_tree import create_content_tree
from techroot_lesson_parser.models import (
    Manifest,
    ManifestChapter,
    ManifestLesson,
    ManifestStats,
    ManifestTier,
    Tier,
)


def create_manifest(content_tree: list[Tier]) -> Manifest:
    """Create a manifest view over the full content tree.

    This flattens rich `Tier` / `Chapter` / `Lesson` structures into a compact
    summary with aggregate statistics for downstream consumers (e.g. frontends).
    """
    manifest_tiers: list[ManifestTier] = []

    for tier in content_tree:
        manifest_tier = ManifestTier(
            tier=tier.tier,
            title=tier.title,
            chapters=[
                ManifestChapter(
                    id=chapter.id,
                    title=chapter.title,
                    description=chapter.description,
                    lessons=[
                        ManifestLesson(
                            id=lesson.id,
                            title=lesson.title,
                            # Lessons are ordered by position inside their chapter folder
                            order=idx + 1,
                            estimated_minutes=lesson.estimated_minutes,
                            has_story=lesson.story is not None,
                        )
                        for idx, lesson in enumerate(chapter.lessons)
                    ],
                )
                for chapter in tier.chapters
            ],
        )
        manifest_tiers.append(manifest_tier)

    manifest = Manifest(
        version="1.0.0",
        generated_at=datetime.now().isoformat(),
        stats=ManifestStats(
            total_lessons=sum(
                len(chapter.lessons)
                for tier in manifest_tiers
                for chapter in tier.chapters
            ),
            total_estimated_minutes=sum(
                lesson.estimated_minutes
                for tier in manifest_tiers
                for chapter in tier.chapters
                for lesson in chapter.lessons
            ),
            lessons_with_story=sum(
                lesson.has_story
                for tier in manifest_tiers
                for chapter in tier.chapters
                for lesson in chapter.lessons
            ),
        ),
        tiers=manifest_tiers,
    )
    return manifest


def write_manifest(manifest: Manifest, output_folder: str):
    """Serialize a `Manifest` to `manifest.json` in the given folder."""
    json_output = json.dumps(
        dataclasses.asdict(manifest),
        # Convert Enum values to their primitive representation for JSON
        default=lambda x: x.value if isinstance(x, Enum) else x,
    )

    os.makedirs(output_folder, exist_ok=True)
    with open(os.path.join(output_folder, "manifest.json"), "w") as json_file:
        json_file.write(json_output)
