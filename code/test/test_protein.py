import numpy as np
import pickle
from tempfile import TemporaryFile
import unittest

from classes.amino import Amino
from classes.protein import Protein

TYPES = "HHPHPPPPH"
DIRECTION = (1, 2, -1, -1, 2, 2, 1, -2, 0)
SCORE = -2


class ProteinTest(unittest.TestCase):
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
        """constructor method

        Parameters
        ----------
        methodName : str, optional
            see unittest module, by default ...
        """
        self.prot1 = Protein(TYPES, DIRECTION)
        self.prot2 = Protein(TYPES)
        super().__init__(methodName)

    def test_protein_creation(self):
        """Method that tests protein creation"""
        self.assertIsInstance(self.prot1, Protein)
        self.assertEqual(len(TYPES), len(self.prot1))
        self.assertEqual(len(DIRECTION), len(self.prot1))
        self.assertEqual(TYPES, self.prot1.types)
        self.assertEqual(DIRECTION, self.prot1.directions)

    def test_protein_aminos(self):
        self.assertEqual(self.prot1.aminos, instanceof(tuple))
        self.assertIsInstance(self.prot2.aminos[0], Amino)

    def test_protein_score(self):
        """Method that tests the protein score @property"""
        self.assertEqual(self.prot1.score, SCORE)

    def test_protein_grid(self):
        """Method that tests the protein grid @property"""
        self.assertIsInstance(self.prot1.grid, np.ndarray)
        self.assertEqual(
           self.prot1.grid.shape,
           (len(self.prot1), len(self.prot1))
        )

    def test_protein_validate(self):
        """Method that tests the protein validate method"""
        self.assertTrue(Protein.validate(self.prot1))
        self.assertFalse(Protein.validate(self.prot2))
        self.assertEqual(self.prot1.is_valid, Protein.validate(self.prot1))

    def test_protein_hash(self):
        """Method that tests protein hash euqality"""
        self.assertNotEqual(self.prot1, self.prot2)
        prot3 = Protein.copy(self.prot1)
        self.assertEqual(self.prot1, prot3)
        self.assertEqual(hash(self.prot1), hash(prot3))

    def test_pickle_protein(self):
        """Method that tests pickeling a protein"""
        pickle_result = None
        with TemporaryFile() as fp:
            pickle.dump(self.prot1, fp)
            fp.seek(0)
            pickle_result = pickle.load(fp)

        self.assertIsInstance(pickle_result, Protein)
        self.assertEqual(pickle_result.types, self.prot1.types)
        self.assertEqual(pickle_result.directions, self.prot1.directions)
        self.assertEqual(pickle_result, self.prot1)


if __name__ == "__main__":
    unittest.main()
