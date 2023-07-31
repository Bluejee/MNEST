import random
from typing import Any 
import numpy as np
import sys
import h5py
import os
import pickle
# from .perceptron import *

# class NeuralNetwork(Perceptron.fit):
#     def __init__(self, state_dim, action_dim):
#         super(NeuralNetwork, self).__init__()
#         self.FirstLayer = Perceptron.predict
#         self.SecondLayer = Perceptron.predict


'''
1. Adam Optimizer
` 2. MeanSquareError `
3. QNetwork
4. DenseLayer
5. Agent
6. Neural Network

'''

global reward


class Optimizer:
    pass



class MyMeanSquareError:
    def __call__(self, y_true, y_pred):
        return np.mean(np.square(y_true - y_pred))



class ModelCheckpoint:
    # def save_model(self, model):
    #     # Save the model architecture
    #     model.save

    def __init__(self, model):
        self.model = model
        self.step_count = 0

    def saveModelWeights(self, step_count, save_path):
        # Save Model Weights
        with open(save_path + "_weights.pkl", "wb") as f:
            pickle.dump(self.model.get_weights(), f)

        # Save Step Count
        with open(save_path + "_stepCounts.pkl", "wb") as f:
            pickle.dump(self.step_count, f)

    def loadModelWeights(self, save_path):
        # Load Model Weights
        with open(save_path + "_weights.pkl", "rb") as f:
            weights = pickle.load(f)
        self.model.set_weights(weights)

        # Load Step Count
        with open(save_path + '_stepCount.pkl', "rb") as f:
            self.step_count = pickle.load(f)
    
    def incrementStepCount(self):
        self.step_count += 1

# This is Neural Network with 1 hidden layer
class Perceptron:
    def __init__(self, data, weights = None):
        print("Perceptron Init Ran")
        random.shuffle(data)
        inputs = np.array([[float(x) for x in row[0:-1]] for row in data])
        self.inputs = np.hstack((inputs, [[1]] * len(inputs))) # Append 1 to each input row, for the bias weight
        self.outputs = np.array([float(row[-1]) for row in data]) # Change no. of o/p to no. of actions 
        self.numInputs = len(self.inputs[0])

        if weights == None:
            weights = np.array([random.uniform(0, 100) \
                            for x in range(self.numInputs)])
            weights[-1] = -1        # Set initial value of bias weights
        self.weights = weights
        self.error = float(sys.maxsize)     # Initialise error to some very high value
        self.smallestError = self.error
        self.bestWeights = self.weights
        self.fitHistory = []

    def predict(self, x_i):
        # Activation functions is the dot product of input vector and weight vector
        y = np.dot(x_i, self.weights) 

        if y > 0:
            return y
        else :
            return 0.01*y
        
    '''
    def fit(self, state_dim, action_dim, learning_rate=0.001, gamma=0.99, epsilon=1.0, epsilon_decay=0.999, epsilon_min=0.01, numIters = 100, breakSoon = True):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.loss_fn = MyMeanSquareError(1, 0.83)
    '''        

    '''
    def nextMove(location, action):
        row, col = location
        if action == "UP":
            return (row - 1, col)
        elif action == "DOWN":
            return (row + 1, col)
        elif action == "LEFT":
            return(row, col - 1)
        elif action == "RIGHT":
            return(row, col + 1)
        else:
            return location
    '''

    # Deciding Rewards & Punishment
    def Reward(self, location):

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


    def fit(self, state, lr = 0.5, numIters = 100, breakSoon = True):
        errorList = []
        for iter in range(numIters):
            totalError = 0.0
            for i in range(len(self.outputs)):
                
                # Checking The Difference Between The Actual & Predicted Output
                pred = self.predict(self.inputs[i])
                # Error is the difference between true and predicted class
                error = self.outputs[i] - pred
                
                
                '''# Rewards Function'''
                # Calling Reward Function
                self.state = state
                reward = Perceptron.Reward(state)
                reward += reward
                print("Total rewards: " + reward)
                              

                # Multiplying with the error yields a positive or negative adjustment depending on a positive or negative prediction error
                self.weights = self.weights + \
                                lr * error * self.inputs[i]
                # totalError += abs(error)**2
                totalError += abs(error)
            
            self.saveBestFit(self.weights, totalError)
            if breakSoon:
                if totalError == 0.0:
                    break
            self.printWeights()
            errorList.append(totalError)
        
        # Store error history for the convenient plotting
        self.fitHistory = errorList
        self.error = totalError

        

    # Store the best performing weights for reuse
    def saveBestFit(self, w, e):
        if e < self.smallestError:
            self.smallestError = e
            self.bestWeights = w

    def printWeights(self):
        print("\t".join(map(str, self.weights)), file=sys.stderr)

    # Ideally we should split data into train/test sets to feed this method. For now, just use the data passed during initialization.
    def test(self):
        e = 0.0
        for i in range(len(self.inputs)):
            pred = self.predict(self.inputs[i])
            e += self.outputs[i] - pred
        print(e, file=sys.stdout)

    def __str__(self) -> str:
        s = "Inputs (1 sample): {}\n".format(self.inputs[0])
        s += "weights: {}\n".format(self.weights)
        s += "Error: {}\n".format(self.error)
        return s