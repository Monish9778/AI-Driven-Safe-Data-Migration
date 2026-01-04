import sqlite3
from config import SOURCE_DB, TARGET_DB

def get_source_db():
    return sqlite3.connect(SOURCE_DB)

def get_target_db():
    return sqlite3.connect(TARGET_DB)
