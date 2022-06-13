from .amino import Amino

class Protein:
    def __init__(self, string):
        def create_amino(letter):
            return Amino(letter)

        self.aminos = map(create_amino, string)