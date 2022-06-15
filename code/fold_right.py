def only_right(protein):
    for index, amino in enumerate(protein.aminos):
        if index == 0:
            protein.place_in_grid(amino)
        else: 
            protein.fold(index, 1)
            protein.place_in_grid(amino)
