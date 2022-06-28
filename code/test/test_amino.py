import pickle
from tempfile import TemporaryFile
from unittest import TestCase

from classes.amino import Amino


class AminoTest(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.a1 = Amino("H", -1)
        self.a2 = Amino("H", -1)

    def test_amino_equality(self):
        self.assertTrue(self.a1 == self.a2)

    def test_amino_type(self):
        self.assertEqual(self.a1.type, "H")

    def test_amino_direcitons(self):
        self.assertEquals(self.a1.direction, self.a1._direction)
        self.assertEquals(self.a2.direction, self.a2._direction)
        # test setter
        self.a1.direction = -2
        self.assertEquals(self.a1.direction, -2)

    def test_pickle_amino(self):
        unpickled_a1 = None
        with TemporaryFile() as fp:
            pickle.dump(self.a1, fp)
            fp.seek(0)
            unpickled_a1 = pickle.load(fp)

        self.assertEqual(unpickled_a1, self.a1)
        self.assertEqual(hash(unpickled_a1), hash(self.a1))
        self.assertNotEqual(id(unpickled_a1), id(self.a1))
