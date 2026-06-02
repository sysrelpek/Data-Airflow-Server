# =============================================================================
# src/business_lib/core/manifest_builder.py
# Core logic for converting human-friendly YAML manifests into the
# final structure expected by create_dag_from_manifest()
# =============================================================================

from pathlib import Path
from typing import Any, Dict
import yaml


def load_yaml_manifest(yaml_path: Path) -> Dict[str, Any]:
    """
    Load a YAML manifest file and return it as a dictionary.
    This is the single place where we read YAML in the core.
    """
    if not yaml_path.exists():
        raise FileNotFoundError(f"Manifest file not found: {yaml_path}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Manifest file must contain a YAML mapping: {yaml_path}")

    return data


def build_manifest(yaml_path: Path) -> Dict[str, Any]:
    """
    Convert a source YAML manifest into the final dictionary that will be
    consumed by create_dag_from_manifest() in dags/dag_factory.py.

    This is where we can later add:
    - Schema validation (jsonschema / pydantic)
    - Environment variable substitution
    - Default values
    - Transformation / enrichment logic

    For now we keep it simple and mostly pass-through.
    """
    raw = load_yaml_manifest(yaml_path)

    # Future improvement area:
    # - Validate required fields (dag_id, workflow, resources)
    # - Resolve environment variables in config values
    # - Normalize schedule vs schedule_interval

    return raw