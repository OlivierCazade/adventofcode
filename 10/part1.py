from math import atan2
from itertools import groupby


def gen_value_from_file(inputFile):
    with open(inputFile) as fp:
        x = 0
        y = 0
        for line in fp:
            for c in line:
                if c == "#":
                    yield((x,y))
                x += 1
            x = 0
            y += 1


def get_solution(inputFile):
    res = 0
    asteroids = list(gen_value_from_file(inputFile))
    for ast in asteroids:
        a_x, a_y = ast
        tmp = sorted([atan2((x - a_x),(y - a_y)) for x,y in asteroids if x != a_x or y != a_y])
        res = max(res, len(list(groupby(tmp))))
    return(res)

if __name__ == '__main__':
    print(get_solution("./input.txt"))
