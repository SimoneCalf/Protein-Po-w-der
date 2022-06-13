from .amino import Amino


class Protein:
    def __init__(self, string):
        self.aminos = list(map(self.create_amino, string))
        self.set_previous()
        self.set_next()

    def create_amino(self, letter):
        return Amino(letter)

    def set_previous(self):
        self.aminos[0].previous = None

        i = 0
        for amino in self.aminos[1:]:
            amino.previous = self.aminos[i]
            i += 1

    def set_next(self):
        self.aminos[-1].next = None

        i = 1
        for amino in self.aminos[:-1]:
            amino.next = self.aminos[i]
            i += 1

    def calc_score(self):
        pass
