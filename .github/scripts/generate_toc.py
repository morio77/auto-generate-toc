import os
from pathlib import Path

HEADER = "<!-- AUTO-TOC-START -->\n"
FOOTER = "<!-- AUTO-TOC-END -->\n"
INDENT = "  "

def generate_toc_for_dir(dir_path: Path, base_path: Path = None, depth: int = 0, max_depth: int = 3) -> list[str]:
    if base_path is None:
        base_path = dir_path

    toc_lines = []

    for item in sorted(dir_path.iterdir()):
        if item.name.startswith('.') or item.name == "README.md":
            continue

        relative_path = item.relative_to(base_path)
        display_path = relative_path.as_posix()
        indent = INDENT * depth

        if item.is_file() and item.suffix == '.md':
            toc_lines.append(f"{indent}- [{item.name}]({display_path})")

        elif item.is_dir():
            readme_link = f"{display_path}/README.md" if (item / "README.md").exists() else display_path
            toc_lines.append(f"{indent}- [{item.name}]({readme_link})")

            if depth < max_depth:
                toc_lines.extend(generate_toc_for_dir(item, base_path, depth + 1, max_depth))

    return toc_lines

def update_readme(readme_path: Path, max_depth: int = 3):
    dir_path = readme_path.parent
    toc = HEADER + '\n'.join(generate_toc_for_dir(dir_path, max_depth=max_depth)) + '\n' + FOOTER

    if readme_path.exists():
        content = readme_path.read_text(encoding='utf-8')
        if HEADER in content and FOOTER in content:
            start = content.index(HEADER)
            end = content.index(FOOTER) + len(FOOTER)
            new_content = content[:start] + toc + content[end:]
        else:
            new_content = toc + '\n' + content
    else:
        new_content = toc + '\n# ' + dir_path.name + '\n'

    readme_path.write_text(new_content, encoding='utf-8')

def main():
    for root, dirs, files in os.walk("."):
        path = Path(root)
        if any(part.startswith(".") for part in path.parts):
            continue
        readme = path / "README.md"
        update_readme(readme, max_depth=3)

if __name__ == "__main__":
    main()
