from random import random

from algorithms.hillclimber import HillClimber
from classes.protein import Protein


class SimulatedAnnealing(HillClimber):
    def __init__(self, protein: Protein, temperature: int = 2000) -> None:
        """Constructor method for Simulated Annealing

        Parameters
        ----------
        protein : Protein
            the protein this algorithm is to run on
        temperature : int, optional
            the starting temperature for this algorithm,
            can later also be set by run; by default 2000
        """
        super().__init__(protein)
        self.__start_temp = temperature
        self.iterations = 1000

    def get_temperature(self, i: int = 1) -> int:
        """Returns the current temperature

        Parameters
        ----------
        i : int, optional
            the amount of iterations this algorithm has already run;
            by default 1

        Returns
        -------
        int
            the calculated temeperature at the given amout of iterations
        """
        return self.__start_temp - (self.__start_temp/self.iterations) * i

    def accept(self, new: Protein, old: Protein, iterations: int = 1) -> bool:
        """
        Calculates whether the new (worse) protein configuration
        should be accepted depending on the difference in score and the current
        temperature

        Parameters
        ----------
        new : Protein
            the new protein configuration
        old : Protein
            the old protein configuration
        iterations : int, optional
            the amount of iterations we have already done, by default 1

        Returns
        -------
        float
            The chance to accept the new solution, even though it's worse
        """
    def accept(self, new, old, iterations=1):
        # !!
        return 2**(
            new.score - old.score /
            float(self.get_temperature(iterations)+1)
        )

    # gebruiken om het algoritme te starten
    def run(self,
            iterations: int = 1000,
            start_temp: int = None,
            verbose: bool = False
            ) -> Protein:
        """
        Starts the algorithm

        Parameters
        ----------
        iterations : int, optional
            the amount of iterations to run; by default 1000
        start_temp : int, optional
            the starting temperature
        verbose : bool, optional
            whether to log messages to stdout, by default False

        Returns
        -------
        Protein :
            Returns the best solution we have found
        """
        # set verbose
        self.verbose = verbose

        # make sure we'll run the algorithm at least once
        self.iterations = max(1, iterations)

        # same for temperature is set
        if isinstance(start_temp, int):
            self.__start_temp = max(100, start_temp)

        # get random starting point
        curr = self.get_starting_point(self.protein)

        for i in range(self.iterations):
            new_state = None
            while not Protein.validate(new_state):
                new_state = self.fold_randomly(curr)

            self.log(
                f"iteration: {i}; " +
                f"score: {new_state.score - curr.score} "
                f"accept chance: {self.accept(curr, new_state, i)}",
            )

            if curr.score >= new_state.score:
                curr = Protein.copy(new_state)
                continue

            accept_chance = self.accept(new_state, curr, i+1)
            #  self.log(f"accept?: {accept_chance}")
            if random() < accept_chance:
                curr = Protein.copy(new_state)

            self.log(
                f"Best solution: {curr}; " +
                f"score: {curr.score}",
            )

        return Protein.copy(curr)
