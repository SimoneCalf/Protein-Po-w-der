from collections import deque
import sys
import threading
import time
from typing import Union

from classes.protein import Protein


class BaseAlgorithm():
    """A superclass with some common properties and methods used by algorithms

    Attributes
    -----------
    protein: Protein
        a copy of the protein the instance was first initialized with
    best: Protein
        the best protein this algorithm has found (so far)
    verbose: bool
        flag that controls whether the algorithm prints extra information
        while it is running

    Methods
    -------
    log(msg="", start=False, end=False):
        prints a message if the verbose flag is set

    """
    def __init__(self, protein: Union[Protein, str]) -> None:
        """Constructor method for BaseAlgorithm, do not call directly

        Parameters
        ----------
        protein : Union[Protein, str]
            the protein to run an algorithm on (not this one though)

        Raises
        ------
        TypeError
            Returns a TypeError if the given argument is neither a protein,
            nor a string;
        """
        # create protein from string if string was given
        if type(protein) == str:
            self.__protein = Protein(protein)
        elif type(protein) == Protein:
            self.__protein = Protein.copy(protein)
        else:
            raise TypeError(
                f"Unsupported type {type(protein)}," +
                f"must be of type '{str}' or '{Protein}'"
            )
        self.best = self.protein
        self.prot_str = self.__protein.types

        # needed for threaded logging
        self.verbose = False
        self.__log = deque()
        self.__thread = None

    @property
    def protein(self) -> Protein:
        """Returns a copy of the protein this algorithm was initiated with

        Returns
        -------
        Protein
            a new protein instance with the same data as the protein this
            algorithm was initiated with
        """
        return Protein.copy(self.__protein)

    def __loglisten(self, q: deque):
        """Listens to and prints log messages put in the log queue

        This function will run in a endless loop, until the queue is empty
        so not to be called directly; instead use `BaseAlgorithm.log` which
        starts this function in a seperate thread
`
        Parameters
        ----------
        q : deque
            the queue this function will check for messages
        """
        while True:
            if q:
                print(q.popleft(), end="\033[K\r", flush=True)
            else:
                break
            time.sleep(.05)

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
        if not self.verbose:
            return

        # start the thread if the parameter is given
        if start and self.__thread is None:
            self.__thread = threading.Thread(
                target=self.__loglisten,
                daemon=True,
                args=(self.__log,)
            )
            self.__thread.start()
        # stop if a thread exists and the flag was set
        if self.__thread is not None and end:
            self.__thread.join()
            self.__thread = None
            sys.stdout.write("\033[K\r")

            print(msg)
            return

        # add message to the queue
        self.__log.append(msg)

    def parallel(self) -> Protein:
        """
        Function that must be implemented by any child processes that use
        multiprocessing

        Returns
        -------
        Protein
            the implemented function must return Protein, so that the function
            may be directly called as well

        Raises
        ------
        NotImplementedError
            This function must be implemented by any child classes
        """
        raise NotImplementedError

    def run(verbose: bool = False) -> Protein:
        """
        Function children classes must overload;
        to be used to start the algorith

        Parameters
        ----------
        verbose : bool, optional
            whether to log messages to stdout, by default False

        Return
        ------
        Protein :
            any child class must implement run such that it returns
            a Protein instance

        Raises
        ------
        NotImplementedError
            This function must be implemented by any child classes
        """
        raise NotImplementedError
