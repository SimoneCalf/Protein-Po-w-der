import csv
from classes import Protein


def create():
    string = input() 
    return Protein(string)


def output(protein):
    with open("data/output.csv", "w") as f:
        writer = csv.writer(f)

        writer.writerow(["amino", "fold"])

        for amino in protein.aminos:
            writer.writerow([amino.letter, amino.fold])

        writer.writerow(["score", 0])
    return


def main():
    protein = create()
    output(protein)


if __name__ == "__main__":
    main()