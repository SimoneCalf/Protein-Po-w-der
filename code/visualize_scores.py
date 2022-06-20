import matplotlib.pyplot as plt
import random

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])

score_freq = {}

for i in range(5):
    # score = random()
    # if score in score_freq:
        # score_freq[score] += 1
    # else:
        # score_freq[score] = 1
    score_freq[random.randint(1,10)] = random.randint(1, 10)
scores = score_freq.keys()
frequencies = score_freq.values()
ax.bar(scores, frequencies)
plt.show()
