from functools import reduce
from typing import Sequence, Tuple


def cantor_pair(a: int, b: int, deconstructable=False) -> Tuple[int, bool]:
    """
    Returns a cantor pairing number of two given numbers

    Parameters
    ----------
    a : int
        the first number
    b : int
        the second number

    Returns
    -------
    int
        a unique number identifying the pair of numbers in the specific order
        they were given

    See Also
    --------
    `Wikipedia
    <https://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function>`_:
        for the cantor pairing function
    """
    return (int((b+a)/2 * (a+b+1) + b), (a, b) >= (0, 0))


def cantor_str(input_str: str) -> int:
    # convert string to collection of utf-8 character codes and
    # reduce that collection to a cantor pair
    return reduce(cantor_pair, map(lambda i: ord(i), input_str))


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
        TypeError
            raises a TypeError when no type
        """
        if(type is None):
            raise TypeError("No type given")
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
        """Returns the direction of this amino

        Returns
        -------
        int
            the direction of this amino
        """
        return self._direction

    @direction.setter
    def direction(self, dir: int) -> int:
        """Sets the direction of this amino

        Parameters
        ----------
        dir : int
            the direction to set this to, must be between -2 to 2

        Returns
        -------
        int
            Returns the direction

        Raises
        ------
        ValueError
            Returns a ValueError when the given direction is not between
            a range of -2 to 2; as we only live in a 2d world
        """
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

    @staticmethod
    def copy(amino: 'Amino') -> 'Amino':
        """Copies the data of an amino into a new instance

        Parameters
        ----------
        amino : Amino
            the amino to copy

        Returns
        -------
        Amino
            a new amino intiated with the same values as the given aminos
        """
        return Amino(
            amino.type,
            direction=amino.direction,
            index=amino.index,
            coords=(amino.x, amino.y, amino.z)
        )



    def __eq__(self, obj: any) -> bool:
        """Compares object to this instance

        Parameters
        ----------
        obj : any
            the object to compare this instance to

        Returns
        -------
        bool
            True if both objects are functionally equal, False otherwise
        """
        if obj is None:
            return False

        # compare types
        if not isinstance(obj, Amino):
            return False

        # compare type and _direciton attributes
        if obj.type and obj.type != self.type or \
                obj.direction and obj.direction != self._direction:
            return False

        # compare coordinates
        if obj.x and obj.x != self.x or obj.y and obj.y != self.y \
                or obj.z and obj.z != self.z:
            return False

        # compare index
        if obj.index and obj.index != self.index:
            return False

        # compare bonds
        if obj.bonded and obj.bonded != self.bonded:
            return False

        return True

    def __hash__(self) -> int:
        """Returns a unique hash for an Amino object

        Returns
        -------
        int
            a unique integer by which python can identify a specific Amino
            instance by its values (works across instances)

        See Also
        --------
        `This Answer <https://stackoverflow.com/a/27522708/8571352>`_:
            on why hash values are different accross processes
        `cantor_str`:
            used to reliably return the same number given the same str
`        """
        # hash instance
        # we convert self.type to a cantor pair number in order to
        # avoid hash randomization across instances

        #
        # see: https://stackoverflow.com/a/27522708/8571352
        return hash((
            cantor_str(self.type),
            self.index,
            self._direction,
            self.x,
            self.y,
            self.z
        ))

    def __repr__(self):
        """Represents this amino acid as a string."""
        return "( {}{}: {:+} )".format(self.type, self.index, self.direction)


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
        """Constructor method for AminoBond

        Parameters
        ----------
        origin : Amino
            the origin amino of the bond; which is which does not matter
        target : Amino
            the target amino of this bond; whihc is which does not matter
        """
        if not isinstance(origin, Amino):
            raise TypeError(
                f"target parameter must be an Amino object; was {origin}"
            )
        if not isinstance(target, Amino):
            raise TypeError(
                f"target parameter must be an Amino object; was {target}"
            )

        self.origin = origin
        self.target = target

    def __eq__(self, __o: object) -> bool:
        """
        Checks if given object is equals this instance;
        used by 'is', '!==' and 'in' checks.

        which amino is the target and which amino is the origin is not relevant
        for this

        Parameters
        ----------
        __o : object
            the object to check against this instance

        Returns
        -------
        bool
            True if the given object equals this instance, False otherwise
        """
        if isinstance(__o, self.__class__):
            return False
        if __o.origin != self.origin and __o.origin != self.target:
            return False

        if __o.target != self.target and __o.target != self.origin:
            return False

        if __o.target == __o.origin and self.target != self.origin:
            return False

        return True

    def __hash__(self) -> int:
        """Creates a hash for easy dictionary and set lookup

        Returns
        -------
        int
            the hash of this amino
        """
        return hash((self.origin, self.target))

    def __repr__(self) -> str:
        """Representis this AminoBond as a string

        Returns
        -------
        str
            string of format 'H0-P1' where the first is the origin amino
            and the right is the target amino
        """
        return f"{self.origin.type}{self.origin.index}-" +\
            f"{self.target.type}{self.target.index}"
