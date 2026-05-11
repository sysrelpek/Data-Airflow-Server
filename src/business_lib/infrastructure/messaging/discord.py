# src/business_lib/infrastructure/messaging/discord.py

class DiscordLoggerAdapter(LoggingPort):
    def __init__(self, webhook_url: str, env: str, task_context: dict = None, grok_mode: bool = True):
        self.webhook_url = webhook_url
        self.env = env
        self.context = task_context or {}
        self.grok_mode = grok_mode

    def _send_to_discord(self, content: str):
        # Dela upp i 2000-teckens bitar (Discord-gräns)
        chunks = [content[i:i + 1900] for i in range(0, len(content), 1900)]
        for chunk in chunks:
            payload = {"content": f"**[AI-DEBUG-STREAM]**\n```python\n{chunk}\n```"}
            requests.post(self.webhook_url, json=payload)

    def error(self, message: str, error_details=None):
        ctx = f"DAG: {self.context.get('dag_id')} | Task: {self.context.get('task_id')}"

        # Grundmeddelandet
        full_msg = f"❌ ERROR: {ctx}\nMSG: {message}\n"

        # GROK-MODE: Lägg till extra diagnostik
        if self.grok_mode:
            metadata = {
                "manifest_path": f"dags/manifests/{self.context.get('dag_id')}.json",
                "python_version": "3.10.x",
                "model_version": self.context.get('model_ver', 'v1.0'),
                "git_commit": self.context.get('commit_hash', 'unknown'),
                "suggestion": "Check the YAML depends_on logic or the StoragePort adapter."
            }
            full_msg += f"\n--- AI CONTEXT ---\n{json.dumps(metadata, indent=2)}\n"

        if error_details:
            full_msg += f"\nTRACEBACK:\n{str(error_details)}"

        self._send_to_discord(full_msg)
