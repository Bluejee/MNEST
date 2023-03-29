from Environment import World, Clock, Realise
import matplotlib.pyplot as plt
import numpy as np

"""
This is the main code file. The following is a sample template that can be modified inorder to create any type 
of simulations. 
"""

# Initialising all the classes and functions for the simulation to run
# Initialise the world with necessary size and layers.
world = World(r_length=30, c_length=30, layer_labels=['Agent', 'Food', 'Home'])

# Initialise the clock.
clock = Clock()


# Create one step of the event loop that is to happen. i.e. how the world changes in one step.
def one_loop_step():
    """
    This function is passed to the realise class to be run everytime the loop iterates.
    Basically this function is the entire set of changes that are to happen to the world.
    :return:
    """

    # for random data for trial.
    if np.random.randint(60) == 1:
        # 1 in 60 probability to make a change
        layer = world.layers['Agent']
        layer[np.random.randint(30), np.random.randint(30)] = 1

    return


# Initialise the realisation/ Gods Perspective
realise = Realise(world=world, loop_step=one_loop_step, clock=clock)

# Now that all the classes have been initialised.
realise.loop()


# old code that might come in handy
# for c, layer in enumerate(w.layers):
#     layer = w.layers[layer]
#     layer[0, 0] = 1
#     layer[29, 29] = 1
#     c = ['r.', 'b.', 'g.'][c]
#
#     for i in range(10):
#         layer[np.random.randint(30), np.random.randint(30)] = 1
#
#     for y in range(layer.shape[0]):  # y as row number
#         for x in range(layer.shape[1]):  # x as column number
#             if layer[y, x] == 1:
#                 plt.plot(x, y, c)
#
