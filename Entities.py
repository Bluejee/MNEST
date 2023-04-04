import numpy as np
from scipy.signal import convolve2d

from Laws import *


class Agent:
    def __init__(self, world, layer_name, child, position: Vector2 = Vector2(0, 0), direction=E,
                 brain_type='Q-Table', action_list=('move', 'stay')):

        self.world = world
        self.layer_name = layer_name
        self.child = child

        self.position = position
        self.direction = np.copy(direction)
        # as Right is a list, it is inherited as a pointer and hence we have to make a copy to avoid problems.

        # Fun Fact.
        # As We are storing the position of the element inside the layer. and not a copy of the values.
        # It is stored as a reference and hence we do not have to update the world values everytime.
        # Frankly for all those who are reading this. I was about to write code to update the values when I accidentally
        # ran the simulation to test and saw them updating automatically.
        # I jumped* up and down around the room (* Literally.)
        self.world.layers[self.layer_name] = [position, *self.world.layers[self.layer_name]]

        # Variables to make the agent autonomous
        self.action_list = action_list
        self.brain = Brain(brain_type, self.action_list)
        self.state_hash = ''
        self.current_observed_state = None
        self.selected_action = None
        self.result_observed_state = None
        self.earned_reward = None

    def update(self):
        """
        This function updates the state list so that the sense can work correctly.
        (Can be overwritten by the child.)
        :return:
        """
        print('Hi im here probably you should probably check if you performed the override',
              'on the update function in the child')

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

    def sense_state(self, sense_type):
        """

        :param sense_type:
        :return:
        """
        # first update the state_list then sense the state.
        self.update()

        if sense_type == 'Initial':
            self.current_observed_state = self.state_hash
            # print('initial', self.current_observed_state, self.result_observed_state)
        elif sense_type == 'Final':
            self.result_observed_state = self.state_hash
            # print('final', self.current_observed_state, self.result_observed_state)
        else:
            print('Something seems wrong with the sense type given.')

    def perform_action(self):
        self.selected_action = self.action_list[self.brain.predict_action(self.current_observed_state)]
        eval('self.child.' + self.selected_action + '()')

    def earn_reward(self, reward):
        self.earned_reward = reward

    def learn(self):
        self.brain.learn(state_observed=self.current_observed_state,
                         action_taken=self.action_list.index(self.selected_action),
                         next_state=self.result_observed_state,
                         reward_earned=self.earned_reward)


class Essence:
    def __init__(self, world, layer_name,
                 dispersion_matrix=np.array([[0.01, 0.01, 0.01],
                                             [0.01, 0.92, 0.01],
                                             [0.01, 0.01, 0.01]]), decay_rate=0):
        self.world = world
        self.layer_name = layer_name
        self.max_value = self.world.layer_data[layer_name][3]
        self.decay_rate = decay_rate
        self.dispersion_matrix = dispersion_matrix

    def disperse(self):
        """
        Uses matrices and convolutions to disperse the essence
        In general the rule of thumb is that the dispersion matrix con have values where the total of the values is 1.
        Also, the sum of all values that is dispersed(Total - Center_Value) = 1 - Center_Value. of the matrix
        # we need the original layer
        :return:
        """

        self.world.layers[self.layer_name] = convolve2d(self.world.layers[self.layer_name], self.dispersion_matrix,
                                                        mode='same')

    def decay(self):
        # This is usually not something that we need to use in simulations unless we have periodic boundaries or so.
        # Usually, things disperse and then go out of the edge of the world.
        self.world.layers[self.layer_name] -= self.decay_rate
        # check if any value went below 0 and if so set it to 0.
        mask = self.world.layers[self.layer_name] < 0
        self.world.layers[self.layer_name][mask] = 0


# AI for the Entities.
class Brain:
    def __init__(self, brain_type: str, action_list: list, learning_rate=0.2,
                 exploration_rate=0.1, discounted_return=0.5, exploration_decay=0.01, min_exploration=0):

        self.brain_type = brain_type
        self.action_list = action_list

        # Learning Parameters
        self.learning_rate = learning_rate  # Alpha
        self.exploration_rate = exploration_rate  # Epsilon
        self.exploration_decay = exploration_decay  # Epsilon Decay
        self.min_exploration = min_exploration
        self.discounted_return = discounted_return  # Gamma or Lambda

        if self.brain_type == 'Q-Table':
            self.q_table = {}
        elif self.brain_type == 'Deep-Q':
            pass
        else:
            print('There seems to be some mistake on the brain type.')

    def add_state(self, state: str):
        """
        This function is applicable to the Q-Table type Brain.
        (If a state being asked for doesn't exist) It populates the Q-Table with a new key value pair.
        :param state: The state for which the new state is to be added.
        :return:
        """
        self.q_table[state] = np.zeros(len(self.action_list))

        # Sort the dictionary by its keys alphabetically
        self.q_table = dict(sorted(self.q_table.items()))

    def predict_action(self, state: str):
        """
        This function takes in a state and predicts an action based on the brain.
        :param state: The state for which the action is to be predicted
        :return: a number between 0 and number of actions to act as an index.
        """
        if self.brain_type == 'Q-Table':
            if state in self.q_table:
                q_values = self.q_table[state]  # q_values for that state
                predict_list = np.where(q_values == max(q_values))[0]  # list of all indices with max q_values
                action = np.random.choice(predict_list)
                # print('State_found')
            else:
                self.add_state(state)
                action = np.random.randint(len(self.action_list))
                # action = 0
                # print('New_state')
        elif self.brain_type == 'Deep-Q':
            action = 0
            pass

        else:
            action = None
            print('There seems to be some mistake on the brain type.')
        # print(len(self.q_table), self.q_table.keys())
        # print(action)
        return action

    def learn(self, state_observed: str, action_taken: int, next_state: str, reward_earned: float):
        """

        :param next_state:
        :param state_observed:
        :param action_taken:
        :param reward_earned:
        :return:
        """
        if self.brain_type == 'Q-Table':
            # There is a possibility that the new state does not exist in the q table.
            if next_state not in self.q_table:
                self.add_state(next_state)

            values_state_observed = self.q_table[state_observed]
            values_next_state = self.q_table[next_state]

            learned_value = reward_earned + self.discounted_return * (max(values_next_state))
            new_value = ((1 - self.learning_rate) * values_state_observed[action_taken] +
                         self.learning_rate * learned_value)
            values_next_state[action_taken] = new_value

        elif self.brain_type == 'Deep-Q':
            pass
        else:
            print('There seems to be some mistake on the brain type.')
            pass
