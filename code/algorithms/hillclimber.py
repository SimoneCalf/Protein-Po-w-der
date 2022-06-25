from typing import Union
from algorithms.random_protein import fold_randomly
from classes.protein import Protein
from classes.amino import Amino
import random


class HillClimber():
    """A Hill Climber algorithm for folding proteins
    """
    def __init__(self, prot: Union[Protein, str]) -> None:
        """Constructor method

        Parameters
        ----------
        prot : Union[Protein, str]
            the protein to fold; can either be a Protein instance or a string
            of amino types to represent a protein

        Raises
        ------
        TypeError
            raises a TypeError when the given parameter is neither a Protein
            instance or a string
        """
        # create protein from string if string was given
        if type(prot) == str:
            self.__protein = Protein(prot)
        elif type(prot) == Protein:
            self.__protein = Protein.copy(prot)
        else:
            raise TypeError(
                f"Unsupported type {type(prot)}," +
                f"must be of type '{str}' or '{Protein}'"
            )
        self.best = self.protein

    @property
    def protein(self) -> Protein:
        """Returns a new Protein instance of the protein property

        Returns
        -------
        Protein
            a copy of the protein instance property
        """
        return Protein.copy(self.__protein)

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
        for _ in range(0, repeat):
            start = self.get_starting_point(self.protein)
            for i in range(0, iterations):
                # random vouwen
                # foldpoint is een amino object
                new_state = None
                while new_state is None:
                    foldpoint = self.get_random_amino(start)
                    new_state = self.fold_one_amino_acid(start, foldpoint)
                    if not Protein.validate(new_state):
                        new_state = None
                # score vergelijken
                if start.score >= new_state.score:
                    start = Protein.copy(new_state)
                # beste vouwing eitwit opslaan

            if self.best.score >= start.score:
                if verbose:
                    print(
                        f"Improved {self.best.score} by " +
                        f"{self.best.score - start.score} to {start.score}"
                    )
                self.best = Protein.copy(start)

        return self.best
