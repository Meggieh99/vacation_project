import unittest

def test_all() -> None:
    """
    Discover and run all test modules in the current package.
    """
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
