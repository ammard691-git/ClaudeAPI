import os
from pathlib import Path

import anthropic

MODEL = "claude-haiku-5-5"
MAX_CHARS = 60_000
INCLUDE = {".py", ".js", ".ts", ".java", ".go", ".rs", ".c", ".cpp",
           ".md", ".yml", ".yaml", ".json", ".toml", ".txt", ".html", ".css"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
SKIP_FILES = {"package-lock.json", "yarn.lock", "PROJECT_DESCRIPTION.md", "expenses.json"}


def collect_code(root="."):
    parts, total = [], 0
    for path in sorted(Path(root).rglob("*")):
        if not path.is_file():
            continue
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        if path.name in SKIP_FILES or path.suffix not in INCLUDE:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        chunk = f"--- {path} ---\n{text}\n"
        if total + len(chunk) > MAX_CHARS:
            break
        parts.append(chunk)
        total += len(chunk)
    return "".join(parts)


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set - skipping description.")
        return

    code = collect_code()
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": (
                "Below are the files of a GitHub project. Write a resume-ready "
                "project description: one summary sentence, then 3-4 bullet points "
                "covering what it does, the tech used, and notable features. "
                "Only mention what the code actually shows.\n\n" + code
            ),
        }],
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    Path("PROJECT_DESCRIPTION.md").write_text(
        "# Project description\n\n" + text.strip() + "\n", encoding="utf-8"
    )
    print(text)


if __name__ == "__main__":
    main()
