from input_output import create
from classes import Grid


def main():
    protein = create()
    grid = Grid(len(list(protein.aminos)))
    return


if __name__ == "__main__":
    main()