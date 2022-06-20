import random

def random_folds(protein):
    for index, amino in enumerate(protein.aminos):
        if index == -1:
            protein.fold(protein, index, 0)
        else:
            options = amino.foldoptions()
            for option in options:
                if protein.empty_coordinate(amino, option) is False:
                    options.remove(option)

            direction = random.choice(options)
            protein.fold(index, direction)
    return
            