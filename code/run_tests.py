#!/bin/env python


from test.test_amino import AminoTest  # noqa: F401,261
from test.test_protein import ProteinTest  # noqa: F401,261
from test.test_random import RandomTest  # noqa: F401,261
import unittest

if __name__ == "__main__":
    unittest.main(verbosity=2)
