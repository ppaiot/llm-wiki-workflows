#!/usr/bin/env python3
"""One-way mirror of template .md files from the git tree into the Obsidian vault."""

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "tools" / "config.toml"
EXAMPLE_CONFIG_PATH = REPO_ROOT / "tools" / "config.example.toml"


class GuardError(Exception):
    """Raised for any fail-loud guard violation."""


def load_config():
    if not CONFIG_PATH.exists():
        raise GuardError(
            f"Missing config file: {CONFIG_PATH}\n"
            f"Copy {EXAMPLE_CONFIG_PATH.name} to config.toml in the same folder "
            "and set your real vault_root."
        )
    with open(CONFIG_PATH, "rb") as f:
        data = tomllib.load(f)

    vault_root = data.get("vault_root")
    if not vault_root or not isinstance(vault_root, str):
        raise GuardError(f"config.toml is missing a valid 'vault_root' string entry.")

    mirrors = data.get("mirrors")
    if not mirrors or not isinstance(mirrors, list):
        raise GuardError("config.toml is missing a valid 'mirrors' list entry.")

    for entry in mirrors:
        if not (isinstance(entry, list) and len(entry) == 2):
            raise GuardError(f"Invalid mirrors entry (expected [repo_subdir, vault_subdir]): {entry!r}")

    # Read vault_root literally -- no expanduser. The vault folder name contains
    # a literal '~' (iCloud~md~obsidian); expansion would corrupt the path.
    return Path(vault_root), mirrors


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_md_files(root: Path) -> dict:
    """Return {relative_posix_path: absolute_path} for all *.md files under root, recursive."""
    result = {}
    for path in root.rglob("*.md"):
        if path.is_file():
            result[path.relative_to(root).as_posix()] = path
    return result


def mirror_one(source_dir: Path, dest_dir: Path, dry_run: bool, prune: bool, verbose: bool, stats: dict):
    if not source_dir.exists() or not source_dir.is_dir():
        raise GuardError(f"Source directory does not exist: {source_dir}")

    if not dest_dir.exists():
        if dry_run:
            if verbose:
                print(f"[dry-run] would create directory: {dest_dir}")
        else:
            try:
                dest_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                raise GuardError(f"Could not create vault destination folder {dest_dir}: {e}")

    source_files = find_md_files(source_dir)
    dest_files = find_md_files(dest_dir) if dest_dir.exists() else {}

    for rel_path, src_path in source_files.items():
        dest_path = dest_dir / rel_path
        src_hash = sha256_of(src_path)

        if rel_path not in dest_files:
            action = "copy (new)"
            do_copy = True
        else:
            dest_hash = sha256_of(dest_files[rel_path])
            if dest_hash == src_hash:
                action = "skip (unchanged)"
                do_copy = False
            else:
                action = "overwrite (changed)"
                do_copy = True

        if verbose:
            print(f"[{dest_dir.name}] {action}: {rel_path}")

        if do_copy:
            stats["copied"].append(str(dest_path))
            if not dry_run:
                try:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(src_path, dest_path)
                except OSError as e:
                    raise GuardError(f"Could not write {dest_path}: {e}")
        else:
            stats["skipped"] += 1

    orphan_rel_paths = set(dest_files) - set(source_files)
    for rel_path in sorted(orphan_rel_paths):
        orphan_path = dest_files[rel_path]
        if prune:
            stats["pruned"].append(str(orphan_path))
            if verbose:
                print(f"[{dest_dir.name}] prune: {rel_path}")
            if not dry_run:
                try:
                    orphan_path.unlink()
                except OSError as e:
                    raise GuardError(f"Could not delete orphan {orphan_path}: {e}")
        else:
            stats["would_prune"].append(str(orphan_path))
            if verbose:
                print(f"[{dest_dir.name}] would prune: {rel_path}")


def main():
    parser = argparse.ArgumentParser(description="Mirror template .md files from the git tree into the Obsidian vault.")
    parser.add_argument("--dry-run", action="store_true", help="Show intended actions, change nothing.")
    parser.add_argument("--prune", action="store_true", help="Delete orphan .md files in mapped dest folders.")
    parser.add_argument("--verbose", action="store_true", help="Print per-file decisions.")
    args = parser.parse_args()

    try:
        vault_root, mirrors = load_config()
    except GuardError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    stats = {"copied": [], "skipped": 0, "pruned": [], "would_prune": []}

    for repo_subdir, vault_subdir in mirrors:
        source_dir = REPO_ROOT / repo_subdir
        dest_dir = vault_root / vault_subdir
        try:
            mirror_one(source_dir, dest_dir, args.dry_run, args.prune, args.verbose, stats)
        except GuardError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1

    print()
    print("Summary" + (" (dry-run, no changes made)" if args.dry_run else "") + ":")
    print(f"  copied/overwritten: {len(stats['copied'])}")
    print(f"  skipped (unchanged): {stats['skipped']}")
    if args.prune:
        print(f"  pruned: {len(stats['pruned'])}")
    else:
        print(f"  would prune (not deleted, pass --prune to delete): {len(stats['would_prune'])}")

    if stats["copied"]:
        print("\nFiles written:")
        for p in stats["copied"]:
            print(f"  {p}")

    prune_list = stats["pruned"] if args.prune else stats["would_prune"]
    if prune_list:
        label = "Files deleted" if args.prune else "Orphans (would prune)"
        print(f"\n{label}:")
        for p in prune_list:
            print(f"  {p}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
