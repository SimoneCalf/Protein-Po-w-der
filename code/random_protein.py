import random

def random_folds(protein):
    for index, amino in enumerate(protein.aminos[:-1]):
        options = protein.foldoptions(amino)
        for option in options:
            if protein.empty_coordinate(amino, option) is False:
                options.remove(option)

        direction = random.choice(options)
        protein.fold(index, direction)

    return