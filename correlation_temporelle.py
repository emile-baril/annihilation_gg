import numpy as np
import matplotlib.pyplot as plt

plt.style.use("classic")

delay = [0.88, 0.86, 0.84, 0.82, 0.80, 0.78, 0.76, 0.74, 0.72, 0.7]
nbCoups = [2, 45, 811, 1332, 1525, 1503, 1310, 424, 43, 23]

plt.scatter(delay, nbCoups)
plt.xlim(xmin=0.68)
plt.show()