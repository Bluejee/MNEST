import numpy as np
import pygame

"""
This file contains the classes that create the environment.
This would contain the Clock, The World, and the God's Perspective(Realise).
"""


class Clock:
    """
    This class represents the clock or timeline that keeps track of the current state of the world.
    Although this is not exactly necessary to be set up as a class, This allows more control and separation of time and
    the world so that each can be manipulated separately if necessary.
    """

    def __int__(self):
        self.time_step = 0

    def next_step(self):
        self.time_step += 1


class World:
    """
    This class represents the physical world that everything exists in.
    The only purpose of the world if to hold the classes of things and give it existence
    Thus, this is just a class that holds different layers and the structure of the world and does not provide any
    method of visualisation or control.

    The layers of the world are also set up such that each cell of a layer can only hold one element. If there exist a
    scenario such that there needs to be 2 Agents present at the same location, then each agent is given a different
    layer to exist on.


    """

    def __init__(self, r_length=30, c_length=30, layer_labels=['Agents']):
        self.r_length = r_length  # no of rows
        self.c_length = c_length  # no of columns
        self.layer_labels = layer_labels
        self.layers = {}
        for lable in self.layer_labels:
            self.layers[lable] = np.zeros([self.r_length, self.c_length])  # formation of one layer
        # r represents the vertical(row number) and c the horizontal(column number).


class Realise:
    def __int__(self, world, loop_step):
        self.world = world
        self.loop_step = loop_step
        self.width = 1300
        self.height = 1000
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw(self):
        # This function draws the layers of the world on to the screen
        # This also creates a list of layers for the user to click on to add or remove layer displays.

        return

    def loop(self):
        while True:
            # Checking events in pygame.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Running one step of the loop as provided in the definition.
            # This is defined by the creator according to the needs of the simulation.
            self.loop_step()

            # Running the draw loop to create all the necessory layouts and surfaces
            self.draw()

            # updating the clock as one step is completed.
            self.clock
