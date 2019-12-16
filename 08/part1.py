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


def get_solution(inputFile):
    best = None
    for g in group_by_layer(inputFile):
        nb_iter = {key: len(list(group)) for key, group in groupby(sorted(g))}
        if best is None or nb_iter["0"] < best["0"]:
            best = nb_iter
    return(best["1"] * best["2"])


if __name__ == '__main__':
    print(get_solution("./input.txt"))
