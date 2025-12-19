# Project Brief: pomo-tui

## Overview

| Field | Value |
|-------|-------|
| **Project Name** | pomo-tui |
| **Project Type** | CLI |
| **Goal** | A terminal-based Pomodoro timer with a clean TUI interface for focused work sessions |
| **Timeline** | 1 day |
| **Team Size** | 1 |

## Target Users

- Developers who work in the terminal
- Remote workers who want distraction-free focus timers
- Anyone who uses the Pomodoro technique for productivity

## Features

### Must-Have (MVP)

1. **Timer Display** - Large, clear countdown timer showing MM:SS in the center of the terminal
2. **Work/Break Modes** - 25-minute work sessions, 5-minute short breaks, 15-minute long breaks (after 4 work sessions)
3. **Keyboard Controls** - Space to start/pause, R to reset, Q to quit
4. **Session Counter** - Track completed Pomodoro sessions (work periods)
5. **Visual Feedback** - Different colors for work mode (red/orange) vs break mode (green/blue)

### Nice-to-Have (v2)

- Configurable timer durations via command-line flags
- Sound notification when timer completes (bell character)
- Session history/statistics
- Custom themes

## Technical Requirements

### Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| TUI Framework | textual |
| Package Manager | uv |
| Testing | pytest |

### Constraints

- Must work on Linux, macOS, and Windows terminals
- No external API dependencies (fully offline)
- Single-file installation via `pip install`
- Terminal must be at least 40x10 characters

### Architecture

```
pomo-tui/
├── src/
│   └── pomo_tui/
│       ├── __init__.py
│       ├── __main__.py      # Entry point
│       ├── app.py           # Main Textual App
│       ├── timer.py         # Timer logic
│       └── widgets.py       # Custom TUI widgets
├── tests/
│   ├── test_timer.py
│   └── test_app.py
├── pyproject.toml
└── README.md
```

## Success Criteria

1. `pomo` command launches the TUI and displays a timer
2. Pressing Space starts/pauses the countdown
3. Timer transitions from work → break → work automatically
4. Session counter increments after each completed work period
5. All keyboard controls work as documented
6. Tests pass with >80% coverage

## Out of Scope

- GUI version
- Mobile app
- Cloud sync
- User accounts
- Integration with other productivity tools
