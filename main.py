import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from vacations.tests import test_all


if __name__ == "__main__":
    """
    Entry point for running all tests through main.py.
    This will apply migrations, load initial data, and execute all test cases.
    """
    test_all()
