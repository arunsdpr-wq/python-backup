#!/usr/bin/env python3
import argparse
import os
import shutil
from datetime import datetime
from pathlib import Path

def make_unique_name(dest_dir: Path, filename: str) -> Path:
    """Return a unique destination path, appending timestamp if needed."""
    dest_path = dest_dir / filename
    if not dest_path.exists():
        return dest_path

    stem = dest_path.stem           # name without extension
    suffix = dest_path.suffix       # extension (e.g. ".txt")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = f"{stem}_{timestamp}{suffix}"
    return dest_dir / new_name

def backup_directory(src: Path, dst: Path) -> None:
    if not src.exists() or not src.is_dir():
        raise FileNotFoundError(f"Source directory does not exist: {src}")

    if not dst.exists():
        # create destination directory (including parents)
        dst.mkdir(parents=True, exist_ok=True)

    for entry in src.iterdir():
        if entry.is_file():
            unique_dest = make_unique_name(dst, entry.name)
            shutil.copy2(entry, unique_dest)
            print(f"Copied: {entry} -> {unique_dest}")
        # if you also want to handle subdirectories, you can extend here

def parse_args():
    parser = argparse.ArgumentParser(
        description="Simple backup script: copy files from source to destination."
    )
    parser.add_argument("source", help="Path to source directory")
    parser.add_argument("destination", help="Path to destination directory")
    return parser.parse_args()

def main():
    args = parse_args()
    src = Path(args.source)
    dst = Path(args.destination)

    try:
        backup_directory(src, dst)
        print("Backup completed successfully.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"Unexpected error during backup: {e}")

if __name__ == "__main__":
    main()
