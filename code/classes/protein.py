from classes.amino import Amino
from .grid import Grid
from typing import Optional, List


class Protein:
    """Represents a protein existing of a sequence of Amino acids.

    Attributes:
    -----------
    aminos: list[Amino]
        the list of amino acids that make up this protein
    """
    def __init__(self, string: str, directions: List[int] = None):
        """Constructor method

        Parameters
        ----------
        string : str
            string representation of the Amino acid
        directions : list[int], optional
            representation of the directions this protein is folded,
            by default None
        """
        if directions is not None and len(directions) is len(string):
            self._aminos = list(map(self.create_amino, string, directions))
        else:
            self._aminos = list(map(self.create_amino, string))

        self.grid = Grid(len(string))
        self.set_previous()
        self.set_next()

    @property
    def aminos(self) -> List[Amino]:
        """Getter function for the list of Amino acids in this Protein instance

        Returns
        -------
        list[Amino]
            A new list containing the current Amino acids of this instance
        """
        return self._aminos.copy()

    def create_amino(self, letter: str, dir: int = 0):
        return Amino(letter, dir)

    def append(self, amino: Amino) -> List[Amino]:
        """Adds a new Amino Acid to this Protein instance

        Parameters
        ----------
        amino : Amino
            the new amino acid to append

        Returns
        -------
        list[Amino]
            a new list containing the amino acids that make up this protein,
            including the appended one
        """
        self._aminos.append(amino)
        return self.aminos

    def fold(self, index: int, direction: int) -> Optional[List[Amino]]:
        """Folds this protein in a given direction at a given point

        Parameters
        ----------
        index : int
            the point at which to fold this protein
        direction : int
            the direction to fold the protein in

        Returns
        -------
        Optional[list[Amino]]
            a new list containing the amino acids and their direction,
            or None if the given point was invalid
        """
        try:
            self._aminos[index].direction = direction
            if direction in [-1, 1]:
                self.aminos[index].x = self.aminos[index].previous.x + direction
                self.aminos[index].y = self.aminos[index].previous.y
            else:
                self.aminos[index].x = self.aminos[index].previous.x
                self.aminos[index].y = self.aminos[index].previous.y + direction
            return self.aminos
        except IndexError:
            return None

    def set_previous(self):
        self.aminos[0].previous = None

        i = 0
        for amino in self.aminos[1:]:
            amino.previous = self.aminos[i]
            i += 1

    def set_next(self):
        self.aminos[-1].next = None

        i = 1
        for amino in self.aminos[:-1]:
            amino.next = self.aminos[i]
            i += 1

    def place_in_grid(self, amino):
        self.grid.grid[amino.y][amino.x] = amino

    def calc_score(self):
        pass

    def __len__(self) -> int:
        """Returns the length of this protein

        Returns
        -------
        int
            the total amount of amino acids in this protein
        """
        return len(self.aminos)

    def __str__(self) -> str:
        """Represents this Protein instance as a string

        Returns
        -------
        str
            a string representation of this protein, as a list of amino acids
        """
        return "[%s]" % (", ".join(map(lambda amino: str(amino), self.aminos)))
