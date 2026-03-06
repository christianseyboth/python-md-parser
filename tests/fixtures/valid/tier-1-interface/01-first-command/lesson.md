---
id: "first-command"
title: "Your First Command"
estimated_minutes: 5
prerequisites: []
story:
  scene: "rain_terminal"
  audio: "ambient_rain"
  narrative: "The screen flickers. A cursor blinks."
---

::text
Every system starts with a blinking cursor.
This is where your journey begins.
::

::typing target="ls -la /home/user" wpm_goal=30
Type the command exactly as shown.
::

::text
`ls` lists files. The `-la` flag shows _all_ files with details.
Simple — but now you've spoken to the machine.
::

::terminal expected_output="total 0" validator="contains"
Now try it yourself. List the contents of an empty directory:
::

::checkpoint
You just ran your first command.
Most people never open a terminal. You did.
::
