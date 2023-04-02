from Laws import *


class Agent:
    def __init__(self, world, layer_name, position=Vector2(0, 0)):
        self.world = world
        self.layer_name = layer_name
        self.position = position
        self.direction = RIGHT

        # Fun Fact.
        # As We are storing the position of the element inside the layer. and not a copy of the values.
        # It is stored as a reference and hence we do not have to update the world values everytime.
        # Frankly for all those who are reading this. I was about to write code to update the values when i accidently
        # ran the simulation to test and saw them updating automatically.
        # I jumped* up and down around the room (* Literally.)
        self.world.layers[self.layer_name] = [position, *self.world.layers[self.layer_name]]

    def move(self):
        self.position += self.direction

        # Boundary Check

        # Left
        if self.position.x < 0:
            if self.world.periodic_boundary:
                self.position = self.world.c_length - 1
            else:
                self.position -= self.direction
                self.direction *= -1  # Flip direction.
                # print('Reflect right')

        # Right
        if self.position.x >= self.world.c_length:
            if self.world.periodic_boundary:
                self.position = 0
            else:
                self.position -= self.direction
                self.direction *= -1  # Flip direction.
                # print('Reflect left')

        # Up
        if self.position.y < 0:
            if self.world.periodic_boundary:
                self.position = self.world.r_length - 1
            else:
                self.position -= self.direction
                self.direction *= -1  # Flip direction.
                # print('Reflect down')

        # Right
        if self.position.y >= self.world.r_length:
            if self.world.periodic_boundary:
                self.position = 0
            else:
                self.position -= self.direction
                self.direction *= -1  # Flip direction.
                # print('Reflect up')


class Essence:
    def __init__(self, world, layer_name, dispersion_rate=0, decay_rate=0):
        self.world = world
        self.layer_name = layer_name
        self.max_value = self.world.layer_data[layer_name][3]
        self.decay_rate = decay_rate
        self.dispersion_rate = dispersion_rate

    def disperse(self):
        # use matrices and convolutions to disperse
        pass

    def decay(self):
        # use matrices and convolutions to disperse
        self.world.layers[self.layer_name] -= self.decay_rate

        # check if any value went below 0 and if so set it to 0.
        mask = self.world.layers[self.layer_name] < 0
        self.world.layers[self.layer_name][mask] = 0
