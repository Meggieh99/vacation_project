# config.py
"""
Configuration file for managing database settings dynamically
based on whether the environment is for testing or production.
"""

USE_TEST_DB: bool = False
"""Set to True when running tests, to switch to test_db automatically."""

DB_NAME: str = "test_db" if USE_TEST_DB else "vacation_db"
DB_USER: str = "postgres"
DB_PASSWORD: str = "123456"
DB_HOST: str = "localhost"
DB_PORT: str = "5432"
