from typing import Optional, Sequence, List
import numpy as np

from classes.amino import Amino


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
        self.grid = np.empty((len(string), len(string)), dtype=np.object_)

        # create amino instances for each char in string
        for index, char in enumerate(string):
            amino = Amino(
                type=char,
                direction=directions[index] if index < len(directions) else 1,
                index=len(self.__aminos),
                x=len(self.__aminos)
            )
            self.__aminos.append(amino)

        #  move_dir = x = y = 0
        #  for amino in self._aminos:
        #      match move_dir:
        #          case -2:
        #              y += 1
        #          case -1:
        #              x = x-1 if x > 0 else 0
        #          case 1:
        #              x = x+1 if x < len(self.grid) else x
        #          case 2:
        #              y = y+1 if y < len(self.grid) else y
        #
        #      amino.x, amino.y = x, y
        #      self.place_in_grid(amino)
        #      move_dir = amino.direction

        self.populate_grid()

        #  self.set_previous()
        #  self.set_next()

    @property
    def aminos(self) -> List[Amino]:
        """Getter function for the list of Amino acids in this Protein instance

        Returns
        -------
        list[Amino]
            A new list containing the current Amino acids of this instance
        """
        return self.__aminos.copy()

    def populate_grid(self, index=0, in_place=False):
        """Populates a 2d grid representation of the protein

        The representation assumes the first amino is at [0, 0] and
        follows each aminos direction to place each item relative to the
        previous amino

        Parameters
        ----------
        index : int, optional
            the index of the point in a 1-dimensional array at which to start
            traversing directions, only makes sense to use when editing the grid
            in place. 0 by default.

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
        grid = self.grid if in_place and self.grid is not None else \
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
            move_dir, x, y = prev.direction, prev.x, prev.y

            # clear current position in grid
            if in_place:
                grid[amino.y, amino.x] = None

            # change coordinates based on the previous aminos direction
            if move_dir == -2:
                y -= 1
            elif move_dir == -1:
                x = x-1 if x > 0 else 0
            elif move_dir == 1:
                x = x+1 if x < len(grid) else x
            elif move_dir == 2:
                y = y+1 if y < len(grid) else y

            # insert amino at new(?) position in grid
            amino.x, amino.y = x, y
            grid[amino.y, amino.x] = amino
            prev = amino
        self.grid = grid

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
        self.populate_grid(amino.index)
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
            self.__aminos[index].direction = direction
            self.populate_grid(index, True)

            return self.aminos
        except IndexError:
            return None

    @property
    def score(self):
        pass

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
