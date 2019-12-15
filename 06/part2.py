from functools import lru_cache

def gen_value_from_file(inputFile):
    with open(inputFile) as fp:
        for line in fp:
            value = line[:-1].split(")")
            yield((value[0], value[1]))


def get_path(system, path={}, n=None):
    if n is None:
        n = system["YOU"]
        path = {n : 0}
    if n in system and system[n] not in path:
        path[system[n]] = path[n] + 1
        get_path(system, path, system[n])
    for p in filter( lambda x: system[x] == n, system):
        if p not in path:
            path[p] = path[n] + 1
            get_path(system, path, p)
    return(path)

def get_solution(inputFile):
    orbit_system = {}
    for A, B in gen_value_from_file(inputFile):
        orbit_system[B] = A
    path = get_path(orbit_system)
    return(path[orbit_system["SAN"]])


if __name__ == '__main__':
    print(get_solution("./input.txt"))
