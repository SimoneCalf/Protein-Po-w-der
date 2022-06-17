import typing


class Amino:
    """Represents a single amino Acid.

    Attributes
    ----------
    type: str
        the type of amino acid, represented by a single characters
    direction: int
        the direction the amino acid is folded, represented as a number between
        -2 and +2
    x: int
        the absolute x coordinate of this amino
    y: int
        the absolute y coordinate of this amino
    prev_amino: int
        the previous amino in a sequence of aminos
    next_amino: int
        the next amino in a sequence of aminos
    """

    def __init__(
            self,
            type: str,
            direction: int = 0,
            coords: typing.Sequence = (0, 0, 0),
            x: int = 0,
            y: int = 0,
            z: int = 0,
            index: int = 0) -> None:
        """Constructor method

        Parameters
        ----------
        letter : str
            the type of amino represented by a single character,
            valid types are "C", "H", "P"
        direction : int, optional
            the direction the amino is pointing, relative to the previous node,
            must be an integer between -2 and 3 by default 0
        coords : sequence, optional
            represents the absolute coordinates of this amino,
            as if in a 3d grid. by default (0, 0, 0)
        x: int, optional
            alternative way to pass the absolute x coordinate of this amino
        y: int, optional
            alternative way to pass the absolute y coordinate of this amino
        z: int, optional
            alternative way to pass the absolute y coordinate of this amino,
            ignored if not given
        index:
            the postion of this amino as if in a 1d grid. by default 0


        Raises
        ------
        ValueError
            raises ValueError when the given direction is not in the range of
            -2 to 3
        """
        if direction not in range(-2, 3):
            raise ValueError(
                "Given direction is not valid. \
                 Must be an interger between -2 and 2"
            )

        self.type = type
        self._direction = direction
        self.x = x if x != 0 or len(coords) < 1 else coords[0]
        self.y = y if y != 0 or len(coords) < 2 else coords[1]
        self.z = z if z != 0 or len(coords) < 3 else coords[2]
        self.index = index

    @property
    def direction(self) -> int:
        return self._direction

    @direction.setter
    def direction(self, dir: int) -> int:
        if dir not in range(-2, 3):
            raise ValueError(
                "Given direction is not valid. \
                Must be an interger between -2 and 2"
            )

        self._direction = dir
        return self._direction

    

    
    
    def foldoptions(self) -> list:
        if self._direction == 0:
            return [1, 2]
        options = [-2, 2, -1, 1]
        options.remove(self._direction * -1)
        return options

    def __repr__(self):
        """Represents this amino acid as a string."""
        return "( {}{}: {:+} )".format(self.type, self.index, self.direction)
