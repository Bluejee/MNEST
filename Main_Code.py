from Environment import World, Clock, Realise
from Entities import Agent, Essence
from Laws import *
import numpy as np
import random

"""
This is the main code file. The following is a sample template that can be modified inorder to create any type 
of simulations. This version uses inheritance to work through everything avoiding duplication and other issues.

Note : Maybe start custom variables with an _ or some identifier to prevent accidental renaming of variables.
(Or just keep in mind the parent class and not rename variables)
"""


# Setting up the Visualiser.
class Visualise(Realise):
    def __init__(self):
        # To Set up the Visualisation, Initialise the class with the World, required variables, and the one_step_loop
        # Initialise the world with necessary size and layers.
        # It is not recommended that the number of layers be more than 10
        # It Might cause errors within the visualisation.
        # The simulation will however work fine. just that the option for selecting layers will be disabled

        # Create the necessary layers.
        layers = {'Pheromone': ['Float', (209, 126, 17), 'None', 100],
                  'Home': ['Block', (214, 103, 191), 'None'],
                  'Agent': ['Block', (255, 0, 0), 'Stock_Images/ant_sq_20.png']}

        # Initialise the parent class.
        super().__init__(world=World(layer_data=layers, r_length=30, c_length=30))

        # Adjust set parameters
        self.frame_rate_cap = 60

        # Set up the new variables and performing initial setups.
        self.agent_list = [Agent(self.world, 'Agent', Vector2(i % 30, i % 30)) for i in range(50)]
        self.world.layers['Home'] = [[15, 15], [14, 14], [15, 14]]
        self.pheromone = Essence(self.world, 'Pheromone', 0, 3)
        self.loop(self.one_loop_step)

    # Create one step of the event loop that is to happen. i.e. how the world changes in one step.
    def one_loop_step(self):
        """
        This function is passed to the realise class to be run everytime the loop iterates.
        Basically this function is the entire set of changes that are to happen to the world.
        :return:
        """
        # [w, agent_list, pheromone] = loop_parameters
        for agent in self.agent_list:
            agent.move()

        for agent in self.agent_list:
            if np.random.randint(2) == 1:
                agent.direction = random.choice([RIGHT, LEFT, UP, DOWN])
            agent.move()
            # print(agent.position.y, agent.position.x)
            # using random and not np.random to use objects and not a np array.
            loc = self.world.layers['Pheromone'][int(agent.position.y), int(agent.position.x)]
            if loc < 80:
                self.world.layers['Pheromone'][int(agent.position.y), int(agent.position.x)] += 20
            # print(w.layers['Pheromone'][0])

        self.pheromone.decay()

        return


# Instantiating the realisation/ Gods Perspective
realise = Visualise()
