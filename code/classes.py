class Protein:
    def __init__(self, string):
        def create_amino(letter):
            return Amino(letter)

        self.aminos = map(create_amino, string)


class Amino:
    def __init__(self, letter):
        self.letter = letter
        self.fold = 0

    # set fold
    