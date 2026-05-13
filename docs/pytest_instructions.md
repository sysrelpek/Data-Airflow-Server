```
pytest tests -q
```

---

Example to test invidual testfunction in a test_file:
```
pytest tests/test_ingest_pipeline.py::test_full_yaml_flow_locally -q
```