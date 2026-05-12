## Data Airflow Server Project Structure   (   Next Gen Hexagonal MLOps )
```
my_project/
├── .env                               # Environment Identity (ENV=dev/prod, API keys) - [Git-ignored]
├── .env.dev                           # Development environment variables
├── .env.prod                          # Production environment variables
├── .gitignore                         # Git ignore file
│  
├── config/                            # CONFIG LAYER (Strategy & Topology)
│   ├── envs/                          # Infrastructure Overlays (Injection)
│   │   ├── dev_resources.yaml         # ToDo: CREATE - Local adapters (FileStorage, SQLite)
│   │   └── prod_resources.yaml        # ToDo: CREATE - Production adapters (Postgres, Redis)
│   ├── base_resources.yaml            # ToDo: CREATE - Common resource settings
│   └── workflows/                     # Business Logic Flows (YAML Blueprints)
│       └── ingest_pipeline.yaml       # Defines steps, parameters & dependencies
│
├── dags/                              # AIRFLOW LAYER (Orchestration)
│   ├── dag_factory.py                 # THE ENGINE: Reads JSON and creates DAGs in memory
│   ├── outbox_relay_worker.py         # THE COURIER: Syncs local Outbox to central server
│   └── manifests/                     # Manifests (JSON): Generated blueprints for Airflow
│       └── ingest_pipeline_dev.json   # Development manifest for ingest pipeline
│
├── doc/                               # Documentation
│   ├── proj_info.md                   # Project info and overview
│   ├── proj_tree.md                   # Project directory structure and file organization
│   ├── proj_file_head_template.txt    # Code files header template    
│   └── proj_file_info.yaml            # Project file info and details
│
├── local_db/                          # Local storage for Dev runs (JSON files)
│
├── scripts/                           # SYSTEM BUILD LAYER
│   └── build_manifest.py              # THE FACTORY: Validates code & builds JSON from YAML
│
├── scripts_dev/                       # DEVELOPMENT SETUP AND ADMINISTRATION
│   ├── sysnc_to_server                # Synchronize project files from dev to prod 
│   └── Makefile                       # Creates short command to help the development process
│
├── scripts_prod/                      # SERVER SETUP AND ADMINISTRATION (NOT SYSTEM BUILD)
│   ├── admin/
│   │   ├── build_dags.sh                 # ToDo: UPDATE - check paths
│   │   ├── restart_airflow_services.sh   # ToDo: UPDATE - check paths
│   │   ├── run.sh                        # ToDo: UPDATE - check paths
│   │   ├── run_airflow_service.sh        # ToDo: UPDATE - check paths
│   │   ├── run_debug.sh                  # ToDo: UPDATE - check paths
│   │   └── stop_airflow_service.sh       # ToDo: UPDATE - check paths
│   │
│   └── setup/
│       ├── Makefile                                           # Creates short command to control the administartion
│       ├── create_and_setup_airflow_service.sh                # Creates service, start servie and check servide state
│       ├── create_and_setup_airflow_scheduler_service.sh      # Creates service, start servie and check servide state
│       └── create_and_setup_airflow_api_service.sh            # Creates service, start servie and check servide state
│
│
├── src/                               # BUSINESS LIBRARY (The Core Hexagon)
│   └── business_lib/
│       ├── core/                      # Configuration & Pydantic settings
│       │   └── config.py              # ToDo: UPDATE - Reads .env and handles environment variables
│       │
│       ├── domain/                    # PORTS (Interfaces) & MODELS
│       │   ├── interfaces.py          # ABC classes (StoragePort, CachePort, EventPort)
│       │   └── models.py              # ToDo: CREATE - Pydantic models for data validation
│       │
│       ├── services/                  # BUSINESS PROCESSES (Business Logic)
│       │   ├── ingest/                # e.g., feature_ingest.py (Collect/Clean/Transform)
│       │   └── finance/               # e.g., onboarding.py
│       │
│       └── infrastructure/            # ADAPTERS (Technical Implementation)
│           ├── storage/               # Storage adapters
│           │   ├── file_adapter.py    # PostgresAdapter 
│           │   └── postgres_adapter.py# FileStorageAdapter
│           │
│           ├── messaging/             # RedisAdapter, ApiAdapter
│           │
│           ├── logging/               # LoggingAdapters
│           │   └── airflow_adapter.py
│           │
│           └── resilience.py          # (Smart Switch) change the primary storage temporarily if a data-step fails.
│
│   
├── tests/                       # TEST LAYER (Hexagon Outside - Test Adapters)
│   ├── test_ingest_pipeline.py  # ToDo - Test - Verifies business flows locally
│   └── test_factory.py          # ToDo - Verifies that YAML -> JSON works correctly
│
├── README.txt                          # ToDo - GitHub project fron page info
└── requirements.txt                    # Project dependencies and requirements
```

