import random
import numpy as np
from collections import deque
import sys

'''
Here, considering number of agents to be 100
'''

class WorldEnvironment:

    global sense_state

    def __init__(self, gridSize):
        self.gridSize = gridSize
        # Initializing Grid: Create a 2D array of the world with all cells set to None (empty)
        self.grid = np.zeros(gridSize)
        
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

        WorldEnvironment.sense_state = sense_type
    
    def reset(self):
        # Reset grid to initial state
        self.grid = np.zeros(self.gridSize)
        '''
        Placing 100 ants randomly on the grid

        For testing consider 2-10
        '''
        for _ in range(10):
            row = np.random.randint(0, self.gridSize[0])
            col = np.random.randint(0, self.gridSize[1])
            self.grid[row, col] = 1
        
    def step(self, actions, next_state):
        # Reward for each agent
        rewards = np.zeros(10)         # Change to 100

        for agent in range(10):         # Change to 100
            if next_state[agent] == WorldEnvironment.sense_state[agent]:
                rewards[agent] += 1

        for i in range(10):            # Change to 100
            # Moving Up
            if actions[i] == 0 and self.grid[i // 10, i % 10] != 0:
                newRow = max(i // 10 - 1, 0)
                if self.grid[newRow, i % 10] == 0:
                    self.grid[i // 10, i % 10] = 0
                    self.grid[newRow, i % 10] = 1
            
            # Moving Down
            elif actions[i] == 1 and self.grid[i // 10, i % 10] != 0:
                newRow = min(i // 10 + 1, self.grid_size[0] - 1)
                if self.grid[newRow, i % 10] == 0:
                    self.grid[i // 10, i % 10] = 0
                    self.grid[newRow, i % 10] = 1

            # Moving Left
            elif actions[i] == 2 and self.grid[i // 10, i % 10] != 0:
                newCol = max(i % 10 - 1, 0)
                if self.grid[i // 10, newCol] == 0:
                    self.grid[i // 10, i % 10] = 0
                    self.grid[i // 10, newCol] = 1

            # Moving Right
            elif actions[i] == 3 and self.grid[i // 10, i % 10] != 0:
                newCol = min(i % 10 + 1, self.gridSize[1] - 1)
                if self.grid[i // 10, newCol] == 0:
                    self.grid[i // 10, i % 10] = 0
                    self.grid[i // 10, newCol] = 1

            # Calculating The Reward Based On The Environment
            '''
            if self.grid[i // 10, i % 10] == 1:
                rewards[i] = 1
            '''
            for j in range(10):     # Change to 100
                if next_state[i] == next_state[j]:
                    rewards[i] -= 0.5
                    rewards[j] -= 0.5

        # return rewards, self.grid.copy()
        return rewards

class ExperienceReplay:
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.buffer = deque(maxlen=buffer_size)

    def add_experience(self, experience):
        self.buffer.append(experience)

    def sample_batch(self, batch_size):
        if len(self.buffer) < batch_size:
            return None

        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, done_flags = zip(*batch)

        return states, actions, rewards, next_states, done_flags

    def size(self):
        return len(self.buffer)

    def is_full(self):
        return len(self.buffer) == self.buffer_size

    def clear(self):
        self.buffer.clear()
    pass


# Five Hidden Layer
class NeuralNetwork:
    def __init__(self, input_dim, output_dim, hidden_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_dim = hidden_dim

        # Initialize weights and biases for each agents
        self.weights = {}
        self.biases = {}

        # Create separate networks for each agent
        self.networks = []
        # Assuming each agent has its own output
        for agent in range(output_dim): 
            network = {
                'input_hidden': np.random.randn(input_dim, hidden_dim[0]),
                # Single output per agent
                'hidden_output': np.random.randn(hidden_dim[-1], 1)
            }
            self.weights[agent] = network
            self.biases[agent] = {
                'input_hidden': np.zeros((1, hidden_dim[0])),
                'hidden_output': np.zeros((1, 1))
            }
            self.networks.append(network)

    # Forward pass through the Q-Network for the specified agent
    def forward(self, state, agent):
        x = state
        for layer in range(self.num_hidden_layers):
            x = np.dot(x, self.weights[agent]['input_hidden']) + self.biases[agent]['input_hidden']
            x = np.maximum(0, x) #ReLU Activation

        q_values = np.dot(x, self.weights[agent]['hidden_output']) + self.biases[agent]['hidden_output']
        return q_values
    
    def get_weights(self, agent):
        return self.weights[agent], self.biases[agent]
    
    def set_weights(self, agent, weights, biases):
        self.weights[agent] = weights
        self.biases[agent] = biases

    '''
    # Deciding Rewards & Punishment
    def Rewards(self, location):
        self.location = location
        if location == 'Target':
            print("Reached Target")
            return 100
        
        elif location == "Home":
            print("Reached Home")
            return 200
        
        # elif location != "Home" and location != "Target":
        elif location != "Home" or location != "Target":
            return -300
             
        else:
            return -1
    '''
    

class Perceptron:
    def __init__(self, data, hidden_dim, weights = None):
        print("Perceptron with Hidden Layer Init Ran")
        random.shuffle(data)

        inputs = np.array([[float(x) for x in row[0:-1]] for row in data])
        self.inputs = np.hstack((inputs, [[1]] * len(inputs)))  # Append 1 to each input row for bias weights
        self.outputs = np.array([float(row[-1]) for row in data])
        self.num_inputs = len(self.inputs[0])

        self.hidden_dim = hidden_dim
        if weights is None:
            weights = np.array([random.uniform(0, 100) for _ in range(self.num_inputs)])
            weights[-1] = -1    # Set Initial value of bias weights
        self.weights = weights
        self.hidden_weights = np.array([random.uniform(0, 100) for _ in range(hidden_dim)])
        self.error = float(sys.maxsize)
        self.smallest_error = self.error
        self.best_weights = self.weights
        self.fit_history = []
    
    def predict(self, x_i):
        hidden_activation = np.dot(x_i, self.hidden_weights)
        hidden_output = np.maximum(hidden_activation, 0)    #  ReLU Activation
        combined = np.hstack((hidden_output, [1]))      # Append 1 for bias weights
        output = np.dot(combined, self.weights)
        if output > 0:
            return output
        else:
            return 0.01 * output

    def fit(self, state, lr=0.5, num_iters=100, break_soon=True):
        error_list = []
        for iter in range(num_iters):
            total_error = 0.0
            for i in range(len(self.outputs)):
                pred = self.predict(self.inputs[i])
                error = self.outputs[i] - pred

                self.state = state
                reward = WorldEnvironment.step()       # Called Reward function
                reward += reward
                print("Total Rewards: ", reward)

                self.weights = self.weights + lr * error * self.inputs[i]
                total_error += abs(error)

            self.save_best_fit(self.weights, total_error)
            if break_soon:
                if total_error == 0.0:
                    break
            self.print_weights()
            error_list.append(total_error)      
        
        self.fit_history = error_list
        self.error = total_error

    def save_best_fit(self, w, e):
        if e < self.smallest_error:
            self.smallest_error = e
            self.best_weights = w

    def print_weights(self):
        print("\t".join(map(str, self.weights)), file=sys.stderr)

    def test(self):
        e = 0.0
        for i in range(len(self.inputs)):
            pred = self.predict(self.inputs[i])
            e += self.outputs[i] - pred
        print(e, file=sys.stdout)

    def __str__(self) -> str:
        s = "Input (1 sample): {}\n".format(self.inputs[0])
        s += "Weights: {}\n".format(self.weights)
        s += "Hidden Weights: {}\n".format(self.hidden_weights)
        s += "Error: {}\n".format(self.error)


def main():
    # Creating The Environment
    gridSize = (10, 10)
    env = WorldEnvironment(gridSize)

    # Reset The Environment
    env.reset()

    # Simulate a few steps in the environment
    for _ in range(10):
        # Random Action for 100 agents
        actions = np.random.randint(0, 4, size=100)
        rewards, newGrid = env.step(actions)
        print("Rewards:", rewards)
        print(newGrid)