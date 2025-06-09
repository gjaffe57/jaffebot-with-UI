import re
import logging
import json as pyjson
from typing import Optional
from logging import Formatter

class PIIRedactionFormatter(Formatter):
    """Custom formatter that redacts PII from log messages."""
    PII_PATTERNS = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}',
        'phone': r'\\b\\d{3}[-.]?\\d{3}[-.]?\\d{4}\\b',
        'ssn': r'\\b\\d{3}[-]?\\d{2}[-]?\\d{4}\\b',
        'credit_card': r'\\b\\d{4}[- ]?\\d{4}[- ]?\\d{4}[- ]?\\d{4}\\b',
        'ip_address': r'\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b',
        'api_key': r'(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)[=:]\\s*[\\w\\-\\.]+'
    }
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        super().__init__(fmt, datefmt)
        self.patterns = {k: re.compile(v) for k, v in self.PII_PATTERNS.items()}
    def format(self, record: logging.LogRecord) -> str:
        msg = record.getMessage()
        redacted_msg = self.redact_pii(msg)
        record.msg = redacted_msg
        if hasattr(record, 'args'):
            record.args = tuple(self.redact_pii(str(arg)) for arg in record.args)
        return super().format(record)
    def redact_pii(self, text: str) -> str:
        if not isinstance(text, str):
            return text
        redacted = text
        for pattern_name, pattern in self.patterns.items():
            redacted = pattern.sub(f'[REDACTED {pattern_name.upper()}]', redacted)
        return redacted

class PIIRedactionJSONFormatter(Formatter):
    """Custom JSON formatter that redacts PII from log messages."""
    PII_PATTERNS = PIIRedactionFormatter.PII_PATTERNS
    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        super().__init__(fmt, datefmt)
        self.patterns = {k: re.compile(v) for k, v in self.PII_PATTERNS.items()}
    def format(self, record: logging.LogRecord) -> str:
        msg = record.getMessage()
        redacted_msg = self.redact_pii(msg)
        log_record = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'logger': record.name,
            'message': redacted_msg,
        }
        # Optionally add extra fields
        if hasattr(record, 'extra') and isinstance(record.extra, dict):
            log_record.update(record.extra)
        return pyjson.dumps(log_record)
    def redact_pii(self, text: str) -> str:
        if not isinstance(text, str):
            return text
        redacted = text
        for pattern_name, pattern in self.patterns.items():
            redacted = pattern.sub(f'[REDACTED {pattern_name.upper()}]', redacted)
        return redacted

def setup_logging(
    level: int = logging.INFO,
    format_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_file: Optional[str] = None,
    json_format: bool = False
) -> None:
    if json_format:
        formatter = PIIRedactionJSONFormatter()
    else:
        formatter = PIIRedactionFormatter(format_str)
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = []
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name) 