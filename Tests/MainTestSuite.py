import unittest

from Tests import FirstLoopTests

suite = unittest.TestLoader().loadTestsFromModule(FirstLoopTests)
unittest.TextTestRunner(verbosity=2).run(suite)
