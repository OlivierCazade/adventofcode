from itertools import groupby


def gen_value_from_file(inputFile):
    with open(inputFile) as fp:
        for line in fp:
            for c in line:
                if c != "\n":
                    yield(c)


def group_by_layer(inputFile):
    tmp = []
    for c in gen_value_from_file(inputFile):
        tmp.append(c)
        if len(tmp) == 150:
            yield(tmp)
            tmp = []


def get_pixel(layers, pos):
    for l in layers:
        if l[pos] != "2":
            return(l[pos])


def get_solution(inputFile):
    layers = list(group_by_layer(inputFile))
    for y in range(0, 6):
        for x in range(0, 25):
            tmp = get_pixel(layers, x + (y * 25))
            if tmp == "0":
                print(" ", end='')
            else:
                print("0", end='')
        print("")


if __name__ == '__main__':
    get_solution("./input.txt")
