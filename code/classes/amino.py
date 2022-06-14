from typing import Optional


class Amino:
    """Represents a single amino Acid.

    Attributes
    ----------
    letter: str
        the type of amino acid, represented by a single characters
    direction:
        the direction the amino acid is folded, represented as a number between
        -2 and +2
    """
    def __init__(self, letter: str, direction: int = 0):
        """Constructor method

        Parameters
        ----------
        letter : str
            the type of this amino acid, represented by a single letter
        direction : int, optional
            the direction this amino acid is folded, by default 0
        """
        self.letter = letter
        self._direction = direction
        self.x = 0
        self.y = 0
        self.previous = 0
        self.next = 0

    @property
    def direction(self) -> int:
        return self._direction

    @direction.setter
    def set_direction(self, dir: int) -> Optional[int]:
        if dir not in range(-2, 2):
            return None

        self._direction = dir
        return self.direction

    def __str__(self):
        """Represents this amino acid as a string."""
        return "{{ {}: {:+} }}".format(self.letter, self.direction)
