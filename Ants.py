from Environment import World, Clock, Realise
from Entities import Agent, Essence
from Laws import *
import numpy as np
import random

"""
This is the  code file. The following is a sample template that can be modified inorder to create any type 
of simulations. This version uses inheritance to work through everything avoiding duplication and other issues.

Note : Maybe start custom variables with an _ or some identifier to prevent accidental renaming of variables.
(Or just keep in mind the parent class and not rename variables)
"""


class Ant(Agent):

    def __init__(self, world, layer_name, position=Vector2(0, 0)):
        super().__init__(world, layer_name, position)

    def drop_pheromone(self, pheromone_type, quantity):
        pheromone_type = 'Pheromone_' + pheromone_type  # for simplicity
        self.world.layers[pheromone_type][int(self.position.y), int(self.position.x)] += quantity

        # capping pheromone at a cell to 100
        loc = self.world.layers[pheromone_type][int(self.position.y), int(self.position.x)]
        if loc > 100:
            self.world.layers[pheromone_type][int(self.position.y), int(self.position.x)] = 100
            # print(w.layers['Pheromone'][0])


# Setting up the Visualiser.
class Visualise(Realise):
    def __init__(self):
        # To Set up the Visualisation, Initialise the class with the World, required variables, and the one_step_loop
        # Initialise the world with necessary size and layers.
        # It is not recommended that the number of layers be more than 10
        # It Might cause errors within the visualisation.
        # The simulation will however work fine. just that the option for selecting layers will be disabled

        # Create the necessary layers.
        layers = {'Pheromone_B': ['Float', (209, 126, 17), 'None', 100],
                  'Pheromone_A': ['Float', (126, 209, 17), 'None', 100],
                  'Home': ['Block', (214, 103, 191), 'None'],
                  'Ants': ['Block', (255, 0, 0), 'Stock_Images/ant_sq.png']}

        # Initialise the parent class.
        # Adjust set parameters
        # sim_background = (255, 255, 255)
        super().__init__(world=World(layer_data=layers, r_length=30, c_length=30), frame_rate_cap=60, cell_size=20,
                         sim_background=(255, 255, 255))
        # Set up the new variables and performing initial setups.
        self.ant_list = [Ant(self.world, 'Ants', Vector2(i % 30, i % 30)) for i in range(2)]
        # self.ant_list = [Ant(self.world, 'Ants', Vector2(0, 0)), Ant(self.world, 'Ants', Vector2(5, 5))]
        self.world.layers['Home'] = [[15, 15], [14, 14], [15, 14], [14, 15]]
        self.pheromone_a = Essence(self.world, 'Pheromone_A', decay_rate=1)
        self.pheromone_b = Essence(self.world, 'Pheromone_B', decay_rate=3)
        # Do not add any variables after calling the loop. it will cause object has no attribute error when used.
        self.loop(self.one_loop_step)

    # Create one step of the event loop that is to happen. i.e. how the world changes in one step.
    def one_loop_step(self):
        """
        This function is passed to the realise class to be run everytime the loop iterates.
        Basically this function is the entire set of changes that are to happen to the world.
        :return:
        """
        for i, ant in enumerate(self.ant_list):
            # if np.random.randint(2) == 1:
            # using random and not np.random to use objects and not a np array.
            # ant.direction = random.choice([RIGHT, LEFT, UP, DOWN])
            ant.move()
            if ant.position.y == 0:
                ant.drop_pheromone('A', 100)
            else:
                ant.drop_pheromone('B', 100)

        self.pheromone_a.disperse()
        self.pheromone_b.disperse()
        return


# Instantiating the realisation/ Gods Perspective
realise = Visualise()
