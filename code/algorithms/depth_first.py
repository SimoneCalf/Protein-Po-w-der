from collections import deque
from typing import Union

from classes.protein import Protein
from algorithms.BaseAlgorithm import BaseAlgorithm


class DepthFirstFold(BaseAlgorithm):
    """
    DepthFirstFold is an algorithm that explores a Protein's entire state space
    of possible folds in order to find the most stable solution.

    Exploring the entire state space garuantees that it will find the optimal
    solution, but this also means that it takes a very long time

    Methods
    -------
    run(verbose=False):
        starts the algorithm

    """
    def __init__(self, prot: Union[str, Protein]) -> None:
        """Creates a DepthFirstFold instance

        Parameters
        ----------
        prot : Union[str, Protein]
            the protein to fold

        Raises
        ------
        TypeError
            raises a TypeError when the given protein is neither a Protein
            instance nor a string which can be interpreted into a protein
        """
        super().__init__(prot)

        # create stack, and add root protein to it
        self.__stack = deque()
        self.__stack.append(self.protein)

    def run(self, verbose=False):
        """Runs the main algorithm
        """
        self.verbose = verbose
        count = 0

        # loop door de stack
        while self.__stack:
            curr = self.__stack.pop()
            curr_amino = curr.next_uninitialized()

            # er zijn geen ongeinitieerde aminos meer,
            # we hebben een oplossing
            if curr_amino is None:
                count += 1
                self.log(f"found {count} solutions", start=True)

                if self.best is None or curr.score <= self.best.score:
                    self.best = curr
                continue

            else:
                # loop door de mogelijke richtingen
                for direction in curr.foldoptions(curr_amino):
                    if curr.empty_coordinate(curr_amino, direction):
                        # voor elke geldige oplossing, maken we een kopie
                        # en vouwen we die kopie de huidige richting in
                        nxt_prot = Protein.copy(curr)
                        nxt_prot.fold(curr_amino.index, direction)

                        # vervolgens stoppen we die bovenop de stack
                        self.__stack.append(nxt_prot)
                    else:
                        # als er geen geldige richtingen zijn gaan we door
                        # naar de volgende eiwit-mogelijkheid in de stack
                        continue

        self.log(f"Best solution: {self.best.score}", end=True)
        return self.best
