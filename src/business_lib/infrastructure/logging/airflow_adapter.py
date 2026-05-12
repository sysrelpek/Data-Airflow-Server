"""
This adapter ensures that logs from your business logic show up in the Airflow UI logs.
"""
import logging
from business_lib.domain.interfaces import LoggingPort

class AirflowLoggerAdapter(LoggingPort):
    def info(self, message: str):
        logging.info(f"[CORE_INFO] {message}")

    def error(self, message: str, error_details=None):
        logging.error(f"[CORE_ERROR] {message} | Details: {error_details}")

    def verify(self, action: str, status: bool):
        symbol = "✅" if status else "❌"
        logging.info(f"[VERIFY] {symbol} {action}")
