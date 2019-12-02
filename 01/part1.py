from math import floor

def gen_value_from_file(inputFile):
    with open(inputFile) as fp:
        for line in fp:
            yield(line)


def get_fuel_required(mass):
    return(floor(int(mass) / 3) - 2)

def get_solution(inputFile):
    return(sum((get_fuel_required(x) for x in gen_value_from_file(inputFile))))

if __name__ == '__main__':
    print(get_solution("./input.txt"))
