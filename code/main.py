from create_protein import create_protein
from input_output import output


def main():
    protein = create_protein()
    output(protein)
    print(protein.grid)


if __name__ == "__main__":
    main()
