# Command List - Our Custom Orchestra Language

This document defines the official commands that Mozart (you) can give to the Orchestra (me) for working on this project.

## GitHub Related Commands

### Reading / Pulling Files
- `github__pull_updated_files` → Pull and show all recently updated files

### Pushing Files
- `github__push_file_[filepath/filename]` → Push a single file
- `github__push_file_[filepath1]_[filepath2]_[filepath3]` → Push multiple files in one commit

**Note**: File paths are always relative to project root.
If no path is specified, file goes to root.

## General Rules
- You are Mozart. I am the Orchestra.
- I will only perform GitHub write operations when you explicitly give me a command.
- All commands must be clearly written.

---

*This file will evolve as we define more commands.*