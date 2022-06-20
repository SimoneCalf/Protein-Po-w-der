import random

def random_folds(protein):
    for index, amino in enumerate(protein.aminos):
        if index == -1:
            protein.fold(protein, index, 0)
        else:
            options = amino.foldoptions()
            for option in options:
                if protein.bordercontrol(amino.x, amino.y) is not True:
                    options.remove(option)
                    continue
                if protein.empty_coordinate(amino.x, amino.y) is not True:
                    options.remove(option)

            direction = random.choice(options)
            protein.fold(index, direction)
    return
            