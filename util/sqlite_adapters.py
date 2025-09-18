import sqlite3
from datetime import datetime

def adapt_datetime(dt):
    """Adaptador para converter datetime para string ISO"""
    return dt.isoformat()

def convert_datetime(s):
    """Conversor para converter string ISO de volta para datetime"""
    return datetime.fromisoformat(s.decode())

def register_adapters():
    """Registra os adaptadores customizados para datetime no sqlite3"""
    sqlite3.register_adapter(datetime, adapt_datetime)
    sqlite3.register_converter("TIMESTAMP", convert_datetime)