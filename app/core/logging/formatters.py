"""
Custom logging formatters.
"""

import logging


class EnterpriseFormatter(logging.Formatter):
    """
    Human-readable formatter for local development.
    """

    def format(self, record: logging.LogRecord) -> str:
        record.request_id = getattr(record, "request_id", "-")
        record.method = getattr(record, "method", "-")
        record.path = getattr(record, "path", "-")
        record.status_code = getattr(record, "status_code", "-")
        record.duration_ms = getattr(record, "duration_ms", "-")
        record.client_ip = getattr(record, "client_ip", "-")

        return super().format(record)