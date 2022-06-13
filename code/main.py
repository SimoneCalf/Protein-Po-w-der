from create_grid import create_grid
from create_protein import create_protein
from input_output import output


def main():
    protein = create_protein()
    grid = create_grid(protein)
    output(protein)


if __name__ == "__main__":
    main()