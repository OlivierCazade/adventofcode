def get_wires_from_file(inputFile):
    with open(inputFile) as fp:
        for line in fp:
            yield(line)


def get_direction_from_wire(wire):
    for direction in wire.split(","):
        yield(direction)


def next_coordinates(x, y, direction):
    if direction[0] == "R":
        return((x + int(direction[1:]), y))
    if direction[0] == "L":
        return((x - int(direction[1:]), y))
    if direction[0] == "U":
        return((x, y + int(direction[1:])))
    if direction[0] == "D":
        return((x, y - int(direction[1:])))


def get_segments_from_wire(wire):
    x = 0
    y = 0

    for direction in get_direction_from_wire(wire):
        next_x, next_y = next_coordinates(x, y, direction)
        yield(((x, y), (next_x, next_y)))
        x = next_x
        y = next_y


def get_intersection(wire1, wire2):
    wire2_length = 0
    for segment in wire2:
        p1, p2 = segment
        x1, y1 = p1
        x2, y2 = p2
        wire1_length = 0
        seg_length = 0
        for A, B in wire1:
            xA, yA = A
            xB, yB = B
            wire1_length += seg_length
            seg_length = abs(xA - xB) + abs(yA - yB)
            if xA == xB:
                if x1 == x2:
                    continue
                if xA > x1 and xA > x2:
                    continue
                if xA < x1 and xA < x2:
                    continue
                if y1 > yA and y1 > yB:
                    continue
                if y1 < yA and y1 < yB:
                    continue
                yield(wire1_length + abs(yA - y1) + wire2_length + abs(x1 - xA))
            else:
                if y1 == y2:
                    continue
                if yA > y1 and yA > y2:
                    continue
                if yA < y1 and yA < y2:
                    continue
                if x1 > xA and x1 > xB:
                    continue
                if x1 < xA and x1 < xB:
                    continue
            yield(wire1_length + abs(xA - x1) + wire2_length + abs(y1 - yA))
        wire2_length += abs(x1 - x2) + abs(y1 - y2)


def get_solution(inputFile):
    wires = get_wires_from_file(inputFile)
    wire1 = list(get_segments_from_wire(next(wires)))
    tmp_res = get_intersection(wire1, get_segments_from_wire(next(wires)))
    return(min(tmp_res))


if __name__ == '__main__':
    print(get_solution("./input.txt"))
