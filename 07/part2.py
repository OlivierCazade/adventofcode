import asyncio
import itertools


def gen_value_from_file(inputFile):
    with open(inputFile) as fp:
        for line in fp:
            for value in line.split(","):
                if value != "\n":
                    yield(int(value))


async def operation_add(prog, position, data_in, data_out):
    a = get_instruction(prog, position, 3, 0)
    b = get_instruction(prog, position, 3, 1)
    prog[prog[position + 3]] = a + b
    return(4)


async def operation_mul(prog, position, data_in, data_out):
    a = get_instruction(prog, position, 3, 0)
    b = get_instruction(prog, position, 3, 1)
    prog[prog[position + 3]] = a * b
    return(4)


async def operation_input(prog, position, data_in, data_out):
    tmp = int(await data_in.get())
    prog[prog[position + 1]] = tmp
    return(2)


async def operation_output(prog, position, data_in, data_out):
    a = get_instruction(prog, position, 1, 0)
    await data_out.put(a)
    return(2)


async def operation_jump_if_true(prog, position, data_in, data_out):
    a = get_instruction(prog, position, 2, 0)
    b = get_instruction(prog, position, 2, 1)
    if a != 0:
        return(b - position)
    else:
        return(3)


async def operation_jump_if_false(prog, position, data_in, data_out):
    a = get_instruction(prog, position, 2, 0)
    b = get_instruction(prog, position, 2, 1)
    if a == 0:
        return(b - position)
    else:
        return(3)


async def operation_less_than(prog, position, data_in, data_out):
    a = get_instruction(prog, position, 3, 0)
    b = get_instruction(prog, position, 3, 1)
    if a < b:
        prog[prog[position + 3]] = 1
    else:
        prog[prog[position + 3]] = 0
    return(4)


async def operation_equals(prog, position, data_in, data_out):
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


async def exec_file(inputFile, input_data, output_data):
    prog = list(gen_value_from_file(inputFile))
    position = 0
    while(prog[position] != 99):
        # print("Calling: {} {} {} {}".format(prog[position], prog[position + 1], prog[position + 2], prog[position + 3]))
        position += await _instructions[prog[position] % 100](prog, position, input_data, output_data)
        await asyncio.sleep(0)
    return(output_data)


async def exec_sequence(inputFile, sequence):
    queues = []
    tasks = []
    for i in range(0, 5):
        queues.append(asyncio.Queue())
        await queues[i].put(sequence[i])
    await queues[0].put(0)
    queues.append(queues[0])
    for i in range(0, 5):
        task = asyncio.create_task(exec_file(inputFile, queues[i], queues[i + 1]))
        tasks.append(task)
    await asyncio.wait(tasks)
    return(await queues[5].get())


async def search_max(inputFile):
    res = 0
    for seq in itertools.permutations([9, 8, 7, 6, 5]):
        tmp = await exec_sequence(inputFile, seq)
        res = max(res, tmp)
    return(res)


async def main():
    print(await search_max("./input.txt"))

if __name__ == '__main__':
    asyncio.run(main())
