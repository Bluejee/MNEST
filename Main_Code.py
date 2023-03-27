from Environment import World
import matplotlib.pyplot as plt
import numpy as np

"""
This file contains 
"""

w = World(layer_labels=['Agent', 'Food', 'Home'])

for c, layer in enumerate(w.layers):
    layer = w.layers[layer]
    layer[0, 0] = 1
    layer[29, 29] = 1
    c = ['r.', 'b.', 'g.'][c]

    for i in range(10):
        layer[np.random.randint(30), np.random.randint(30)] = 1

    for y in range(layer.shape[0]):  # y as row number
        for x in range(layer.shape[1]):  # x as column number
            if layer[y, x] == 1:
                plt.plot(x, y, c)

plt.show()
