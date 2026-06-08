#!/usr/bin/env python3
"""
Build all JSON manifests from YAML config files in dags/configs/.

This script uses manifest_builder.py to convert every .yaml/.yml file
into a corresponding .json file in dags/manifests/.

Usage:
    python -m business_lib.core.build_all_manifests
"""

from pathlib import Path
from typing import List
import json
from datetime import datetime, timezone

# Import from our own core module
from business_lib.core.manifest_builder import build_manifest


def build_all_manifests(
    configs_dir: Path = Path("dags/configs"),
    manifests_dir: Path = Path("dags/manifests"),
) -> List[Path]:
    """
    Convert all YAML files in configs_dir into JSON manifests.
    """
    configs_dir = Path(configs_dir).resolve()
    manifests_dir = Path(manifests_dir).resolve()
    manifests_dir.mkdir(parents=True, exist_ok=True)

    yaml_files = sorted(
        list(configs_dir.glob("*.yaml")) + list(configs_dir.glob("*.yml"))
    )

    if not yaml_files:
        print(f"No YAML config files found in {configs_dir}")
        return []

    created_files: List[Path] = []

    print(f"Building manifests from {len(yaml_files)} YAML file(s)...")

    for yaml_file in yaml_files:
        try:
            manifest_dict = build_manifest(yaml_file)

            # Add metadata
            manifest_dict = {
                "_meta": {
                    "source_file": str(yaml_file.name),
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "generated_by": "build_all_manifests.py",
                    "version": "1.0"
                },
                **manifest_dict  # original manifest data comes after metadata
            }

            json_file = manifests_dir / (yaml_file.stem + ".json")

            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(manifest_dict, f, indent=2, ensure_ascii=False)

            created_files.append(json_file)
            print(f"  ✓ {yaml_file.name} → {json_file.name}")

        except Exception as e:
            print(f"  ✗ Failed to build {yaml_file.name}: {e}")

    print(f"\nDone. Created/updated {len(created_files)} manifest(s).")
    return created_files


if __name__ == "__main__":
    build_all_manifests()