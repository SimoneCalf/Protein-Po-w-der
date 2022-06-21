import csv
import os

def output(protein):
    # create dir if it does not already exist
    if not os.path.exists("data/"):
        os.makedirs("data/")

    with open("data/output.csv", "w") as f:
        writer = csv.writer(f)

        writer.writerow(["index", "amino", "fold"])

        for amino in protein.aminos:
            writer.writerow([amino.index, amino.type, amino.direction])

        writer.writerow(["score", protein.score])

    return