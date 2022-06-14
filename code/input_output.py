import csv


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