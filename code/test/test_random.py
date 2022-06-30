import unittest

from algorithms.random_protein import fold_randomly
from classes.protein import Protein


class RandomTest(unittest.TestCase):
    """Unit tests for the Amino class

    Parameters
    ----------
    TestCase :
        unittest superclass needed for unittest;
`
    See Also
    --------
    `unittest module <https://docs.python.org/3/library/unittest.html#unittest.main>`_:
        for more information about the methods used here
    """
    def __init__(self, methodName: str = ...) -> None:
        """Constructor method

        Parameters
        ----------
        methodName : str, optional
            see unittest module, by default ...
        """
        super().__init__(methodName)
        self.test_prot = Protein(
            "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH",
        )

    def test_fold_randomly(self):
        """Method that tests whehter the algorithm folds properly"""
        prot1 = Protein.copy(self.test_prot)
        prot2 = Protein.copy(self.test_prot)
        self.assertIsInstance(prot1, Protein)
        self.assertIsInstance(prot2, Protein)
        fold_randomly(prot1, prot1.aminos[0])
        fold_randomly(prot2, prot2.aminos[0])
        self.assertIsInstance(prot1, Protein)
        self.assertIsInstance(prot2, Protein)
        self.assertTrue(Protein.validate(prot1))
        self.assertTrue(Protein.validate(prot1))
        self.assertNotEqual(prot1, prot2)


if __name__ == "__main__":
    unittest.main()
