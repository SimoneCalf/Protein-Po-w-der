from classes.grid import Grid


def create_grid(protein):
    grid = Grid(len(protein.aminos))
    return grid