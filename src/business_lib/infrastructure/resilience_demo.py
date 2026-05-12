# src/business_lib/infrastructure/resilience_demo.py

class ResilientStorageWrapper:
    def __init__(self, primary, fallback, limit=5):
        self.primary = primary  # e.g., RedisAdapter
        self.fallback = fallback  # e.g., PostgresAdapter
        self.fail_count = 0
        self.limit = limit
        self.is_open = False  # The "Breaker" state

    def save_customer(self, customer_id, data):
        # If the breaker is "open" (tripped), go straight to fallback
        if self.is_open:
            return self.fallback.save_customer(customer_id, data)

        try:
            return self.primary.save_customer(customer_id, data)
        except Exception as e:
            self.fail_count += 1
            print(f"Primary storage failed ({self.fail_count}/{self.limit}): {e}")

            if self.fail_count >= self.limit:
                self.is_open = True
                print("!!! CIRCUIT BREAKER TRIPPED - Switching to Fallback !!!")

            # Immediate fallback for this specific call
            return self.fallback.save_customer(customer_id, data)
