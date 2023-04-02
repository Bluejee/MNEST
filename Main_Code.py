from Environment import World, Clock, Realise
from Entities import Agent, Essence
from Laws import *
import numpy as np
import random

"""
This is the main code file. The following is a sample template that can be modified inorder to create any type 
of simulations. 
"""

# Initialising all the classes and functions for the simulation to run
# Initialise the world with necessary size and layers.
# It is not recommended that the number of layers be more than 10 as it will cause errors within the visualisation.
# The simulation will however work fine. just that the option for selecting layers will be disabled

layers = {'Pheromone': ['Float', (209, 126, 17), 'None', 100],
          'Home': ['Block', (214, 103, 191), 'None'], 'Agent': ['Block', (255, 0, 0), 'Stock_Images/ant_sq_20.png']}

w = World(layer_data=layers, r_length=30, c_length=30)

# Setting up the Agent and Home
agent_list = [Agent(w, 'Agent', Vector2(i % 30, i % 30)) for i in range(50)]
w.layers['Home'] = [[15, 15], [14, 14], [15, 14]]
pheromone = Essence(w, 'Pheromone', 0, 3)
# Initialise the clock.
clock = Clock()

# Create one step of the event loop that is to happen. i.e. how the world changes in one step.

parameters = [w, agent_list, pheromone]


# params is a list of variables defined in the main code that are set up during initialisation that are required for
# the loop to function.
# This could include the world, custom agents, counters, or another parameter that is initialised similar to the
# global variables for a regular program.
# Inorder to preserve the names of the variables, we copy the list (the right-hand side of the params equations).
# and paste it into the loop to access the same parameters while being passed through the realise module.


def one_loop_step(loop_parameters: list):
    """
    This function is passed to the realise class to be run everytime the loop iterates.
    Basically this function is the entire set of changes that are to happen to the world.
    :return:
    """
    # [w, agent_list, pheromone] = loop_parameters
    for agent in agent_list:
        agent.move()

    for agent in agent_list:
        if np.random.randint(2) == 1:
            agent.direction = random.choice([RIGHT, LEFT, UP, DOWN])
        agent.move()
        # print(agent.position.y, agent.position.x)
        # using random and not np.random to use objects and not a np array.
        loc = w.layers['Pheromone'][int(agent.position.y), int(agent.position.x)]
        if loc < 80:
            w.layers['Pheromone'][int(agent.position.y), int(agent.position.x)] += 20
        # print(w.layers['Pheromone'][0])

    pheromone.decay()

    return


# Initialise the realisation/ Gods Perspective
realise = Realise(world=w, loop_step=one_loop_step, loop_parameters=parameters,
                  clock=clock, sim_background=(89, 187, 247))
realise.frame_rate_cap = 60
# Now that all the classes have been initialised.
realise.loop()
