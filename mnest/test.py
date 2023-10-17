import numpy as np

class DQN:
    def __init__(self, input_dim, output_dim, hidden_dims):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_dims = hidden_dims
        self.num_hidden_layers = len(hidden_dims)

        # Initialize weights and biases for the Q-network
        self.weights = {}
        self.biases = {}
        
        # Create separate networks for each agent
        self.networks = []
        for agent in range(output_dim):  # Assuming each agent has its own output
            network = {
                'input_hidden': np.random.randn(input_dim, hidden_dims[0]),
                'hidden_output': np.random.randn(hidden_dims[-1], 1)  # Single output per agent
            }
            self.weights[agent] = network
            self.biases[agent] = {
                'input_hidden': np.zeros((1, hidden_dims[0])),
                'hidden_output': np.zeros((1, 1))
            }
            self.networks.append(network)

    def forward(self, state, agent):
        # Forward pass through the Q-network for the specified agent
        x = state
        for layer in range(self.num_hidden_layers):
            x = np.dot(x, self.weights[agent]['input_hidden']) + self.biases[agent]['input_hidden']
            x = np.maximum(0, x)  # ReLU activation
        
        q_values = np.dot(x, self.weights[agent]['hidden_output']) + self.biases[agent]['hidden_output']
        return q_values

    def get_weights(self, agent):
        return self.weights[agent], self.biases[agent]

    def set_weights(self, agent, weights, biases):
        self.weights[agent] = weights
        self.biases[agent] = biases







class PerceptronWithHiddenLayer:
    def __init__(self, data, hidden_dim, weights=None):
        print("Perceptron with Hidden Layer Init Ran")
        random.shuffle(data)

        inputs = np.array([[float(x) for x in row[0:-1]] for row in data])
        self.inputs = np.hstack((inputs, [[1]] * len(inputs)))  # Append 1 to each input row for bias weight
        self.outputs = np.array([float(row[-1]) for row in data])
        self.num_inputs = len(self.inputs[0])

        self.hidden_dim = hidden_dim
        if weights is None:
            weights = np.array([random.uniform(0, 100) for _ in range(self.num_inputs)])
            weights[-1] = -1  # Set initial value of bias weights
        self.weights = weights
        self.hidden_weights = np.array([random.uniform(0, 100) for _ in range(hidden_dim)])
        self.error = float(sys.maxsize)
        self.smallest_error = self.error
        self.best_weights = self.weights
        self.fit_history = []

    def predict(self, x_i):
        hidden_activation = np.dot(x_i, self.hidden_weights)
        hidden_output = np.maximum(hidden_activation, 0)  # ReLU activation
        combined = np.hstack((hidden_output, [1]))  # Append 1 for bias
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
                reward = PerceptronWithHiddenLayer.reward(state)
                reward += reward
                print("Total rewards:", reward)

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
        s = "Inputs (1 sample): {}\n".format(self.inputs[0])
        s += "weights: {}\n".format(self.weights)
        s += "hidden_weights: {}\n".format(self.hidden_weights)
        s += "Error: {}\n".format(self.error)
        return s
