def right(amino):
    amino.set_fold(1)
    amino.x = amino.previous.x + 1
    return

def only_right(protein):
    protein.place_in_grid(protein.aminos[0])
    for amino in protein.aminos[1:]:
        right(amino)
        protein.place_in_grid(amino)
