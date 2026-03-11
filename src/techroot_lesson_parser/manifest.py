from datetime import datetime
from techroot_lesson_parser.models import (
    Manifest,
    ManifestChapter,
    ManifestLesson,
    ManifestStats,
    ManifestTier,
    Tier,
)


def create_manifest(content_tree: list[Tier]) -> Manifest:
    manifest_tiers = []

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
