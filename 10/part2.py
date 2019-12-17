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


def get_station(asteroids):
    res = 0
    ast_res = None
    for ast in asteroids:
        a_x, a_y = ast
        tmp = sorted([atan2((x - a_x),(y - a_y)) for x,y in asteroids if x != a_x or y != a_y])
        tmp_res = len(list(groupby(tmp)))
        if res < tmp_res:
            res = tmp_res
            ast_res = ast
    return(ast_res)


def manhattan_dist(a):
    x,y = a
    return(abs(x) + abs(y))


def get_destroyed(inputFile):
    asteroids = list(gen_value_from_file(inputFile))
    station = get_station(asteroids)
    st_x, st_y = station

    ast_angle = {}
    for x,y in asteroids:
        if x == st_x and y == st_y:
            continue
        angle = atan2((st_x - x),(st_y - y))
        ast_angle.setdefault(angle, []).append((st_x - x,st_y - y))
    for ang in ast_angle:
        ast_angle[ang].sort(key=manhattan_dist)
    angles = sorted(list(filter(lambda x: x >= 0, ast_angle.keys()))) + sorted(list(filter(lambda x: x < 0, ast_angle.keys())))

    #Hack to get the right order, not really proud of that one
    angles = [angles[0]] + angles[1:][::-1]
    while True:
        for ang in angles:
            if len(ast_angle[ang]) > 0:
                x,y = ast_angle[ang].pop(0)
                yield((st_x - x, st_y - y))


def get_solution(inputFile):
    res = 0
    for x,y in get_destroyed(inputFile):
        res += 1
        if res == 200:
            return((x,y))

if __name__ == '__main__':
    print(get_solution("./input.txt"))
