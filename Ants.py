from Environment import World, Realise
from Entities import Agent, Essence
from Laws import *
import random
import matplotlib.pyplot as plt
import numpy as np
import time
import argparse

start_time = time.time()
parser = argparse.ArgumentParser(description='Run The ants simulation.')
parser.add_argument('-ns', '--no_show', action='store_true',
                    help='Activate Command Line Mode(No Visualisation)')
parser.add_argument('--start_as', type=str, default='Play', help='Weather the simulation starts (Play)ing or (Pause)d')
parser.add_argument('--sim_name', type=str, default='Default_sim', help='Name of the sim to create files and logs')
parser.add_argument('--max_steps', type=int, default=80000, help='Maximum number of steps to be taken')
parser.add_argument('--min_exploration', type=float, default=0.01)
parser.add_argument('--exploration_rate', type=float, default=0.9)
parser.add_argument('--exploration_decay', type=float, default=0.000005)
parser.add_argument('--learning_rate', type=float, default=0.5)
parser.add_argument('--discounted_return', type=float, default=0.4)
parser.add_argument('--drop_amount', type=float, default=0.05)
parser.add_argument('--dispersion_rate', type=float, default=0.1)
parser.add_argument('--decay_rate', type=float, default=0.03)

args = parser.parse_args()
"""
This is the  code file. The following is a sample template that can be modified inorder to create any type 
of simulations. This version uses inheritance to work through everything avoiding duplication and other issues.

Note : Maybe start custom variables with an _ or some identifier to prevent accidental renaming of variables.
(Or just keep in mind the parent class and not rename variables)

Run like this::
python Ants.py --no_show --start_as='Play' --max_steps=1000 --sim_name='Hope_this_works' --min_exploration=0.05 --exploration_rate=0.9 --exploration_decay=0.0001 --learning_rate=0.4 --discounted_return=0.85
"""
seed = int(np.genfromtxt('random_seed.txt'))
random.seed(seed)
np.random.seed(seed)


def progress_bar(progress, total):
    percent = 100 * (progress / total)
    bar = '*' * int(percent) + '-' * (100 - int(percent))
    print('\r' + '\033[33m' + f'|{bar}| {percent:.2f}%' + '\033[0m', end='\r')
    if progress == total:
        print('\r' + '\033[32m' + f'|{bar}| {percent:.2f}%' + '\033[0m')


class Ant(Agent):

    # Initialise the parent class. Make sure to initialise it with the child as self.
    def __init__(self, world, layer_name, position: Vector2 = Vector2(0, 0),
                 min_exploration=0.05,
                 exploration_rate=0.9,
                 exploration_decay=0.0001,
                 learning_rate=0.4,
                 discounted_return=0.85):
        super().__init__(world=world, layer_name=layer_name, child=self, position=position,
                         action_list=['move_random', 'go_home', 'go_target', 'drop_home', 'drop_target'])
        self.food_count = 0
        self.has_food = False
        self.steps_since_pheromone_drop = 0
        self.home_likeness = 1  # How much the current cell is like Home according to the home pheromone
        self.target_likeness = 0  # How much the current cell is like Target according to the target pheromone
        # state_list = 'If the ant has food'+                        (True/False)
        #               'time since dropping the last pheromone.'+   (0,1,...4)
        #               'how much is the cell like home'+            (0,1,2,3,4,...9)
        #               'how much is the cell like target'           (0,1,2,3,4,...9)
        self.max_states = (2 * 5 * 5 * 5)
        self.state_hash = ''  # it is a hash that represents the state the ant exists in.

        # Learning Parameters
        self.brain.min_exploration = min_exploration
        self.brain.exploration_rate = exploration_rate
        self.brain.exploration_decay = exploration_decay
        self.brain.learning_rate = learning_rate
        self.brain.discounted_return = discounted_return
        ################################################################################################################
        # to populate the entire state space. This will speed up the simulation.
        full_state_table = {}
        for _ant_food in [True, False]:
            for _time_drop in [0, 1, 2, 3, 4]:
                for _like_home in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    for _like_target in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                        state = (f'{_ant_food}_' +
                                 f'{_time_drop}_' +
                                 f'{_like_home}_' +
                                 f'{_like_target}')
                        # print(state)
                        full_state_table[state] = np.zeros(len(self.action_list))

        self.brain.q_table = dict(sorted(full_state_table.items()))
        ################################################################################################################

    def reset_position(self):
        self.position += (Vector2(random.choice(self.world.layers['Home'])) - self.position)
        # It has to be done this way because, the position is stored as a reference in the layer.
        # doing something like self.position = something new
        # will destroy the link between the layer and the variable. Hence, we change the referenced variable
        # and not replace it.

    def update(self):
        """
        This updates the state_hash of the ant.
        :return:
        """
        # Check Home Likeness
        if self.position in self.world.layers['Home']:
            home_likeness = 1
        else:
            home_likeness = (self.world.layers['Pheromone_Home'][int(self.position.y), int(self.position.x)] /
                             self.world.layer_data['Pheromone_Home'][3])

        # Check Target Likeness
        if self.position in self.world.layers['Target']:
            target_likeness = 1
        else:
            target_likeness = (self.world.layers['Pheromone_Target'][int(self.position.y), int(self.position.x)] /
                               self.world.layer_data['Pheromone_Target'][3])
        # self.state_hash = (f'{self.has_food}_' +
        #                    f'{self.steps_since_pheromone_drop}_' +
        #                    f'{round(home_likeness, 1):.1f}_' +
        #                    f'{round(target_likeness, 1):.1f}')

        self.state_hash = (f'{self.has_food}_' +
                           f'{self.steps_since_pheromone_drop}_' +
                           f'{round(home_likeness * 10)}_' +
                           f'{round(target_likeness * 10)}')
        # print(self.state_hash)
        # print(self.state_hash)

    def drop_pheromone(self, pheromone_type, quantity):
        pheromone_type = 'Pheromone_' + pheromone_type  # for simplicity
        self.world.layers[pheromone_type][int(self.position.y), int(self.position.x)] += quantity

        # capping pheromone at a cell to max value
        max_pheromone = self.world.layer_data[pheromone_type][3]
        pheromone_value = self.world.layers[pheromone_type][int(self.position.y), int(self.position.x)]
        if pheromone_value > max_pheromone:
            self.world.layers[pheromone_type][int(self.position.y), int(self.position.x)] = max_pheromone
            # print(w.layers['Pheromone'][0])

    def move_to_pheromone(self, pheromone_type):
        # move to the cell around it having the maximum value for the  Pheromone in the forward direction.
        aim = pheromone_type
        pheromone_type = 'Pheromone_' + pheromone_type  # for simplicity
        pheromone_layer = self.world.layers[pheromone_type]

        move_directions = []
        max_pheromone_value = 0
        # print(self.direction, DIRECTIONS)
        front_index = self.position + front(self.direction)
        front_left_index = self.position + front_left(self.direction)
        front_right_index = self.position + front_left(self.direction)

        for check_direction in [front_left_index, front_index, front_right_index]:
            if (0 <= check_direction.x < self.world.c_length) and (0 <= check_direction.y < self.world.r_length):
                # now we know the direction is possible.

                # Directly select direction if it is home or target.
                if check_direction in self.world.layers[aim]:
                    if max_pheromone_value < 2:
                        # This is the first aim cell we find.
                        # Discard all other directions.
                        move_directions = [check_direction - self.position]
                        max_pheromone_value = 2
                    else:
                        # Append new aim cells to the list.
                        move_directions = [check_direction - self.position, *move_directions]  # .

                # The following won't work once an aim cell is found.
                pheromone_value = pheromone_layer[int(check_direction.y), int(check_direction.x)]
                if pheromone_value > max_pheromone_value:
                    move_directions = [check_direction - self.position]  # we only need one direction if its max
                    max_pheromone_value = pheromone_value

                elif pheromone_value == max_pheromone_value:
                    move_directions = [check_direction - self.position, *move_directions]  # appends to the list.

        # now we have checked through all 3 forward directions.

        if len(move_directions) == 0:
            # it means there is no way forward.
            # self.direction = reflect(self.direction) This needs to be solved.
            self.direction = -self.direction

        else:
            # it means there is one or more of the directions to move towards.
            self.direction = random.choice(move_directions).copy()
            self.move()

    def move_random(self):
        self.direction = random.choice(DIRECTIONS).copy()
        self.move()

    def go_home(self):
        self.move_to_pheromone(pheromone_type='Home')

    def go_target(self):
        self.move_to_pheromone(pheromone_type='Target')

    def drop_home(self):
        self.drop_pheromone(pheromone_type='Home', quantity=args.drop_amount)

    def drop_target(self):
        self.drop_pheromone(pheromone_type='Target', quantity=args.drop_amount)


# Setting up the Visualiser.
class Visualise(Realise):
    def __init__(self):
        # To Set up the Visualisation, Initialise the class with the World, required variables, and the one_step_loop
        # Initialise the world with necessary size and layers.
        # It is not recommended that the number of layers be more than 10
        # It Might cause errors within the visualisation.
        # The simulation will however work fine. just that the option for selecting layers will be disabled

        # Create the necessary layers.
        layers = {'Pheromone_Target': ['Float', (250, 10, 50), 'None', 1],
                  'Pheromone_Home': ['Float', (85, 121, 207), 'None', 1],
                  'Ants': ['Block', (255, 0, 0), 'Stock_Images/ant_sq.png'],
                  'Home': ['Block', (50, 98, 209), 'None'],
                  'Target': ['Block', (204, 4, 37), 'None']}

        # Initialise the parent class. Make sure to initialise it with the child as self.
        # Adjust set parameters
        super().__init__(world=World(layer_data=layers, r_length=30, c_length=30), child=self,
                         visualise=not args.no_show, frame_rate_cap=600, cell_size=25, sim_background=(255, 255, 255))
        self.state = args.start_as
        self.max_steps = args.max_steps
        self.sim_name = args.sim_name
        # Set up the new variables and performing initial setups.
        self.world.layers['Home'] = [[15, 15], [16, 16], [15, 16], [16, 15]]
        self.world.layers['Target'] = [[10, 10], [9, 9], [10, 9], [9, 10]]

        self.ant_list = [Ant(world=self.world,
                             layer_name='Ants',
                             position=Vector2(random.choice(self.world.layers['Home']))) for _ in range(30)]
        dispersion_rate = args.dispersion_rate  # percentage of pheromone to be dispersed.
        # calculate it like this, maybe. if 0.1 of the pheromone is to be dispersed then,

        dispersion_matrix = np.array([[dispersion_rate / 8, dispersion_rate / 8, dispersion_rate / 8],
                                      [dispersion_rate / 8, 1 - dispersion_rate, dispersion_rate / 8],
                                      [dispersion_rate / 8, dispersion_rate / 8, dispersion_rate / 8]])
        self.pheromone_a = Essence(self.world, 'Pheromone_Home', dispersion_matrix=dispersion_matrix,
                                   decay_rate=args.decay_rate)
        self.pheromone_b = Essence(self.world, 'Pheromone_Target', dispersion_matrix=dispersion_matrix,
                                   decay_rate=args.decay_rate)

        # Graphing Variables
        self.max_states_explored = {}
        self.food_collected = {}
        self.action_distribution = {}
        # {Time_step: ['move_random', 'go_home', 'go_target', 'drop_home', 'drop_target']}

        # Do not add any variables after calling the loop. it will cause object has no attribute error when used.
        self.run_sim()

    def reset(self):
        for ant in self.ant_list:
            # print(ant.position, type(ant.position))
            # ant.position = Vector2(random.choice(self.world.layers['Home'])).copy()
            # print(ant.position, type(ant.position))
            ant.has_food = False
            ant.reset_position()
        for layer_type in ['Home', 'Target']:
            # for position in self.world.layers[layer_type]:
            # print(type(self.world.layers['Pheromone_' + layer_type]))
            self.world.layers['Pheromone_' + layer_type] *= 0
        return

    # Create one step of the event loop that is to happen. i.e. how the world changes in one step.
    def loop_step(self):
        """
        This function is passed to the realise class to be run everytime the loop iterates.
        Basically this function is the entire set of changes that are to happen to the world.
        :return:
        """
        # # Resetting the world
        # if self.clock.time_step % 5000 == 0:
        #     self.reset()

        self.food_collected[self.clock.time_step] = np.zeros(len(self.ant_list))
        self.action_distribution[self.clock.time_step] = np.zeros(len(self.ant_list[0].action_list))
        # Iterating over all ants.
        for index, ant in enumerate(self.ant_list):

            # use random and not np.random to use objects and not a np array.
            # if self.clock.time_step < 50000:
            if True:
                ant.sense_state('Initial')
                ant.perform_action()
                ant.sense_state('Final')

                self.action_distribution[self.clock.time_step][ant.action_list.index(ant.selected_action)] += 1

                if ant.selected_action in ['drop_home', 'drop_target']:
                    ant.steps_since_pheromone_drop = 0
                else:
                    ant.steps_since_pheromone_drop = (ant.steps_since_pheromone_drop + 1) % 5

                # Check food:

                # Calculate Reward and food count.
                if ant.position in self.world.layers['Home']:
                    if ant.has_food:
                        reward = 100
                        ant.has_food = False
                        ant.food_count += 1
                        # new_array = self.food_collected[self.clock.time_step]
                        # new_array[index] = index + 1
                        self.food_collected[self.clock.time_step][index] = 1
                    else:
                        reward = -5
                        pass
                elif ant.position in self.world.layers['Target']:
                    if ant.has_food:
                        reward = -5
                    else:
                        ant.has_food = True
                        reward = 5
                    # reward = -1

                    # print('Empty ant in target')
                # elif ant.has_food and ant.selected_action == 'drop_target':
                #     reward = -3
                # elif not ant.has_food and ant.selected_action == 'drop_home':
                #     reward = -3
                # elif ant.selected_action in ['drop_home', 'drop_target']:
                #     reward = -2
                else:
                    reward = 0

                ant.earn_reward(reward)
                ant.learn()
                # ant.selected_action = random.choice(ant.action_list)
                # print(max([len(ant.brain.q_table) for ant in self.ant_list]))
                # self.max_states_explored[self.clock.time_step] = max([len(ant.brain.q_table) for ant in self.ant_list])
                # self.food_collected[self.clock.time_step] = [ant.food_count for ant in self.ant_list]
        self.pheromone_a.decay('Percentage')
        self.pheromone_b.decay('Percentage')
        self.pheromone_a.disperse()
        self.pheromone_b.disperse()

        # # Let the home and the target give off a very small amount of pheromone
        # for layer_type in ['Home', 'Target']:
        #     for position in self.world.layers[layer_type]:
        #         # print(type(self.world.layers['Pheromone_' + layer_type]))
        #         self.world.layers['Pheromone_' + layer_type][position[1], position[0]] += 0.01
        #         if self.world.layers['Pheromone_' + layer_type][position[1], position[0]] > 1:
        #             self.world.layers['Pheromone_' + layer_type][position[1], position[0]] -= 0.01

        if self.clock.time_step % 5000 == 0:
            progress_bar(self.clock.time_step, self.max_steps)

        if self.clock.time_step >= self.max_steps:
            # do not use <a>. to analyse if using kwargs.
            self.analyse()
            print('Verify reproducibility by confirming this exact number.')
            print(f'Hash for this run :: {np.random.random()}')
            self.quit_sim = True

    def analyse(self, **kwargs):
        trial = np.array(list(self.ant_list[0].brain.q_table.values()))
        np.savetxt('trial.csv', trial, delimiter=',')
        food = np.array(list(self.food_collected.values()))
        actions = np.array(list(self.action_distribution.values()), dtype=int)

        food_per1000 = {}
        sum_1000 = np.zeros_like(food[0])
        for i, row in enumerate(food):
            sum_1000 += row
            if i % 1000 == 0:
                food_per1000[i] = sum_1000
                sum_1000 = np.zeros_like(row)

        actions_per1000 = {}
        sum_1000 = np.zeros_like(actions[0], dtype=int)
        for i, row in enumerate(actions):
            sum_1000 += row
            if i % 1000 == 0:
                actions_per1000[i] = sum_1000
                sum_1000 = np.zeros_like(row, dtype=int)

        fig_1 = plt.figure(1)
        food_per1000_values = np.array(list(food_per1000.values()))
        food_per1000_values = np.sum(food_per1000_values, axis=1)
        plt.plot(food_per1000.keys(), food_per1000_values, '-.')
        fig_1.savefig('Analysis/' + self.sim_name + '_foodper1000' + '.png')

        fig_2 = plt.figure(2)
        actions_per1000_values = np.array(list(actions_per1000.values()))

        # Define the names of the actions
        action_names = self.ant_list[0].action_list

        # Compute the cumulative sums of the action counts for each time step
        cumulative_counts = np.cumsum(actions_per1000_values, axis=1)
        # Create a stacked bar plot
        for i in range(len(action_names) - 1, -1, -1):
            plt.plot(range(cumulative_counts.shape[0]), cumulative_counts[:, i], '-.')
        plt.legend(action_names)
        plt.title('Action_Distribution')
        plt.xlabel('Time Step')
        plt.ylabel('Counts')
        fig_2.savefig('Analysis/' + self.sim_name + '_actionper1000' + '.png')
        print('Analysis/' + self.sim_name + '_actionper1000' + '.png')

# Instantiating the realisation/ Gods Perspective
realise = Visualise()
end_time = time.time()
print(f'Time for execution :: {end_time - start_time}s')
