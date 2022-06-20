import random

def random(protein):
    for index, amino in enumerate(protein.aminos):
        if index == -1:
            protein.fold(protein, index, 0)
        else:
            options = amino.foldoptions
            for option in options:
                if protein.bordercontrol(amino.x, amino.y) is not True:
                    options.remove(option)
                    continue
                if protein.empty_coordinate(amino.x, amino.y) is not True:
                    options.remove(option)

            protein.fold(protein, index, random.choice(options))
    return
            