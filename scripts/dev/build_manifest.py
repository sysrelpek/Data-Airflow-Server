#!/usr/bin/env python3
# =============================================================================
# scripts/dev/build_manifest.py
# CLI tool: Converts YAML manifests from dags/configs/ into JSON manifests
# in dags/manifests/
# =============================================================================

import json
import sys
from pathlib import Path
from typing import List

# Add project root to path so we can import from src/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.business_lib.core.manifest_builder import build_manifest


CONFIG_DIR = PROJECT_ROOT / "dags" / "configs"
OUTPUT_DIR = PROJECT_ROOT / "dags" / "manifests"


def get_yaml_files(directory: Path) -> List[Path]:
    """Return all .yaml and .yml files in the given directory."""
    return sorted(
        list(directory.glob("*.yaml")) + list(directory.glob("*.yml"))
    )


def build_all_manifests(dry_run: bool = False) -> None:
    """Build all manifests from YAML source files."""
    if not CONFIG_DIR.exists():
        print(f"❌ Config directory does not exist: {CONFIG_DIR}")
        sys.exit(1)

    yaml_files = get_yaml_files(CONFIG_DIR)

    if not yaml_files:
        print(f"⚠️  No YAML files found in {CONFIG_DIR}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"🔨 Building manifests from {len(yaml_files)} YAML file(s)...\n")

    for yaml_file in yaml_files:
        try:
            manifest = build_manifest(yaml_file)
            dag_id = manifest.get("dag_id", yaml_file.stem)

            output_file = OUTPUT_DIR / f"{dag_id}.json"

            if dry_run:
                print(f"  [DRY-RUN] Would write: {output_file}")
            else:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(manifest, f, indent=2, ensure_ascii=False)
                print(f"  ✅ {yaml_file.name} → {output_file.name}")

        except Exception as e:
            print(f"  ❌ Failed to build {yaml_file.name}: {e}")
            sys.exit(1)

    print("\n🎉 Manifest build completed successfully.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build DAG manifests from YAML")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing files",
    )
    args = parser.parse_args()

    build_all_manifests(dry_run=args.dry_run)