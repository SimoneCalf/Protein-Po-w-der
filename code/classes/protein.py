from typing import List, Optional, Sequence, Set, Tuple
from functools import reduce
import numpy as np

from classes.amino import Amino, AminoBond


class Protein:
    """Represents a protein existing of a sequence of Amino acids.

    Attributes:
    -----------
    aminos: list[Amino]
        the list of amino acids that make up this protein
    """
    def __init__(self, string: str, directions: Sequence[int] = []):
        """Constructor method

        Parameters
        ----------
        string : str
            string representation of the Amino acid
        directions : list[int], optional
            representation of the directions this protein is folded,
            by default None
        """
        self.__aminos = []
        self.__grid = np.empty((len(string), len(string)), dtype=np.object_)

        # create amino instances for each char in string
        for i, char in enumerate(string):

            # create amino
            amino = Amino(
                type=char,
                direction=directions[i] if i < len(directions) else 0,
                index=len(self.__aminos),
                x=len(self.__aminos)
            )
            self.__aminos.append(amino)

        self.__populate_grid()

    @property
    def aminos(self) -> List[Amino]:
        """Getter function for the list of Amino acids in this Protein instance

        Returns
        -------
        list[Amino]
            A new list containing the current Amino acids of this instance
        """
        return self.__aminos.copy()

    def __populate_grid(self, index=0, in_place=False):
        """Populates a 2d grid representation of the protein

        The representation assumes the first amino is at [0, 0] and
        follows each aminos direction to place each item relative to the
        previous amino

        Parameters
        ----------
        index : int, optional
            the index of the point in a 1-dimensional array at which to start
            traversing directions, only makes sense to use when editing the
            grid in place. 0 by default.

        in_place : bool, optional
            whether to edit the current grid in-place,
            or whether to replace the grid with a new one.
            Default is False

        Raises
        ------
        IndexError
            Raises an IndexError when the given index is an invalid point in
            the 1 dimensional array
        """
        # Safeguard index overflow
        if index > len(self.__aminos):
            raise IndexError(
                "Given index '{}' is invalid; \
                must be a number between 0 and {}"
                .format(index, len(self.__aminos))
            )

        # use current array if in_place is set to true
        # otherwise create an empty 2d array
        grid = self.__grid if in_place and self.__grid is not None else \
            np.empty((self.__len__(), self.__len__()), dtype=np.object_)

        # if we're populating a completely empty array
        # then we're adding the aminos up to index at their given position,
        # otherwise, we leave any items BEFORE the index untouched
        if not in_place:
            for amino in self.__aminos[:index+1]:
                grid[amino.y, amino.x] = amino

        prev = self.__aminos[index]
        for amino in self.__aminos[index+1:]:
            # retrieve previous move_dir and coordinates

            # clear current position in grid
            if in_place:
                grid[amino.y, amino.x] = None

            amino.x, amino.y = Amino.get_coordinates_at(prev, prev.direction)
            grid[amino.y, amino.x] = amino
            prev = amino
        self.__grid = grid

    @property
    def grid(self) -> np.ndarray:
        """A grid representing this amino as-if in a 2d Array,
        with the x and y axis corrected to show the protein within bounds

        Returns
        -------
        numpy.ndarray:
            read-only 2d array, with the axis corrected to show the entire
            protein within bounds

        """
        # retrieve smallest x and y coords
        min_x, min_y = reduce(
            lambda a, b: (min(a[0], b[0]), min(a[1], b[1])),
            list(map(lambda a: (a.x, a.y), self.__aminos))
        )

        # correct grid representation
        return np.roll(
            self.__grid,
            (min(min_y, 0) * -1, min(min_x, 0) * -1),
            (0, 1)
        )

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
        amino.index = len(self.__aminos)
        self.__aminos.append(amino)
        self.calculate_bonds(self.__aminos[amino.index:])
        self.__populate_grid(amino.index)
        return self.aminos

    def foldoptions(self, amino):
        if amino.index == 0:
            return [1]
        elif amino.index == 1:
            return [1, 2]

        prev = self.__aminos[amino.index-1] if amino.index > 0 else None
        folds = [1, 2, -2, -1]

        if prev:
            folds.remove(prev.direction * -1)

        return folds

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
            self.__aminos[index].direction = direction
            self.calculate_bonds(self.__aminos[index:])
            self.__populate_grid()

            return self.aminos
        except IndexError:
            return None

    def empty_coordinate(self, amino, direction) -> bool:
        x, y = amino.get_coordinates_at(amino, direction)
        return self.__grid[y, x] is None

    def calculate_bonds(self, aminos: Sequence) -> Set[Tuple[Amino]]:
        bonds = []

        # loop through given list of aminos
        for amino in aminos:
            # don't process P aminos, aminos that already have a bond
            # or the last amino
            # (if it has a bond, that will have already been processed)
            # and the 0 direction messes things up
            if amino.type == "P" or amino.direction == 0:
                continue

            # get the directions to check
            # and remove directions of the neighbours
            directions = self.foldoptions(amino)
            directions.remove(amino.direction)
            prev = self.__aminos[amino.index-1] if amino.index > 0 else None
            if prev and (prev.direction * -1) in directions:
                directions.remove(prev.direction * -1)

            # loop through the remaining valid directions
            for direction in directions:
                # retrieve absolute coordinates at directions
                x, y = Amino.get_coordinates_at(amino, direction)
                # then, if the there's an amino at the coordinates
                # that isn't a P amino...
                if not self.empty_coordinate(amino, direction) and \
                        self.__grid[y, x].type != "P":
                    # set the bonded property of each respective
                    # amino to their opposite, and add it the the set
                    amino.bonded.add(self.__grid[y, x])
                    self.__grid[y, x].bonded.add(amino)
                    bond = AminoBond(amino, self.__grid[y, x])
                    if bond not in bonds:
                        bonds.append(AminoBond(amino, self.__grid[y, x]))
        return bonds

    @property
    def score(self) -> int:
        """Returns the score of this protein

        Returns
        -------
        int
            the score of this protein, the smaller the better
        """
        score = 0

        # retrieve and loop through bonds
        for bond in self.calculate_bonds(self.__aminos):
            if bond.origin.type == bond.target.type and \
                    bond.origin.type == "H":
                score -= 1
            elif bond.origin.type == bond.target.type and \
                    bond.origin.type == "C":
                score -= 5
            elif bond.origin.type != "P" and bond.target.type != "P":
                score -= 1

        return score

    def __len__(self) -> int:
        """Returns the length of this protein

        Returns
        -------
        int
            the total amount of amino acids in this protein
        """
        return len(self.__aminos)

    def __str__(self) -> str:
        """Represents this Protein instance as a string

        Returns
        -------
        str
            a string representation of this protein, as a list of amino acids
        """
        return "[%s]" % (", ".join(map(lambda amino: str(amino), self.aminos)))
