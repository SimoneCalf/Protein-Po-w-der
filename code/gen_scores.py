import csv
import time

with open("data/scores.csv", "w") as f:
    writer = csv.writer(f)

    score_freq = {}

    for i in range(1000):
        score = i

        if score in score_freq:
            score_freq[score] += 1
        else: 
            score_freq[score] = 1

        for score in score_freq:
            writer.writerow([score, score_freq[score]])

        time.sleep(1)
    