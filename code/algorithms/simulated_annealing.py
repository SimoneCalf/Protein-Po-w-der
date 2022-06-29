from random import random
from tempfile import tempdir
from math import floor

from classes.protein import Protein
from classes.amino import Amino
from algorithms.hillclimber import HillClimber
from algorithms.random_protein import fold_randomly


class SimulatedAnnealing(HillClimber):
    def __init__(self, protein: Protein, temperature: int = 2000):
        super().__init__(protein)
        self._start_temp = temperature
        self.iterations = 1000

    def get_temperature(self, i=1):
        return self._start_temp - (self._start_temp/self.iterations) * i

    def accept(self, new, old, iterations=1):
        return 2**(
            new.score - old.score /
            float(self.get_temperature(iterations)+1)
        )

    # gebruiken om het algoritme te starten
    def run(self,
            iterations: int = 1000,
            verbose: bool = False
            ):
        # make sure we'll run the algorithm at least once
        self.iterations = max(1, iterations)

        # get random starting point
        curr = self.get_starting_point(self.protein)

        for i in range(self.iterations):
            new_state = None
            while not Protein.validate(new_state):
                new_state = self.fold_randomly(curr)

            print(
                f"iteration: {i}; " +
                f"score: {new_state.score - curr.score} "
                f"accept chance: {self.accept(curr, new_state, i)}",
            )

            if curr.score >= new_state.score:
                curr = Protein.copy(new_state)
                continue

            accept_chance = self.accept(new_state, curr, i+1)
            #  print(f"accept?: {accept_chance}")
            if random() < accept_chance:
                curr = Protein.copy(new_state)

        if verbose:
            self.log(
                f"Best solution: {curr}; " +
                f"score: {curr.score}",
            )

        return Protein.copy(curr)
