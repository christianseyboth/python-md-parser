from techroot_lesson_parser.content_tree import create_content_tree
from techroot_lesson_parser.manifest import create_manifest
from techroot_lesson_parser.models import (
    ManifestChapter,
    ManifestLesson,
    ManifestStats,
    ManifestTier,
)


def test_create_manifest():
    content_tree = create_content_tree("tests/fixtures/valid")
    manifest = create_manifest(content_tree)

    assert all(isinstance(tier, ManifestTier) for tier in manifest.tiers)
    assert all(
        isinstance(chapter, ManifestChapter)
        for tier in manifest.tiers
        for chapter in tier.chapters
    )
    assert all(
        isinstance(lesson, ManifestLesson)
        for tier in manifest.tiers
        for chapter in tier.chapters
        for lesson in chapter.lessons
    )
    assert isinstance(manifest.stats, ManifestStats)

    assert manifest.stats.total_lessons == 2
    assert manifest.stats.lessons_with_story == 2
    assert manifest.tiers[0].chapters[0].lessons[0].id == "first-command"
