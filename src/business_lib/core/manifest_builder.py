# =============================================================================
# src/business_lib/core/manifest_builder.py
# Core logic for converting human-friendly YAML manifests into the
# final structure expected by create_dag_from_manifest()
# =============================================================================

import os
import re
from pathlib import Path
from typing import Any, Dict

import yaml


def _substitute_env_vars(value: Any) -> Any:
    """Recursively replace ${VAR} or $VAR with environment variables."""
    if isinstance(value, str):
        # Match ${VAR} or $VAR
        pattern = r"\$\{([^}]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)"
        def replacer(match):
            var_name = match.group(1) or match.group(2)
            return os.getenv(var_name, match.group(0))  # fallback to original if not found
        return re.sub(pattern, replacer, value)
    elif isinstance(value, dict):
        return {k: _substitute_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_substitute_env_vars(item) for item in value]
    return value


def load_yaml_manifest(yaml_path: Path) -> Dict[str, Any]:
    """Load a YAML manifest file and return it as a dictionary."""
    if not yaml_path.exists():
        raise FileNotFoundError(f"Manifest file not found: {yaml_path}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Manifest file must contain a YAML mapping: {yaml_path}")

    # Substitute environment variables
    return _substitute_env_vars(data)


def build_manifest(yaml_path: Path) -> Dict[str, Any]:
    """
    Convert a source YAML manifest into the final dictionary that will be
    consumed by create_dag_from_manifest() in dags/dag_factory.py.
    """
    raw = load_yaml_manifest(yaml_path)
    return raw