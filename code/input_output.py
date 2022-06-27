import csv
import os
import random


def output(protein, algorithm, string):
    # create dir if it does not already exist
    if not os.path.exists(f"data/{algorithm}"):
        os.makedirs(f"data/{algorithm}")

    file_number = random.getrandbits(16)

    with open(f"{string}_{file_number}.csv", "w") as f:
        writer = csv.writer(f)

        writer.writerow(["index", "amino", "fold"])

        for amino in protein.aminos:
            writer.writerow([amino.index, amino.type, amino.direction])

        writer.writerow(["score", protein.score])

    return
