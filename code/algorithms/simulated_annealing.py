from random import random 

from classes.protein import Protein
from classes.amino import Amino
from algorithms.hillclimber import HillClimber
from algorithms.random_protein import fold_randomly

class SimulatedAnnealing(HillClimber):

    def __init__(self, protein: Protein, temperature: int = 1000):
        super().__init__(protein)
        self._start_temp = temperature

    # gebruiken om het algoritme te starten
    def run(
        self,
        iterations: int = 1000,
        verbose: bool = False
    ) -> Protein:
        """Actually starts the hillclimber algorithm

        Parameters
        ----------
        repeat : int, optional:
            the amount of times the algorithm creates a new starting point
            from which to start mutating the protein, by default 10
        iterations : int, optional
            the amount of times to mutate the protein after hitting a local
            minimum, by default 500
        verbose : bool, optional:
            flag that controls whether to execute logging statements or not,
            by default False

        Returns
        -------
        Protein
            Returns a valid protein instance with the amino structure
            of the given protein, folded in the shape of the best approximated
            solution
        """

        # safeguard giving repeat 0 or iterations 0
        iterations = max(1, iterations)

        start = self.get_starting_point(self.protein)
        i, no_improvement = 0, 0
        # ga zolang door tot er n keer geen verbetering is gevonden
        while no_improvement <= iterations:
            if verbose:
                self.log(
                    f"iteration {i}; " +
                    f" iterations with no improvement: {no_improvement}; "
                    + f"score: {start.score}",
                    start=True
                )
            # random vouwen
            # foldpoint is een amino object
            new_state = None
            while new_state is None:
                foldpoint = self.get_random_amino(start)
                new_state = self.fold_one_amino_acid(start, foldpoint)
                if not Protein.validate(new_state):
                    new_state = None

            # vergelijk de score, als er een verbetering is gevonden dan
            # slaan we die op en resetten we de counter

            if start.score >= new_state.score:
                start = Protein.copy(new_state)

                if start.score > new_state.score:
                    no_improvement = 0
                    continue

            # als er geen verbetering is gevonden dan verhogen we de
            # counter
            no_improvement += 1

            i += 1

            # als we n-keer geen verbetering hebben gevonden dan hebben we
            # een lokaal minimum behaald,
            # als dit beter is dan ons vorige resultaat dan slaan we het op
            # en gaan we nog een keer verder
            if random() :
                if verbose:
                    self.log(
                        f"Improved {self.best.score} by " +
                        f"{self.best.score - start.score} to {start.score}",
                    )
                self.best = Protein.copy(start)

        if verbose:
            self.log(
                f"Best solution: {self.best}; score: {self.best.score}",
                end=True
            )
        return self.best
