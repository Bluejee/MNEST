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

    def __init__(self):
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

    The layer input while initialising the class also contains additional information such as layer type and color which
    can be used for visualisation

    """

    def __init__(self, layer_data: dict, r_length=30, c_length=30):
        """

        :param layer_data: data of the form
        {'layer_label': ['Layer_type(Block/Float)', '#Hex_code_for_color', 'Path_for_sprite_image/None',
        'In case of Float a max value to calculate %']}
        :param r_length: number of rows of the world.
        :param c_length: number of columns of the world.
        """
        self.r_length = r_length  # no of rows
        self.c_length = c_length  # no of columns
        self.layer_data = layer_data
        self.layers = {}
        for label in self.layer_data:
            self.layers[label] = np.zeros([self.r_length, self.c_length])  # formation of one layer
        # r represents the vertical(row number) and c the horizontal(column number).


class Realise:
    """
    This is the class used to visualise the environment/simulation.
    """

    def __init__(self, world: World, loop_step, clock: Clock, cell_size=20, border_size=2, border_color=(255, 0, 0),
                 clock_color=(56, 74, 12)):
        pygame.init()
        # Simulation Variables
        self.world = world
        self.loop_step = loop_step
        self.clock = clock
        self.state = "Pause"

        # Visualisation Variables
        self.pyclock = pygame.time.Clock()
        self.cell_size = cell_size

        self.border_size = border_size  # border goes around the simulation
        self.border_color = border_color

        self.sim_width = (self.cell_size * self.world.c_length)  # width = no of columns * cell_size
        self.sim_height = (self.cell_size * self.world.r_length)  # height = no of rows * cell_size

        self.menu_width = int(self.sim_width / 3)

        self.screen_height = self.sim_height + 2 * border_size
        self.screen_width = self.sim_width + self.menu_width + 2 * border_size

        self.clock_color = clock_color

        # Surface and Display Variables
        # Screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen.fill(border_color)

        # Menu
        self.menu_surf = pygame.Surface((self.menu_width, self.screen_height))
        self.menu_surf.fill((0, 255, 0))
        self.menu_rect = self.menu_surf.get_rect(topright=(self.screen_width, 0))

        # Simulation
        self.sim_surf = pygame.Surface((self.sim_width, self.sim_height))
        self.sim_surf.fill((0, 0, 255))
        self.sim_rect = self.sim_surf.get_rect(topleft=(self.border_size, self.border_size))

        # Clock/Step text
        self.clock_font = pygame.font.Font(None, 25)

    def draw_menu(self):
        # Draw menu
        self.screen.blit(self.menu_surf, self.menu_rect)

        # Clock Step
        step_text = 'Step :: ' + str(self.clock.time_step)
        step_surf = self.clock_font.render(step_text, True, self.clock_color)
        step_rect = step_surf.get_rect(
            midbottom=(self.menu_rect.centerx, self.menu_rect.bottom - 2 * self.border_size))
        self.screen.blit(step_surf, step_rect)

        # Play Prompt.
        prompt_text = 'Press Space to '
        if self.state == "Play":
            prompt_text += "Pause"
        else:
            prompt_text += "Play"
        prompt_surf = self.clock_font.render(prompt_text, True, self.clock_color)
        prompt_rect = prompt_surf.get_rect(
            midbottom=(self.menu_rect.centerx, step_rect.top - 2 * self.border_size))
        self.screen.blit(prompt_surf, prompt_rect)

    def draw_sim(self):
        # Draw screen
        self.screen.blit(self.sim_surf, self.sim_rect)

    def draw(self):
        # This function draws the layers of the world on to the screen
        # This also creates a list of layers for the user to click on to add or remove layer displays.
        self.draw_menu()
        self.draw_sim()
        return

    def switch_state(self):
        if self.state == "Play":
            self.state = "Pause"
        else:
            self.state = "Play"

    def loop(self):
        while True:
            # Checking events in pygame.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.switch_state()

            if self.state == "Play":
                # Running one step of the loop as provided in the definition.
                # This is defined by the creator according to the needs of the simulation.
                self.loop_step()

                # updating the clock as one step is completed.
                self.clock.next_step()

            # Running the draw loop to create all the necessary layouts and surfaces
            self.draw()
            # updating the changes to the screen and limiting to 60 fps
            pygame.display.update()

            self.pyclock.tick(60)
