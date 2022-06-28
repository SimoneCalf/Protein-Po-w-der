import sys
import unittest

from classes.protein import Protein
from algorithms.random_protein import fold_randomly
from visualization import visualize_protein


class RandomTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.test_prot = Protein(
            "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH",
        )

    def test_fold_randomly(self):
        prot1 = Protein.copy(self.test_prot)
        prot2 = Protein.copy(self.test_prot)
        self.assertIsInstance(prot1, Protein)
        self.assertIsInstance(prot2, Protein)
        fold_randomly(prot1, prot1.aminos[0])
        fold_randomly(prot2, prot2.aminos[0])
        self.assertIsInstance(prot1, Protein)
        self.assertIsInstance(prot2, Protein)
        self.assertTrue(Protein.is_valid(prot1))
        self.assertTrue(Protein.is_valid(prot1))

if __name__ == "__main__":
    unittest.main()
