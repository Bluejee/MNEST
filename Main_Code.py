from World import *
import matplotlib.pyplot as plt

w = World()
food_location=np.array([[10, 10], [11, 11]])
w.set_state('f', x=10, y=20)

state = w.get_state_matrix()

for i in range(w.x_length):
    for j in range(w.y_length):
        if state[j, i] != '0':
            plt.plot(i, j, 'r.')
        else:
            plt.plot(i, j, 'b.')
plt.show()
