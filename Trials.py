# import numpy as np
#
# n = 10000
# # initialize the game state environment
# game_state = np.zeros((n, 30, 30))
#
# # set the value of each cell at each time step
# for t in range(n):
#     game_state[t] = t * np.ones([30, 30])
#
# # game_state = np.append(game_state, 77 * np.ones([1, 3, 3]), axis=0)
#
#
# # save the updated game state to disk using savez and specifying a compression level
# np.savez_compressed("game_state.npz", game_state)
#
# # to load the game state later, you can use
# loaded_game_state = np.load("game_state.npz")["arr_0"]


import numpy as np

from scipy.signal import convolve2d
# import numpy as np
# from scipy.signal import convolve2d
#
# # Define the diffusion kernel
# diff_kernel = np.array([[0.1, 0.1, 0.1],
#                         [0.1, 0.2, 0.1],
#                         [0.1, 0.1, 0.1]])
#
# # Define the initial pheromone matrix
# pheromones = np.array([[0, 0, 0, 0, 0],
#                        [0, 100, 100, 100, 0],
#                        [0, 100, 100, 100, 0],
#                        [0, 100, 100, 100, 0],
#                        [0, 0, 0, 0, 0]])
#
# for i in range(100):
#     print(pheromones)
#     temp = convolve2d(pheromones, diff_kernel, mode='same')
#     print(temp)
#     pheromones = temp


from pygame.math import Vector2

direct = Vector2(1, 0)

surroundings = [[1, 0],
                [1, 1],
                [0, 1],
                [-1, 1],
                [-1, 0],
                [-1, -1],
                [0, -1],
                [1, -1]]

front = surroundings[surroundings.index(list(direct))]
front_left = surroundings[(surroundings.index(list(direct)) + 1) % 8]
front_right = surroundings[(surroundings.index(list(direct)) - 1) % 8]
print(front_left, front, front_right)
