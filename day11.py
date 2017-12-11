import functools

DIRECTIONS = {
    'nw': (-1, 0),
    'n': (0, -1),
    'ne': (1, -1),
    'se': (1, 0),
    's': (0, 1),
    'sw': (-1, 1),
}


def distance_to_origin(pos):
    q, r = pos
    return max(abs(q), abs(r), abs(-q - r))


def axial_add(pos1, pos2):
    q1, r1 = pos1
    q2, r2 = pos2
    return q1 + q2, r1 + r2


def reduction_step(state, step):
    current, max_distance = state
    current = axial_add(current, DIRECTIONS[step])
    return current, max(max_distance, current, key=distance_to_origin)


def main():
    with open('day11.in') as f:
        steps = f.readline().split(',')
    end_pos, max_dist_pos = functools.reduce(reduction_step, steps,
                                             ((0, 0), (0, 0)))
    print(distance_to_origin(end_pos))
    print(distance_to_origin(max_dist_pos))


if __name__ == '__main__':
    main()
