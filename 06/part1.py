from functools import lru_cache

def gen_value_from_file(inputFile):
    with open(inputFile) as fp:
        for line in fp:
            value = line[:-1].split(")")
            yield((value[0], value[1]))


def gen_get_number_orgbit(system):
    @lru_cache(maxsize=None)
    def _get_nb_orbit(key):
        if key not in system:
            return(0)
        else:
            return(_get_nb_orbit(system[key]) + 1)
    return(_get_nb_orbit)

def get_solution(inputFile):
    orbit_system = {}
    for A, B in gen_value_from_file(inputFile):
        orbit_system[B] = A
    res = 0
    get_number_orbit = gen_get_number_orgbit(orbit_system)
    for key in orbit_system:
        res += get_number_orbit(key)
    return(res)


if __name__ == '__main__':
    print(get_solution("./input.txt"))
