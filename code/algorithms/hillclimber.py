from logging import raiseExceptions
from algorithms.random_protein import fold_randomly
from classes.protein import Protein
import random

class NoValidFoldException(Exception):
    pass

class hillclimber():
    def __init__(self, prot):

        # create protein from string if string was given
        if type(prot) == str:
            self.__protein = Protein(prot)
        elif type(prot) == Protein:
            self.__protein = prot
        else:
            raise TypeError(
                f"Unsupported type {type(prot)}," +
                f"must be of type '{str}' or '{Protein}'"
            )


    @property
    def protein(self):
        return Protein.copy(self.__protein)

    def get_starting_point(self, protein):
        fold_randomly(protein, protein.aminos[0])
        return protein

    def fold_one_amino_acid(self, protein, amino):
        foldoptions = protein.foldoptions(amino)
        foldoptions[:] = [option for option in foldoptions if protein.empty_coordinate(amino, option)]
        if not foldoptions:
             return None
        direction = random.choice(foldoptions)
        protein.fold(amino.index, direction)
        return protein

    def getrandomamino(self, protein):
        return random.choice(protein.aminos[:-1])

    # gebruiken om het algoritme te starten
    def run(self, itterations=1000):
        for i in range(0, itterations):
            start = self.get_starting_point(self.protein)
            # random vouwen
            # foldpoint is een amino object
            changed = None
            while changed == None:
                foldpoint = self.getrandomamino(start)
                changed = self.fold_one_amino_acid(Protein.copy(start), foldpoint)
            # score vergelijken
            if start.score >= changed.score:
                self.__protein = changed
            # beste vouwing eitwit opslaan
        return self.__protein

    