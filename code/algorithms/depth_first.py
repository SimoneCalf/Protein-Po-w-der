from collections import deque
from typing import Union
import time
import threading
import sys


import os

p = os.path.abspath("code")
sys.path.insert(0, p)

from classes.protein import Protein # noqa E261
from visualization import visualize_protein # noqa E261
from input_output import output # noqa E261


class DepthFirstFold():
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
        # create protein from string if string was given
        if type(prot) == str:
            self.protein = Protein(prot)
        elif type(prot) == Protein:
            self.protein = prot
        else:
            raise TypeError(
                f"Unsupported type {type(prot)}," +
                f"must be of type '{str}' or '{Protein}'"
            )

        # create stack, and add root protein to it
        self.best = None
        self.prot_str = prot
        self.__stack = deque()
        self.__stack.append(self.protein)

        # logging nonsense
        self.__log = deque()
        self.__thread = None

    def log(self, msg: str, start: bool = False, end: bool = False):
        """Logs messages in a different thread

        Parameters
        ----------
        msg : str
            the message to log to stdout
        start : bool, optional
            whether to start the logger, by default False
        end : bool, optional
            whether to kill the logger, by default False
        """
        def loglisten(q):
            while True:
                if self.__log:
                    sys.stdout.flush()
                    print(self.__log.popleft(), end="\r")
                else:
                    break
                time.sleep(.05)

        # add message to the queue
        # start the thread if the parameter is given
        if start and self.__thread is None:
            self.__thread = threading.Thread(
                target=loglisten,
                daemon=True,
                args=(self.log,)
            )
            self.__thread.start()
        # stop if a thread exists and the flag was set
        if self.__thread is not None and end:
            self.__thread.join()
            self.__thread = None
            sys.stdout.write("\033[K\r")

            print(msg)
            return
        self.__log.append(msg)

    def run(self, verbose=False):
        """Runs the main algorithm
        """
        count = 0
        while self.__stack:
            curr = self.__stack.pop()
            curr_amino = curr.next_uninitialized()

            # laatste amino
            if curr_amino.index+1 == len(curr):
                count += 1
                if verbose:
                    self.log(f"found {count} solutions", start=True)

                if self.best is None or curr.score <= self.best.score:
                    self.best = curr
                continue

            else:
                for direction in curr.foldoptions(curr_amino):
                    if curr.empty_coordinate(curr_amino, direction):
                        nxt_prot = Protein.copy(curr)
                        nxt_prot.fold(curr_amino.index, direction)
                        self.__stack.append(nxt_prot)
                    else:
                        continue

        if verbose:
            self.log(f"Best solution: {self.best.score}", end=True)
        return self.best


if __name__ == "__main__":
    dff = DepthFirstFold("PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP")
    solution = dff.run(verbose=True)
    output(solution)
    visualize_protein(solution)
