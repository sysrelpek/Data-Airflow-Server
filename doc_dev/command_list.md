# Command List - Our Custom Orchestra Language

---

This document defines the official commands that Mozart (you) can give to the Orchestra (me) for working on this project.

## GitHub Related Commands

### Reading / Pulling Files
```
- `github__pull_updated_files` → Pull and show all recently updated files

- `github__pull_updated_file[filepath/filename]` → Pull and show the latest version of one specific file
```

### Pushing Files
```
- `github__push_file_[filepath/filename]` → Push a single file

- `github__push_file_[filepath/filname1]_[filename2]` → Push multiple files with same or multiple path in one commit
```

### **Note**: 
```
- File paths are always relative to project root.

- If no path is specified, file goes to root.

- The filepath/filename refers to the code that GROK presents in the chat thread/project.

- If no filename is present directly above the code that GROK wants to change, then any pushing is NOT valid.

- If code snippet, chunk or all code in a file has been presented by GROK in the thread/project
  more than one time, the filename refers to the latest version presented.
```

### General Rules
```
- GROOK is the Orchestra.

- GROOK is only permitted to perform GitHub write operations when receiving an explicit  
  command from the project owner (Mozart).

- All commands must be clearly written.
```

### Update Command List
```
This file will evolve to define more commands. In the future, to ensure any command added, removed 
or changed is read by GROK, the command: `github__pull_updated_file[docs/command_list.md]` must be issued first.
```

**New Rule (added 2026-05-12):**  
In the future, whenever the Orchestra wants to change any file, it **must** first present the proposed file code changes, clearly **MARKED WITH THE FILENAME**.

Last updated: 2026-05-12 by the Orchestra
