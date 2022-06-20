from typing import Sequence, Tuple


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

    Static Methods
    --------------
    get_coordinates_at(amino=Amino, direction=1)
        Given an amino and a possible direction it will return the absolute
        coordinates of that direction relative to the amino

    """

    def __init__(
            self,
            type: str,
            direction: int = 0,
            coords: Sequence = (0, 0, 0),
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
        bonded: Amino, optional
            optional amino this amino forms a bond with. by default None


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

        self.type = type.upper()
        self._direction = direction
        self.x = x if x != 0 or len(coords) < 1 else coords[0]
        self.y = y if y != 0 or len(coords) < 2 else coords[1]
        self.z = z if z != 0 or len(coords) < 3 else coords[2]
        self.index = index
        self.bonded = set()

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

    @staticmethod
    def get_coordinates_at(amino, direction: int) -> Tuple[int, int]:
        """Returns the coordinates of a point a given direction away from a
        given Amino.

        Parameters
        ----------
        amino : Amino
            The amino to use at starting point
        direction : int
            the Direction from

        Returns
        -------
        tuple[int, int]
            a tuple returning two ints, representing the absolute coordinates,
            the first being the x-axis and the second the y-axis
        """
        x, y = amino.x, amino.y
        if direction == -2:
            y -= 1
        elif direction == -1:
            x -= 1
        elif direction == 1:
            x += 1
        elif direction == 2:
            y += 1
        else:
            pass

        return (x, y)

    def next(self) -> Tuple[int, int]:
        """Returns the absolute coordinates this amino's direction is pointing to

        Returns
        -------
        tuple[int, int]
            the x and y coordinates of the point this amino is pointing to
        """
        return Amino.get_coordinates_at(self, self.direction)

    def __repr__(self):
        """Represents this amino acid as a string."""
        return "( {}{}: {:+} )".format(self.type, self.index, self.direction)

    def __hash__(self) -> int:
        """Returns a unique hash for an Amino object

        Returns
        -------
        int
            a unique integer by which python can identify a specific Amino
            instance
        """
        return hash((
            self.type,
            self.index,
            self._direction,
            self.x,
            self.y,
            self.z
            ))


class AminoBond:
    """Represents a two-way bond between two aminos

    Attributes
    ----------
    origin: Amino
        the origin of the bond, since it's a two-way bond which amino is the
        origin is arbitrary, and does not matter for equality
    target: Amino
        the target of the bond, since it's a two-way bond which amino is the
        origin is arbitrary, and does not matter for equality

    """
    def __init__(self, origin: Amino, target: Amino) -> None:
        self.origin = origin
        self.target = target

    def __eq__(self, __o: object) -> bool:
        if type(__o) != type(self):
            return False
        if __o.origin != self.origin and __o.origin != self.target:
            return False

        if __o.target != self.target and __o.target != self.origin:
            return False

        if __o.target == __o.origin and self.target != self.origin:
            return False

        return True

    def __hash__(self) -> int:
        return hash((self.origin, self.target))

    def __repr__(self) -> str:
        return f"{self.origin.type}{self.origin.index}-" +\
            f"{self.target.type}{self.target.index}"
