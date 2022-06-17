import csv
import time

with open("data/scores.csv", "w") as f:
    writer = csv.DictWriter(f)

    writer.writeheader(["score", "frequency"])

    score_freq = {}

    for i in range(1000):
        score = random()

        if score in score_freq:
            score_freq[score] += 1
        else: 
            score_freq[score] = 1

        writer.writerows(score_freq)