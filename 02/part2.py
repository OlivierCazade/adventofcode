def gen_value_from_file(inputFile):
    with open(inputFile) as fp:
        for line in fp:
            for value in line.split(","):
                yield(int(value))

def initialisation(prog, noun, verb):
    prog[1] = noun
    prog[2] = verb

def operation_1(prog, position):
    prog[prog[position + 3]] = prog[prog[position + 1]] + prog[prog[position + 2]]

def operation_2(prog, position):
    prog[prog[position + 3]] = prog[prog[position + 1]] * prog[prog[position + 2]]

_instructions = {
        1 : operation_1,
        2 : operation_2
}

def get_output(prog, noun, verb):
    initialisation(prog, noun, verb)
    position = 0
    while(prog[position] != 99):
        _instructions[prog[position]](prog, position)
        position += 4
    return(prog[0])

def get_solution(inputFile):
    prog = list(gen_value_from_file(inputFile))
    for noun in range(0, 100):
        for verb in range(0, 100):
            if get_output(list(prog), noun, verb) == 19690720:
                return((noun * 100) + verb)



if __name__ == '__main__':
    print(get_solution("./input.txt"))
