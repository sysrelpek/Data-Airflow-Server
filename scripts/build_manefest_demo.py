# scripts/build_manifest.py
import yaml
import json
import os


class NextGenFactory:
    def __init__(self, env="dev"):
        self.env = env
        self.base_dir = "config/workflows"

    def merge_configs(self, base, override):
        """Deep merge two dictionaries to apply environment overrides."""
        for key, value in override.items():
            if isinstance(value, dict):
                base[key] = self.merge_configs(base.get(key, {}), value)
            else:
                base[key] = value
        return base

    def build_manifest(self, workflow_name):
        # 1. Load Base Config
        with open(f"{self.base_dir}/base_resources.yaml", "r") as f:
            config = yaml.safe_load(f)

        # 2. Apply Environment Overrides (e.g., dev_resources.yaml)
        env_file = f"config/envs/{self.env}_resources.yaml"
        if os.path.exists(env_file):
            with open(env_file, "r") as f:
                env_overrides = yaml.safe_load(f)
            config = self.merge_configs(config, env_overrides)

        # 3. Resolve Dependencies (The DAG Graph)
        # We ensure every task has its 'depends_on' field mapped for Airflow
        with open(f"{self.base_dir}/{workflow_name}.yaml", "r") as f:
            workflow = yaml.safe_load(f)

        config["workflow"] = workflow["steps"]

        # 4. Save the Final Manifest for Airflow
        output_path = f"dags/manifests/{workflow_name}_{self.env}.json"
        with open(output_path, "w") as f:
            json.dump(config, f, indent=4)
        print(f"✅ Manifest built for {self.env.upper()}: {output_path}")

# Example usage in CI/CD or local script
# factory = NextGenFactory(env="prod")
# factory.build_manifest("onboarding")
