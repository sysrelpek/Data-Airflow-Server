"""
This is the "Smart Switch" that protects the store_data step.
If it is the primary storage, (e.g., Redis or a remote DB) fails,
it reroutes to your local fallback.
"""

import logging
from business_lib.domain.interfaces import StoragePort

class ResilientStorageWrapper(StoragePort):
    def __init__(self, primary: StoragePort, fallback: StoragePort, fail_limit: int = 3):
        self.primary = primary
        self.fallback = fallback
        self.fail_limit = fail_limit
        self.fails = 0
        self.circuit_open = False

    def save(self, entity_id: str, data: dict):
        if self.circuit_open:
            return self.fallback.save(entity_id, data)

        try:
            return self.primary.save(entity_id, data)
        except Exception as e:
            self.fails += 1
            logging.error(f"Primary Storage Failed ({self.fails}/{self.fail_limit}): {e}")
            if self.fails >= self.fail_limit:
                self.circuit_open = True
                logging.warning("!!! CIRCUIT BREAKER TRIPPED - Falling back to local storage !!!")
            return self.fallback.save(entity_id, data)

    def get_by_id(self, entity_id: str):
        # Always try primary first, fallback if breaker is open
        if self.circuit_open:
            return self.fallback.get_by_id(entity_id)
        return self.primary.get_by_id(entity_id)

    def get_pending_messages(self, limit: int = 50):
        return self.fallback.get_pending_messages(limit)
