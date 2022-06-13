import csv
from classes.protein import Protein


def create():
    string = input("protein: ") 
    return Protein(string)


def output(protein):
    with open("data/output.csv", "w") as f:
        writer = csv.writer(f)

        writer.writerow(["amino", "fold", "previous", "next"])

        for amino in protein.aminos:
            if amino.previous is None:
                writer.writerow([amino.letter, amino.fold, None, amino.next.letter])
            elif amino.next is None:
                writer.writerow([amino.letter, amino.fold, amino.previous.letter, None])
            else:
                writer.writerow([amino.letter, amino.fold, amino.previous.letter, amino.next.letter])


        writer.writerow(["score", 0])
    return


def main():
    protein = create()
    output(protein)


if __name__ == "__main__":
    main()