# Environments

This project uses three separate environment files:

| Environment | File         | Database          | Purpose                     | Loaded by                  |
|-------------|--------------|-------------------|-----------------------------|----------------------------|
| Development | `.env.dev`   | **SQLite (mock)** | Local development           | `scripts/dev/`             |
| Test        | `.env.test`  | **SQLite (mock)** | Testing / CI                | `scripts/test/`            |
| Production  | `.env.prod`  | **Postgres**      | Live Airflow server         | `scripts/prod/` + systemd  |

## How to use

```bash
cp .env.dev.example .env.dev     # (create example files later if missing)
cp .env.test.example .env.test
cp .env.prod.example .env.prod