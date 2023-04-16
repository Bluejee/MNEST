from pygame.math import Vector2

E = Vector2(1, 0)
W = Vector2(-1, 0)
N = Vector2(0, 1)
S = Vector2(0, -1)
NE = Vector2(1, 1)
NW = Vector2(-1, 1)
SE = Vector2(1, -1)
SW = Vector2(-1, -1)

DIRECTIONS = [E,
              NE,
              N,
              NW,
              W,
              SW,
              S,
              SE]


def front(direction):
    return DIRECTIONS[DIRECTIONS.index(direction)]


def front_left(direction):
    return DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 8]


def front_right(direction):
    return DIRECTIONS[(DIRECTIONS.index(direction) - 1) % 8]


def back(direction):
    return -direction


def back_left(direction):
    return front_right(back(direction))


def back_right(direction):
    return front_left(back(direction))
