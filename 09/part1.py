import asyncio
import itertools


class Prog:
    def __init__(self, mem, data_in, data_out):
        self.mem = mem
        self.data_in = data_in
        self.data_out = data_out
        self.position = 0
        self.relative_base = 0


def gen_value_from_file(inputFile):
    with open(inputFile) as fp:
        for line in fp:
            for value in line.split(","):
                if value != "\n":
                    yield(int(value))
    for i in range(0, 10000):
        yield(0)


async def operation_add(prog):
    a = get_instruction(prog, 3, 0)
    b = get_instruction(prog, 3, 1)
    set_instruction_value(prog, 3, 2, a + b)
    prog.position += 4


async def operation_mul(prog):
    a = get_instruction(prog, 3, 0)
    b = get_instruction(prog, 3, 1)
    set_instruction_value(prog, 3, 2, a * b)
    prog.position += 4


async def operation_input(prog):
    tmp = int(await prog.data_in.get())
    set_instruction_value(prog, 1, 0, tmp)
    prog.position += 2


async def operation_output(prog):
    a = get_instruction(prog, 1, 0)
    await prog.data_out.put(a)
    prog.position += 2


async def operation_jump_if_true(prog):
    a = get_instruction(prog, 2, 0)
    b = get_instruction(prog, 2, 1)
    if a != 0:
        prog.position = b
    else:
        prog.position += 3


async def operation_jump_if_false(prog):
    a = get_instruction(prog, 2, 0)
    b = get_instruction(prog, 2, 1)
    if a == 0:
        prog.position = b
    else:
        prog.position += 3


async def operation_less_than(prog):
    a = get_instruction(prog, 3, 0)
    b = get_instruction(prog, 3, 1)
    if a < b:
        set_instruction_value(prog, 3, 2, 1)
    else:
        set_instruction_value(prog, 3, 2, 0)
    prog.position += 4


async def operation_equals(prog):
    a = get_instruction(prog, 3, 0)
    b = get_instruction(prog, 3, 1)
    if a == b:
        set_instruction_value(prog, 3, 2, 1)
    else:
        set_instruction_value(prog, 3, 2, 0)
    prog.position += 4


async def operation_set_relative_base(prog):
    a = get_instruction(prog, 1, 0)
    prog.relative_base += a
    prog.position += 2


_instructions = {
    1: operation_add,
    2: operation_mul,
    3: operation_input,
    4: operation_output,
    5: operation_jump_if_true,
    6: operation_jump_if_false,
    7: operation_less_than,
    8: operation_equals,
    9: operation_set_relative_base,
}


def get_instruction(prog, nb_instruction, instruction_number):
    opcode = prog.mem[prog.position]
    opcode = str(opcode)
    # we remove the operation code :
    opcode = opcode[:-2]
    opcode = "0" * (nb_instruction - len(opcode)) + opcode
    mode = opcode[-1 - instruction_number]
    if mode == "0":
        return(prog.mem[prog.mem[prog.position + instruction_number + 1]])
    elif mode == "1":
        return(prog.mem[prog.position + instruction_number + 1])
    elif mode == "2":
        tmp_pos = prog.relative_base + prog.mem[prog.position + instruction_number + 1]
        return(prog.mem[tmp_pos])


def set_instruction_value(prog, nb_instruction, instruction_number, value):
    opcode = prog.mem[prog.position]
    opcode = str(opcode)
    # we remove the operation code :
    opcode = opcode[:-2]
    opcode = "0" * (nb_instruction - len(opcode)) + opcode
    mode = opcode[-1 - instruction_number]
    if mode == "0":
        prog.mem[prog.mem[prog.position + instruction_number + 1]] = value
    elif mode == "1":
        print("Error !")
    elif mode == "2":
        tmp_pos = prog.relative_base + prog.mem[prog.position + instruction_number + 1]
        prog.mem[tmp_pos] = value


async def exec_file(inputFile, input_data, output_data):
    prog = Prog(list(gen_value_from_file(inputFile)), input_data, output_data)
    while(prog.mem[prog.position] != 99):
        # print("Position : {} Calling: {} {} {} {}".format(prog.position,
        #                                                   prog.mem[prog.position],
        #                                                   prog.mem[prog.position + 1],
        #                                                   prog.mem[prog.position + 2],
        #                                                   prog.mem[prog.position + 3]))
        await _instructions[prog.mem[prog.position] % 100](prog)
        await asyncio.sleep(0)
    return(output_data)


async def print_queue(q):
    try:
        while True:
            tmp = q.get_nowait()
            print(tmp)
    except asyncio.QueueEmpty:
        pass


async def exec_prog(inputFile):
    queues = []
    tasks = []
    for i in range(0, 2):
        queues.append(asyncio.Queue())
    await queues[0].put(1)
    queues.append(queues[0])
    task = asyncio.create_task(exec_file(inputFile, queues[0], queues[1]))
    tasks.append(task)
    await asyncio.wait(tasks)
    await print_queue(queues[1])
    return


async def main():
    await exec_prog("./input.txt")

if __name__ == '__main__':
    asyncio.run(main())
