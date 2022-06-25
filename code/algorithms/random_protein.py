import random
import sys
from typing import List

from classes.protein import Protein
from classes.amino import Amino


def fold_randomly(
        protein: Protein,
        prev: Amino,
        faulty_directions: List[int] = []):
    """Folds a protein in a random direction at every amino

    Parameters
    ----------
    protein : Protein
        the protein to fold randomly
    prev : Amino
        the previous amino, should be the first amino uninitialized amino on
        the first call
    faulty_directions : List[int], optional
        a direction to be pruned from the options to choose from when,
        backtracking, by default []

    See Also:
        `https://www.geeksforgeeks.org/python-handling-recursion-limit/ <GFG>`
        for credit for the code for increasing the recursion count
    """

    # get default recursion limit for later
    default_recur_count = sys.getrecursionlimit()
    # retrieve next uninitialized amino
    curr = protein.next_uninitialized()

    # check if all amino have been placed,
    # if so set recursion limit back to default and return the protein
    if curr is None:
        sys.setrecursionlimit(default_recur_count)
        return protein

    # temporarily increase recursion limit
    sys.setrecursionlimit(10**6)

    options = protein.foldoptions(
        curr,
        completely_random=curr.index == 0 and faulty_directions)

    # Remove all options that lead to a non-empty coordinate
    options[:] =\
        [option for option in options if
            protein.empty_coordinate(curr, option)]

    # Remove all options that lead to a dead end later on
    if faulty_directions:
        options = [o for o in options if o not in faulty_directions]

    # if no options are left take one step back, otherwise execute the fold,
    # and go on to the next amino acid
    if not options:
        faulty_directions.append(prev.direction)
        prev.direction = 0
        fold_randomly(
            protein,
            protein.aminos[prev.index - 1] if prev.index > 0 else
            protein.aminos[0],
            faulty_directions)
    else:
        direction = random.choice(options)
        protein.fold(curr.index, direction)
        fold_randomly(protein, curr)
