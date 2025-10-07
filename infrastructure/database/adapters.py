"""
Adaptadores customizados para tipos Python/SQLite
"""
import sqlite3
from datetime import datetime


def adapt_datetime(dt: datetime) -> str:
    """Adaptador para converter datetime para string ISO"""
    return dt.isoformat()


def convert_datetime(s: bytes) -> datetime:
    """Conversor para converter string ISO de volta para datetime"""
    return datetime.fromisoformat(s.decode())


def register_adapters() -> None:
    """Registra os adaptadores customizados para datetime no sqlite3"""
    sqlite3.register_adapter(datetime, adapt_datetime)
    sqlite3.register_converter("TIMESTAMP", convert_datetime)
