import unittest
import numpy as np

from classes.protein import Protein

types = "HHPHPPPPH"
directions = (1, 2, -1, -1, 2, 2, 1, -2, 0)
score = -2


class ProteinTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.prot1 = Protein(types, directions)
        self.prot2 = Protein(types)
        super().__init__(methodName)


    def test_protein_creation(self):
        self.assertIsInstance(self.prot1, Protein)
        self.assertEqual(len(types), len(self.prot1))
        self.assertEqual(len(directions), len(self.prot1))
        self.assertEqual(types, self.prot1.types)
        self.assertEqual(directions, self.prot1.directions)

    def test_protein_score(self):
        self.assertEqual(self.prot1.score, score)

    def test_protein_grid(self):
        self.assertIsInstance(self.prot1.grid, np.ndarray)
        self.assertEqual(
           self.prot1.grid.shape,
           (len(self.prot1), len(self.prot1))
        )

    def test_protein_validate(self):
        self.assertTrue(Protein.validate(self.prot1))
        self.assertFalse(Protein.validate(self.prot2))


if __name__ == "__main__":
    unittest.main()
