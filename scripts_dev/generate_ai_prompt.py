import os
from pathlib import Path

# Settings
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_FILE = PROJECT_ROOT / "all_python_code.txt"
EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", "venv", ".venv", "egg-info"}


def generate_project_tree(dir_path, prefix=""):
    """Creates a visual filter tree over the project."""
    tree = ""
    entries = sorted(list(dir_path.iterdir()), key=lambda x: (x.is_file(), x.name))
    entries = [e for e in entries if e.name not in EXCLUDE_DIRS]

    for i, entry in enumerate(entries):
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "
        tree += f"{prefix}{connector}{entry.name}\n"

        if entry.is_dir():
            next_prefix = prefix + ("    " if is_last else "│   ")
            tree += generate_project_tree(entry, next_prefix)
    return tree


def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        # 1. Print the project structure first
        out.write("==================================================\n")
        out.write("PROJECT DIRECTORY TREE\n")
        out.write("==================================================\n")
        out.write(generate_project_tree(PROJECT_ROOT))
        out.write("\n\n")

        # 2. Loop through and add all Python files
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Filter out unwanted folders
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in sorted(files):
                if file.endswith(".py") and file != "generate_ai_prompt.py":
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(PROJECT_ROOT)

                    # Clear header for Google AI to read
                    out.write("==================================================\n")
                    out.write(f"FILE: {relative_path}\n")
                    out.write("==================================================\n")

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            out.write(f.read())
                    except Exception as e:
                        out.write(f"# Error reading file: {str(e)}\n")
                    out.write("\n\n")

    print(f"Done! All code has been collected in: {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
