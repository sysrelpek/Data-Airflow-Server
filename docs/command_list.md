# Command List - Our Custom Orchestra Language

---

This document defines the official commands that Mozart (you) can give to the Orchestra (me) for working on this project.

## GitHub Related Commands

### Reading / Pulling Files
```
- `github__pull_updated_files` → Pull and show all recently updated files
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

- The filepath/filname is refer to the code that GROK present in the chat thread/project.

- If no filename is present direct above tho code that GROK want to change any pushing is NOT valid.

- If code snippet, chunk or all code in a file has been present by GROOK in the thread/project
  more than one time the filename refer to the latest present.
```



### General Rules
```
- GROOK is the Orchestra.

- GROOK are only permitted to perform GitHub write operations when GROOK receiving explicitly  
  command from the project oener.

- All commands must be clearly written.
```

### Update Command List
```
This file will evolve to define more commands.* in the future to make ensure any command added, removed 
or changed is read by GROOK, the command:  github__pull_updated_file[docs/command_list.md]  must be made.  
```
----


