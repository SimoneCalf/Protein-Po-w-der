import random


def fold_randomly(protein):
    for amino in (amino for amino in protein.aminos[:-1] if amino.direction == 0):
        options = protein.foldoptions(amino)
        for option in options:
            if protein.empty_coordinate(amino, option) is False:
                options.remove(option)

        direction = random.choice(options)
        protein.fold(amino.index, direction)

    return


def fold_randomly(protein, prev, faulty_direction=None):
    # retrieve next uninitialized amino
    curr = protein.next_uninitialized()

    # check if all amino have been placed
    if curr is None:
        return
    options = protein.foldoptions(curr)

    # chosen path is a dead end
    if faulty_direction:
        options.remove(faulty_direction)

    for option in options:
        if protein.empty_coordinate(curr, option) is False:
            options.remove(option)
        
    if not options:
        faulty_direction = prev.direction
        prev.direction = 0
        fold_randomly(protein, protein.aminos[prev.index - 1], faulty_direction)
    else:
        direction = random.choice(options)
        protein.fold(curr.index, direction)
        fold_randomly(protein, curr)
    
    
    



    
