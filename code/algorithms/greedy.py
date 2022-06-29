import random

from classes.amino import Amino
from classes.protein import Protein
from visualization import visualize_protein


def greedy(
        protein: Protein,
        prev: Amino = None,
        faulty_direction: int = None):
    """

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

    options[:] = [option for option in options
                  if protein.empty_coordinate(curr, option)]

    if not options:
        faulty_direction = prev.direction
        prev.direction = 0
        greedy(
            protein,
            protein.aminos[prev.index - 1] if prev.index > 0 else 0,
            faulty_direction)
    else:
        scores = []
        for option in options:
            protein.fold(curr.index, option)
            score = protein.score
            scores.append(score)
        print(f"scores: {scores}")
        minimum = [index for index, score in enumerate(scores)
                   if score == min(scores)]
        print(f"minimum: {minimum}")
        direction = options[random.choice(minimum)]
        protein.fold(curr.index, direction)
        print(protein.grid)
        visualize_protein(protein)
        greedy(protein, curr)
