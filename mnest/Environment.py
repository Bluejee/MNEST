import numpy as np
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "True"
import pygame

"""
This file contains the classes that create the environment.
This would contain the Clock, The World, and the God's Perspective(Realise).
"""

data_file_path = os.path.join(os.path.dirname(__file__), 'data', 'random_seed.txt')
seed = int(np.genfromtxt(data_file_path))
np.random.seed(seed)


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


    The layer for a BlockElement is stored as an empty numpy array with each element being a [x,y].
    The layer for a FloatElement is stored as a NxM matrix with each element storing the value for the cell.


    """

    def __init__(self, layer_data: dict, r_length=30, c_length=30, periodic_boundary=False):
        """

        :param layer_data: data of the form
        {'layer_label': ['Layer_type(Block/Float)', (R, G, B), 'Path_for_sprite_image/None',
        In case of Float a max value to calculate %]}
        :param r_length: number of rows of the world.
        :param c_length: number of columns of the world.
        :param periodic_boundary: weather or not the world has a periodic boundary.
        """
        self.r_length = r_length  # no of rows
        self.c_length = c_length  # no of columns
        self.periodic_boundary = periodic_boundary
        self.layer_data = layer_data
        self.layers = {}

        for label in self.layer_data:
            if layer_data[label][0] == 'Block':
                self.layers[label] = np.array([], dtype=int)  # formation of one layer of Block

            elif layer_data[label][0] == 'Float':
                self.layers[label] = np.zeros([self.r_length, self.c_length])  # formation of one layer
                # r represents the vertical(row number) and c the horizontal(column number).


class Realise:
    """
    This is the class used to visualise the environment/simulation.
    """

    def __init__(self, world: World, child, visualise=True, frame_rate_cap=60, cell_size=20, border_size=2,
                 clock_color=(56, 74, 12), sim_text_color=(119, 21, 167),
                 sim_background=(89, 187, 247), menu_background=(0, 255, 0), border_color=(255, 0, 0)):

        # Child variable.
        self.child = child

        # Simulation Variables
        self.quit_sim = False
        self.world = world
        self.clock = Clock()

        # Everything that deals with Visualisations go under this if statement.
        self.visualise = visualise
        if self.visualise:
            pygame.init()

            self.state = "Pause"  # The visualisation starts at the paused state.
            self.frame_rate_cap = frame_rate_cap
            # Visualisation Variables
            self.pyclock = pygame.time.Clock()
            self.cell_size = cell_size

            self.border_size = border_size  # border goes around the simulation
            self.border_color = border_color

            self.sim_width = (self.cell_size * self.world.c_length)  # width = no of columns * cell_size
            self.sim_height = (self.cell_size * self.world.r_length)  # height = no of rows * cell_size

            self.menu_width = int(self.sim_width / 3)

            self.screen_height = self.sim_height + 2 * self.border_size
            self.screen_width = self.sim_width + self.menu_width + 2 * self.border_size

            self.menu_background = menu_background
            self.sim_background = sim_background

            # Surface and Display Variables
            # Screen
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            self.screen.fill(self.border_color)

            # Title 
            self.title = pygame.display.set_caption('MNEST Window')

            # This creates a dictionary with keys being layer names and the value containing a class which contains
            # information on how to display and if to display the layer.
            self.display_layers = {
                layer: DisplayLayers(layer_data=self.world.layer_data[layer], cell_size=self.cell_size)
                for layer in self.world.layer_data}
            # Menu
            self.menu_surf = pygame.Surface((self.menu_width, self.screen_height))
            self.menu_rect = self.menu_surf.get_rect(topright=(self.screen_width, 0))
            self.menu_surf.fill(self.menu_background)

            # Simulation
            self.sim_surf = pygame.Surface((self.sim_width, self.sim_height))
            self.sim_rect = self.sim_surf.get_rect(topleft=(self.border_size, self.border_size))
            self.sim_surf.fill(self.sim_background)
            self.show_sim = False

            # Text Fonts
            self.all_font = pygame.font.Font(None, 25)
            self.clock_font = pygame.font.Font(None, 25)
            self.sim_font = pygame.font.Font(None, 40)

            # Clock/Step text
            self.clock_color = clock_color

            # Visualisation State Text
            self.sim_text_color = sim_text_color

            # At the end of Initialisation, we have to draw the sim_pause to show the pause screen at the start.
            if not self.show_sim:
                self.draw_sim_pause()

    def draw_menu(self):
        """
        Documentation to be corrected.
        This function draws the menu surface of the visualisation. it does the following.
        1. It shows the simulation clock and allows the user to play and pause the simulation.
        2. It allows the user to select which all layers are to be displayed.
            2.1 This happens only if the number of layers can be displayed on the menu.
            2.2 If the number is too large it can read from a file the list of layers to be displayed. (Future update*)

        :return:
        """
        # Draw menu background
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

        # Analyse Prompt.

        analyse_prompt_text = 'Press <a> to run Analysis.'

        analyse_prompt_surf = self.clock_font.render(analyse_prompt_text, True, self.clock_color)
        analyse_prompt_rect = analyse_prompt_surf.get_rect(
            midbottom=(self.menu_rect.centerx, prompt_rect.top - 2 * self.border_size))
        self.screen.blit(analyse_prompt_surf, analyse_prompt_rect)

    def draw_sim(self):
        # This function draws the layers of the world on to the screen
        # Draw simulation Background
        self.screen.blit(self.sim_surf, self.sim_rect)

        # going through every layer
        for layer_name in self.display_layers:
            layer: DisplayLayers
            # This is a type set. i.e. helping to know that the layer variable is of the DisplayLayers class
            # Not at all necessary but helps in debugging and getting docs on the fly

            layer = self.display_layers[layer_name]
            if layer.active:
                # taking the values from the world.
                layer_values = self.world.layers[layer_name]

                # We are now in the active layer.
                # We create a surface for this layer so that we can have transparency working.
                layer_surf = pygame.Surface((self.sim_width, self.sim_height), pygame.SRCALPHA)
                # We can use the sim_rect to place the layer_surf as both are basically the same thing.

                # We check if the layer is a block type or a float type and then act accordingly.
                if layer.layer_type == 'Block':
                    # Block type layer
                    # We go through all the coordinates in the layer
                    for [x, y] in layer_values:
                        location = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                        layer.draw_cell(value=1, surface=layer_surf, location=location)
                elif layer.layer_type == 'Float':
                    # Block type layer
                    # We go through all cells of the layer.
                    for x in range(self.world.c_length):
                        for y in range(self.world.r_length):
                            # we are now at a cell in the layer
                            # location and size to draw the cell = (x,y,w,h)
                            location = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                            layer.draw_cell(value=layer_values[y, x], surface=layer_surf, location=location)
                            # layer.draw_cell(value=np.random.randint(100), surface=layer_surf, location=location)

                # Now that all cells have been drawn, we blit the layer_surf on to the screen
                self.screen.blit(layer_surf, self.sim_rect)

            # Adding the hide visualisation text if the sim is visible on to the menu.
            prompt_text = 'Press the <v> Key to hide Visualisation.'

            prompt_surf = self.all_font.render(prompt_text, True, self.sim_text_color)
            prompt_rect = prompt_surf.get_rect(midtop=(self.sim_rect.centerx, self.sim_rect.top + 2 * self.border_size))

            self.screen.blit(prompt_surf, prompt_rect)

    def draw_sim_pause(self):
        # Draw simulation Background
        self.screen.blit(self.sim_surf, self.sim_rect)

        # Pause Prompt.
        pause_prompt_text = 'Press the <v> Key to Show Visualisation.'
        pause_prompt_surf = self.sim_font.render(pause_prompt_text, True, self.sim_text_color)
        pause_prompt_rect = pause_prompt_surf.get_rect(midbottom=(self.sim_rect.centerx, self.sim_rect.centery))

        self.screen.blit(pause_prompt_surf, pause_prompt_rect)

        # Pause Info.
        pause_info_text = '(The simulation runs faster without visualisation)'
        pause_info_surf = self.all_font.render(pause_info_text, True, self.sim_text_color)
        pause_info_rect = pause_info_surf.get_rect(midtop=pause_prompt_rect.midbottom)

        self.screen.blit(pause_info_surf, pause_info_rect)

    def draw(self):
        # This function draws the menu and the simulation surfaces.
        self.draw_menu()
        if self.show_sim:
            self.draw_sim()
        return

    def switch_state(self):
        if self.state == "Play":
            self.state = "Pause"
        else:
            self.state = "Play"

    def run_sim(self):
        """
        This Selects the Command line mode or the Visualisation mode.
        :return:
        """
        if self.visualise:
            self.loop()
        else:
            self.no_visualisation()

    def no_visualisation(self):
        """
        This is equivalent to the loop() but has no visualisation at all.
        :return:
        """
        print('Command Line Version: Visualisation turned off.')
        while True:
            if self.quit_sim:
                # exit the loop when requested.
                print('\rExiting Simulation.')
                return
            else:
                # Running one step of the loop as provided in the definition.
                # This is defined by the creator according to the needs of the simulation.
                self.child.loop_step()
                # updating the clock as one step is completed.
                self.clock.next_step()

    # def loop(self, loop_step):
    def loop(self):

        # Running the draw and update functions once to show initial state.
        # Running the draw loop to create all the necessary layouts and surfaces
        self.draw()
        # updating the changes to the screen
        pygame.display.update()

        while True:
            # Checking events in pygame.
            if self.quit_sim:
                pygame.quit()
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('\nExiting Simulation.')
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    # Pause and Play Simulation.
                    if event.key == pygame.K_SPACE:
                        self.switch_state()
                        self.draw()
                        pygame.display.update()

                    # Show and Hide visualisation.
                    if event.key == pygame.K_v:
                        self.show_sim = not self.show_sim
                        # check and display visualisation paused msg.
                        if not self.show_sim:
                            self.draw_sim_pause()
                            # updating the changes to the screen
                            pygame.display.update()
                        else:
                            # This is necessary only cause the simulation starts with a paused sim visualisation.
                            self.draw()
                            # updating the changes to the screen
                            pygame.display.update()

                    if event.key == pygame.K_a:
                        self.analyse()

            if self.state == "Play":
                # Running the draw loop to create all the necessary layouts and surfaces
                self.draw()
                # updating the changes to the screen and limiting to 60 fps
                pygame.display.update()

                # Running one step of the loop as provided in the definition.
                # This is defined by the creator according to the needs of the simulation.
                self.child.loop_step()

                # updating the clock as one step is completed.
                self.clock.next_step()

            self.pyclock.tick(self.frame_rate_cap)

    def analyse(self, **kwargs):
        """
        This function runs all the analysis for the realisation.
        (Can be overwritten by the child.)

        If using <a> to run analysis. Do not use the keyword arguments. I have not found a way to provide it yet.
        else make sure to provide default values to avoid the error.
        :return:
        """
        print('Hi im here probably you should probably check if you performed the override',
              'on the update function in the child')


class DisplayLayers:
    def __init__(self, layer_data, cell_size):
        self.layer_type = layer_data[0]
        self.color = layer_data[1]
        self.sprite_image = layer_data[2]
        if self.layer_type == 'Float':
            self.max_value = layer_data[3]
        if self.sprite_image != 'None':
            self.sprite_image = pygame.image.load(self.sprite_image).convert_alpha()
            self.sprite_image = pygame.transform.scale(self.sprite_image, (cell_size, cell_size))
        self.t_factor = 1  # Transparency factor for the sprites.
        self.active = 1

    def draw_cell(self, value, surface, location):
        """
        This function draws the cell with the element depending upon the type.
        it also checks if a sprite image is to be drawn.

        *This Assumes that the sprite images that are used have the same dimensions as the cell_size*

        :param value: the value/transparency for the cell
        :param surface: layer surface on which the cells are to be drawn
        :param location: the position and size of the cell for the rect to be placed.
        :return:
        """
        if self.layer_type == 'Block':
            if value == 1:
                if self.sprite_image == 'None':
                    # If there is no sprite image to be shown.
                    # Draw the block
                    pygame.draw.rect(surface, self.color, location)
                else:
                    # Show the sprite at the cell
                    sprite_rect = pygame.Rect(location)
                    surface.blit(self.sprite_image, sprite_rect)

        elif self.layer_type == 'Float':
            if self.sprite_image == 'None':
                # If there is no sprite image to be shown.
                # Draw the Float
                transparency = int(self.t_factor * (value / self.max_value) * 255)
                pygame.draw.rect(surface, (*self.color, transparency), location)
            else:
                # Show the sprite at the cell
                # Setting transparency value
                transparency = int(self.t_factor * (value / self.max_value) * 255)
                self.sprite_image.set_alpha(transparency)
                sprite_rect = pygame.Rect(location)
                surface.blit(self.sprite_image, sprite_rect)

        else:
            print("ERROR!!!")
            print("This should not have happened.")
            print("It seems like you have misrepresented a layer.")
            print("Check the Definition of the World and check if all layers are either Block or Float.")
            exit()
