import random
from classes.protein import Protein
from classes.amino import Amino


def fold_randomly(
        protein: Protein,
        prev: Amino,
        faulty_direction: int = None):
    """Folds a protein in a random direction at every amino

    Parameters
    ----------
    protein : Protein
        the protein to fold randomly
    prev : Amino
        the previous amino, should be the first amino uninitialized amino on
        the first call
    faulty_direction : int, optional
        a direction to be pruned from the options to choose from when,
        backtracking by default None
    """

    # retrieve next uninitialized amino
    curr = protein.next_uninitialized()

    # check if all amino have been placed
    if curr is None:
        return
    options = protein.foldoptions(curr)

    # chosen path is a dead end
    if faulty_direction:
        options.remove(faulty_direction)

    picked = None
    for option in options:
        if protein.empty_coordinate(curr, option):
            picked = option

    if not picked:
        faulty_direction = prev.direction
        prev.direction = 0
        fold_randomly(
            protein,
            protein.aminos[prev.index - 1]
            if prev.index > 0 else protein.aminos[0],
            faulty_direction)
    else:
        direction = random.choice(options)
        protein.fold(curr.index, direction)
        fold_randomly(protein, curr)
