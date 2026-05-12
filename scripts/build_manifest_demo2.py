import yaml
import json
import importlib
from pathlib import Path


class ManifestFactory:
    def __init__(self, config_path: str, output_path: str):
        self.config_path = Path(config_path)
        self.output_path = Path(output_path)

    def validate_module(self, module_path: str, attr_name: str):
        """Check if the Python code actually exists before generating JSON."""
        try:
            module = importlib.import_module(module_path)
            if not hasattr(module, attr_name):
                raise AttributeError(f"Module '{module_path}' has no attribute '{attr_name}'")
            return True
        except ImportError:
            print(f"❌ ERROR: Cannot find module {module_path}")
            return False

    def build(self):
        print(f"🚀 Building manifest from {self.config_path}...")

        with open(self.config_path, "r") as f:
            data = yaml.safe_load(f)

        # 1. Logic Validation
        for step in data.get("workflow", []):
            mod = step["business_module"]
            func = step["business_function"]
            if not self.validate_module(mod, func):
                raise Exception(f"Validation failed for step: {step['id']}")

        # 2. Resource Validation
        for res_name, res_cfg in data.get("resources", {}).items():
            # Extract 'infrastructure.adapters.RedisAdapter' -> 'infrastructure.adapters', 'RedisAdapter'
            parts = res_cfg["type"].rsplit(".", 1)
            if not self.validate_module(parts[0], parts[1]):
                raise Exception(f"Validation failed for resource: {res_name}")

        # 3. Export to JSON for Airflow
        with open(self.output_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"✅ Success! Manifest saved to {self.output_path}")


if __name__ == "__main__":
    # In a real CI/CD, these would be arguments
    factory = ManifestFactory("config/workflows/onboarding.yaml", "dags/manifests/onboarding.json")
    factory.build()
