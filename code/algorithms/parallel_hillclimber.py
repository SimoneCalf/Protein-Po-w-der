from multiprocessing import Process, cpu_count, Queue
from os import getpid
from typing import Union

from algorithms.hillclimber import HillClimber
from classes.protein import Protein


class ParallelHillClimber(HillClimber):

    def log(self, msg: str, end=False):
        """A single-threaded version of BaseAlgorithm log

        Parameters
        ----------
        msg : str
            the message to log

        See Also
        --------
        `BaseAlgorithm.log`: A threaded log method that prints messages to
                             stdout
        `PythonSpeed
        <https://pythonspeed.com/articles/python-multiprocessing/>`_:
            an article explaining why mixing threads and processes doesn't work

        """
        if not self.verbose:
            return

        if end:
            print("\033]K")
            print(msg)
        else:
            print(msg, end="\033[K\r", flush=True)

    def parallel(
                self,
                protein: Protein,
                save_to: Queue,
                iterations: int = 1000,
                verbose: bool = False,
            ) -> Protein:
        """
        Function to be run in parallel, executes one run of hillclimber
        Can also be called directly

        Parameters
        ----------
        protein : Protein
            the protein to run this function on
        save_to : Queue
            the queue to save results to
        iterations : int, optional
            the amount of maximum amount iterations to continue,
            when no improvement was found; by default 1000
        verbose : bool, optional
            whether to log messages to stdout, by default False
        """
        # make sure we'll run the algorithm at least once
        iterations = max(1, iterations)

        # get random starting point
        curr = self.get_starting_point(protein)

        for i in range(iterations):
            if self.verbose >= 3:
                self.log(
                    f"process {getpid()}; " +
                    f"iteration: {i}; " +
                    f"score: {curr.score}"
                )
            new_state = None
            while not Protein.validate(new_state):
                new_state = self.fold_randomly(curr)

            if curr.score >= new_state.score:
                curr = Protein.copy(new_state)

        if verbose:
            self.log(
                f"Best solution for {getpid()}: {curr}; " +
                f"score: {curr.score}",
            )

        # we can only store primitive types in a multiprocessing queue
        # so we serialize our protein
        save_to.put({"types": curr.types, "directions": curr.directions})
        return curr # return call in case paralel gets called directly

    def run(
        self,
        runs: int = 10,
        iterations: int = 1000,
        verbose: Union[bool, int] = 0
    ) -> Protein:
        """
        Function that starts running the algorithm on
        the protein this instance was initiated with


        Parameters
        ----------
        runs : int, optional
            the amount of runs to do (in paralel), by default 10
        iterations : int, optional
            how many iterations to continue while finding no improvement
            is reset when an improvement is found; by default 1000
        verbose : Union[bool, int], optional
            Whether to log messages to stdout, by default 0
            this is changed from the single-process version of HillClimber
            to implement a loglevel:

                0, False: do not log messages to stdout

                1, True:  only log messages between runs

                2:        log status messages during runs,
                          whenever we've improved our best solution

                3:        log status messages during runs; every iteration

        Returns
        -------
        Protein
            the best solution we have found overall
        """
        # update verbose flag
        self.verbose = verbose
        # initialize values for managing processes and their results
        process_count = min(cpu_count()-1, max(runs, 1))
        runs_completed = 0
        processes = []
        results = Queue()
        process_args = (self.protein, results, iterations, self.verbose >= 2)

        # create processes
        for i in range(0, process_count):
            p = Process(target=self.parallel, args=process_args)
            processes.append(p)

        self.log(
            f"Starting paralel HillClimber with {process_count} processes"
        )

        # start processes, then wait wait for them to complete
        # then, if there are still runs to be done, we start a new process
        while runs_completed < runs:
            for p in processes:
                if not p.is_alive():
                    p.start()

            for i, p in enumerate(processes):
                p.join(60)  # wait for max. 60 seconds for process to finish
                runs_completed += 1

                # retrieve latest result, and massage the result into a protein
                if not results.empty():
                    result = results.get(timeout=60)
                    result = Protein(result["types"], result["directions"])
                    self.log(
                        f"Run {runs_completed-1} completed with " +
                        f"score {result.score}"
                    )

                    # check if it's better than the best
                    if self.best.score > result.score:
                        self.best = result

                # if we still need to do some runs we replace the process with
                # a new one (you can't restart Processes :( )
                if runs_completed < runs:
                    processes[i] = Process(
                        target=self.parallel,
                        args=process_args
                    )

        return self.best
