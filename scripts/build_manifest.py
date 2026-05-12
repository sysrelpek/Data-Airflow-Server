
import yaml
import json
import os
from pathlib import Path

class ManifestFactory:
    def __init__(self, env="dev"):
        self.env = env
        self.base_path = Path(__file__).parent.parent
        self.config_dir = self.base_path / "config"
        self.output_dir = self.base_path / "dags" / "manifests"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _load_yaml(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def build(self, workflow_name):
        # 1. Ladda Workflow (Vad ska göras?)
        wf_path = self.config_dir / "workflows" / f"{workflow_name}.yaml"
        wf_data = self._load_yaml(wf_path)

        # 2. Ladda Miljö-resurser (Hur ska det lagras?)
        # Vi använder env-variabeln för att välja dev_resources eller prod_resources
        env_path = self.config_dir / "envs" / f"{self.env}_resources.yaml"
        res_data = self._load_yaml(env_path)

        # 3. Slå ihop till ett Manifest
        manifest = {
            "dag_id": f"{wf_data['dag_id']}_{self.env}",
            "resources": res_data["resources"],
            "workflow": wf_data["steps"]
        }

        # 4. Spara som JSON (Airflow-vänligt format)
        output_file = self.output_dir / f"{workflow_name}_{self.env}.json"
        with open(output_file, "w") as f:
            json.dump(manifest, f, indent=4)

        return output_file


if __name__ == "__main__":
    # Hämtar ENV från systemet, defaultar till dev
    environment = os.getenv("ENV", "dev")
    factory = ManifestFactory(env=environment)
    factory.build("ingest_pipeline")
