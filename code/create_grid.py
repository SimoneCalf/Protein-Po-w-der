from input_output import create
from classes.grid import Grid


def main():
    protein = create()
    grid = Grid(len(list(protein.aminos)))
    print(grid.grid)
    return


if __name__ == "__main__":
    main()