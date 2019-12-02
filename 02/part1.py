def gen_value_from_file(inputFile):
    with open(inputFile) as fp:
        for line in fp:
            for value in line.split(","):
                yield(int(value))

def initialisation(prog):
    prog[1] = 12
    prog[2] = 2

def operation_1(prog, position):
    prog[prog[position + 3]] = prog[prog[position + 1]] + prog[prog[position + 2]]

def operation_2(prog, position):
    prog[prog[position + 3]] = prog[prog[position + 1]] * prog[prog[position + 2]]

def get_solution(inputFile):
    prog = list(gen_value_from_file(inputFile))
    initialisation(prog)
    position = 0
    instructions = {
        1 : operation_1,
        2 : operation_2
    }
    while(prog[position] != 99):
        instructions[prog[position]](prog, position)
        position += 4

    return(prog[0])


if __name__ == '__main__':
    print(get_solution("./input.txt"))
