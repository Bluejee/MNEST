import numpy as np

n = 10000
# initialize the game state environment
game_state = np.zeros((n, 30, 30))

# set the value of each cell at each time step
for t in range(n):
    game_state[t] = t * np.ones([30, 30])

# game_state = np.append(game_state, 77 * np.ones([1, 3, 3]), axis=0)


# save the updated game state to disk using savez and specifying a compression level
np.savez_compressed("game_state.npz", game_state)

# to load the game state later, you can use
loaded_game_state = np.load("game_state.npz")["arr_0"]
