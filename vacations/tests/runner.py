import unittest

def test_all() -> None:
    """
    Discover and run all tests in the 'tests' package.
    """
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
