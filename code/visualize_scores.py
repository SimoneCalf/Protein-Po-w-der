import matplotlib.pyplot as plt
import random

score_freq = {}

for i in range(5):
    score = random.randint(1, 1000)

    if score in score_freq:
        score_freq[score] += 1
    else: 
        score_freq[score] = 1

scores = list(score_freq.keys())
frequencies = list(score_freq.values())

plt.bar(scores, frequencies)
plt.show()



    


