from typing import Union
import random

from classes.protein import Protein
from classes.amino import Amino
from algorithms.BaseAlgorithm import BaseAlgorithm
from algorithms.random_protein import fold_randomly


class HillClimber(BaseAlgorithm):
    """A Hill Climber algorithm for folding proteins
    """
    def get_starting_point(self, protein: Protein) -> Protein:
        """Returns a randomly folded copy of the given protein

        Parameters
        ----------
        protein : Protein
            the protein to fold randomly

        Returns
        -------
        Protein
            a new protein instance with the same amino structure as the given
            protein, and folded randomly at every amino acid
        """
        protein = Protein.copy(protein)
        while True:
            fold_randomly(protein, protein.aminos[0])
            if protein.is_valid:
                return protein

    def fold_one_amino_acid(self, protein: Protein, amino: Amino) -> Protein:
        """Folds a Protein randomly at a single point

        Parameters
        ----------
        protein : Protein
            the protein to fold randomly
        amino : Amino
            the amino at which point the protein should be folded

        Returns
        -------
        Protein
            Returns a new protein instance with the same amino structure,
            but folded in a random valid direction at the given amino
        """
        protein = Protein.copy(protein)
        foldoptions = protein.foldoptions(amino, completely_random=True)
        foldoptions[:] =\
            [option for option in foldoptions if
                protein.empty_coordinate(amino, option)]
        if not foldoptions:
            return None
        direction = random.choice(foldoptions)
        protein.fold(amino.index, direction)
        return protein

    def get_random_amino(self, protein: Protein) -> Amino:
        """Selects a random amino from the protein

        Parameters
        ----------
        protein : Protein
            the protein to choose a random amino from

        Returns
        -------
        Amino
            Returns the instance of the randomly selected amino
        """
        return random.choice(protein.aminos[:-1])

    # gebruiken om het algoritme te starten
    def run(
        self,
        repeat: int = 10,
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
            the amount of times to mutate the protein, by default 500
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
        for s in range(0, repeat):
            start = self.get_starting_point(self.protein)
            no_improvement = i = 0
            # ga zolang door tot er n keer geen verbetering is gevonden
            while no_improvement <= iterations:
                if verbose:
                    self.log(
                        f"run: {s}; iteration {i}," +
                        f"no improvement: {no_improvement};" +
                        f"score: {start.score}"
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
            # een lokaal maximum behaald,
            # als dit beter is dan ons vorige resultaat dan slaan we het op
            # en gaan we nog een keer verder
            if self.best.score >= start.score:
                if verbose:
                    print(
                        f"Improved {self.best.score} by " +
                        f"{self.best.score - start.score} to {start.score}"
                    )
                self.best = Protein.copy(start)

        return self.best
