import sys


def gen_value_from_file(inputFile):
    with open(inputFile) as fp:
        for line in fp:
            for value in line.split(","):
                if value != "\n":
                    yield(int(value))


def operation_add(prog, position):
    a = get_instruction(prog, position, 3, 0)
    b = get_instruction(prog, position, 3, 1)
    prog[prog[position + 3]] = a + b
    return(4)


def operation_mul(prog, position):
    a = get_instruction(prog, position, 3, 0)
    b = get_instruction(prog, position, 3, 1)
    prog[prog[position + 3]] = a * b
    return(4)


def operation_input(prog, position):
    tmp = int(sys.stdin.readline())
    prog[prog[position + 1]] = tmp
    return(2)


def operation_output(prog, position):
    a = get_instruction(prog, position, 1, 0)
    print(a)
    return(2)


def operation_jump_if_true(prog, position):
    a = get_instruction(prog, position, 2, 0)
    b = get_instruction(prog, position, 2, 1)
    if a != 0:
        return(b - position)
    else:
        return(3)


def operation_jump_if_false(prog, position):
    a = get_instruction(prog, position, 2, 0)
    b = get_instruction(prog, position, 2, 1)
    if a == 0:
        return(b - position)
    else:
        return(3)


def operation_less_than(prog, position):
    a = get_instruction(prog, position, 3, 0)
    b = get_instruction(prog, position, 3, 1)
    if a < b:
        prog[prog[position + 3]] = 1
    else:
        prog[prog[position + 3]] = 0
    return(4)


def operation_equals(prog, position):
    a = get_instruction(prog, position, 3, 0)
    b = get_instruction(prog, position, 3, 1)
    if a == b:
        prog[prog[position + 3]] = 1
    else:
        prog[prog[position + 3]] = 0
    return(4)


_instructions = {
    1: operation_add,
    2: operation_mul,
    3: operation_input,
    4: operation_output,
    5: operation_jump_if_true,
    6: operation_jump_if_false,
    7: operation_less_than,
    8: operation_equals,
}


def get_instruction(prog, position, nb_instruction, instruction_number):
    opcode = prog[position]
    opcode = str(opcode)
    # we remove the operation code :
    opcode = opcode[:-2]
    opcode = "0" * (nb_instruction - len(opcode)) + opcode
    mode = opcode[-1 - instruction_number]
    if mode == "0":
        return(prog[prog[position + instruction_number + 1]])
    elif mode == "1":
        return(prog[position + instruction_number + 1])


def exec_file(inputFile):
    prog = list(gen_value_from_file(inputFile))
    position = 0
    while(prog[position] != 99):
        # print("Calling: {} {} {} {}".format(prog[position], prog[position + 1], prog[position + 2], prog[position + 3]))
        position += _instructions[prog[position] % 100](prog, position)


if __name__ == '__main__':
    exec_file("./input.txt")
