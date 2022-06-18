from classes.amino import Amino
from collections import deque


amino_stack = deque()
amino_root = Amino("")


def fold_protein(string, current_amino, position):
    if position == len(string):
        return
    for direction in current_amino.foldoptions():
        new_amino = Amino(string[position], direction)
        amino_stack.append(new_amino)
    print(amino_stack)
    fold_protein(string, amino_stack.pop(), position+1)


if __name__ == "__main__":
    fold_protein("hp", amino_root, 0)
    print(amino_stack)
