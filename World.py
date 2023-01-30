import numpy as np


class World:
    def __init__(self, x_length=30, y_length=30, item_list = ['f','a']):
        self.x_length = x_length
        self.y_length = y_length
        self.item_list = item_list
        self.state_matrix = np.full([self.y_length, self.x_length], '0')
        # y represents the vertical and x the horizontal.

    def get_state_matrix(self):
        return self.state_matrix

    def is_occupied(self, x, y):
        if self.state_matrix[y, x] != 0:
            return True
        else:
            return False

    def set_state(self, item_name, x, y):
        self.state_matrix[y, x] = item_name

