import os
import django
import db_config
from vacations.tests.runner import test_all


db_config.USE_TEST_DB = True  # Switch to test_db before loading Django settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


if __name__ == "__main__":
    """
    Entry point for running all tests through main.py.
    This will apply migrations, load initial data, and execute all test cases.
    """
    test_all()
