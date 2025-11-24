import argparse
import os
from pathlib import Path
import json

def list_markdown_files(vault_path: Path, ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = {'.obsidian', '.trash', '.git', 'attachments'}
    md_files = []
    for root, dirs, files in os.walk(vault_path):
        # modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        for f in files:
            if f.lower().endswith('.md'):
                full = Path(root) / f
                md_files.append(full.relative_to(vault_path).as_posix())
    return sorted(md_files)

def main():
    p = argparse.ArgumentParser(description='Obsidian vault: list .md files and count')
    p.add_argument('vault', nargs='?', default='.', help='Vault root path (default: current dir)')
    p.add_argument('--out', '-o', help='Output list file (default: <vault>/_md_list.txt)')
    p.add_argument('--json', action='store_true', help='Write JSON array instead of plain text')
    args = p.parse_args()

    vault = Path(args.vault).resolve()
    if not vault.exists() or not vault.is_dir():
        print(f'Vault not found: {vault}')
        return

    md_files = list_markdown_files(vault)
    count = len(md_files)
    default_out = vault / '_md_list.txt'
    out_file = Path(args.out) if args.out else default_out

    if args.json:
        out_file.write_text(json.dumps(md_files, ensure_ascii=False, indent=2), encoding='utf-8')
    else:
        out_file.write_text('\n'.join(md_files), encoding='utf-8')

    print(f'Markdown files: {count}')
    print(f'List written to: {out_file}')

if __name__ == '__main__':
    main()