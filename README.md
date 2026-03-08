# techroot-lesson-parser

A Python parser for techroot lesson content. Parses markdown lessons with YAML frontmatter and chapter metadata into structured dataclasses.

## Installation

```bash
uv sync
```

Requires Python ≥3.14.

## Usage

### Parse a lesson

```python
from techroot_lesson_parser.parser import parse_lesson

with open("path/to/lesson.md") as f:
    lesson = parse_lesson(f.read())
```

### Parse a chapter

```python
from techroot_lesson_parser.parser import parse_chapter

chapter = parse_chapter("path/to/_chapter.yaml")
```

## Lesson format

Lessons are markdown files with:

1. **YAML frontmatter** (between `---` delimiters):
   - `id`, `title`, `estimated_minutes` (required)
   - `prerequisites` (list)
   - `story` (optional dict: `scene`, `audio`, `narrative`)

2. **Step blocks** using `::type` syntax:

| Block       | Attributes                    | Description                    |
|-------------|-------------------------------|--------------------------------|
| `::text`    | —                             | Instructional text             |
| `::typing`  | `target`, `wpm_goal`          | Type a command (shell-quoted)   |
| `::terminal`| `expected_output`, `validator`| Run command, validate output   |
| `::checkpoint` | —                          | Milestone / recap              |

**Validators:** `exact`, `contains`, `regex`

**Example:**

```markdown
---
id: "first-command"
title: "Your First Command"
estimated_minutes: 5
prerequisites: []
story:
  scene: "rain_terminal"
  narrative: "The screen flickers."
---

::text
Every system starts with a blinking cursor.
::

::typing target="ls -la /home/user" wpm_goal=30
Type the command exactly as shown.
::

::terminal expected_output="total 0" validator="contains"
Now try it yourself.
::
```

## Chapter format

Chapters are YAML files:

```yaml
id: "terminal-basics"
title: "Terminal Basics"
tier: 1
description: "Your first steps in the terminal."
```

## Data models

- **Lesson**: `id`, `title`, `estimated_minutes`, `prerequisites`, `story`, `steps`
- **Step**: `type` (StepType), `order`, `content_md`, plus type-specific fields (`target`, `wpm_goal`, `expected_output`, `validator`)
- **Chapter**: `id`, `title`, `tier`, `description`, `lessons`

## Development

```bash
uv sync
uv run pytest
```
