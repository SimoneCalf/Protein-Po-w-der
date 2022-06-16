from create_protein import create_protein
from fold_right import only_right
from input_output import output


def main():
    protein = create_protein()
    #  only_right(protein)
    output(protein)
    print(protein.grid)


if __name__ == "__main__":
    main()
