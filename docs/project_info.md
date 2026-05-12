# Project Info - Data Airflow Server

----

----


### Explanation of the Components

### 1. The Core (The Inside)

* domain/interfaces.py (Ports): These are the system's "sockets." The logic only communicates through these. 
  They force all adapters (whether file-based or Postgres) to use the same methods (save, get_by_id).


* services/ (Logic): This is where the projects intelligence lives. 
  Thanks to the ports, this code is 100% portable. 
  It doesn't know if it's running on a laptop or in a cloud cluster.
 

* domain/models.py (Validation): Uses Pydantic to stop corrupted data (e.g., negative income or invalid email) 
  before it even reaches an adapter.


---
### 2. Infrastructure (The Outside)

* infrastructure/adapters/: This is where the "dirty" technology lives.


* PostgresAdapter: Contains your SQL logic.
   * FileStorageAdapter: Simulates a database locally using JSON files.


* resilience.py (Smart Switch): A Wrapper injected via the Factory. 
  If Redis goes down, this automatically switches the business logic to Postgres (Fallback) without the 
  logic crashing.


---
### 3. The Factory & Manifests (The Bridge)

* build_manifest.py: This is the "Compiler." It takes the human-readable YAML vision, checks that the Python code actually exists, 
  and outputs a technical JSON blueprint. It also handles Environment Overrides (switching between Dev and Prod).


* dag_factory.py: Airflow's "Runtime." It doesn't create files; it draws DAG objects in the Airflow UI based on the JSON blueprints. This makes the system extremely fast and scalable.


---
### 4. Synchronization (Next Gen Decentralization)

* Transactional Outbox: Every time an adapter saves data, it also saves a notice in a local "Outbox" table.
* outbox_relay_worker.py: An Airflow DAG that acts as a messenger. It clears the local Outbox and sends the 
  data to the central server as soon as the network allows.

-----

