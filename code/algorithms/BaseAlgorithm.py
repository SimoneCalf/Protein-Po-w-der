from collections import deque
import sys
import time
import threading
from typing import Union

from classes.protein import Protein


class BaseAlgorithm():
    def __init__(self, protein: Union[Protein, str]) -> None:
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

        # logging nonsense
        self.__log = deque()
        self.__thread = None

    @property
    def protein(self):
        return Protein.copy(self.__protein)

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
                if q:
                    print(q.popleft(), end="\033[K\r", flush=True)
                else:
                    break
                time.sleep(.05)

        # add message to the queue
        # start the thread if the parameter is given
        if start and self.__thread is None:
            self.__thread = threading.Thread(
                target=loglisten,
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
        self.__log.append(msg)

    def run():
        raise NotImplementedError
