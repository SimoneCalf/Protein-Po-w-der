from collections import deque
from typing import Union

from algorithms.BaseAlgorithm import BaseAlgorithm
from classes.protein import Protein


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

            # there are nu uninitiated aminos available
            # there is a solution
            if curr_amino is None:
                count += 1
                self.log(f"found {count} solutions", start=True)

                if self.best is None or curr.score <= self.best.score:
                    self.best = curr
                continue

            else:
                # loop through possible solutions
                for direction in curr.foldoptions(curr_amino):
                    if curr.empty_coordinate(curr_amino, direction):
                        # for each possible solution, there is a copy made
                        # the copy gets folded in the currenct direction
                        nxt_prot = Protein.copy(curr)
                        nxt_prot.fold(curr_amino.index, direction)

                        # the copy goes on top of the stack
                        self.__stack.append(nxt_prot)
                    else:
                        # if there are no valid direction we continue
                        # to the next protein-possibility in the stack
                        continue

        self.log(f"Best solution: {self.best.score}", end=True)
        return self.best
