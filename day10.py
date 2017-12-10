import functools
import operator


CIRCLE_SIZE = 256
INPUT_SALT = [17, 31, 73, 47, 23]
ROUNDS = 64
DENSE_GROUP_SIZE = 16


def calc_twists(lengths):
    pos = 0
    for skip_size, length in enumerate(lengths):
        yield pos, length
        pos += length + skip_size
        pos %= CIRCLE_SIZE


def apply_twist_to_pos(pos, start, length):
    """Apply a reversal of the values between start and start + length - 1.

    >>> apply_twist_to_pos(2, 0, 3, 6)
    0
    >>> apply_twist_to_pos(1, 0, 3, 6)
    1
    >>> apply_twist_to_pos(5, 0, 3, 6)
    5
    """
    offset = (pos - start) % CIRCLE_SIZE
    if offset < length:
        return (start + length - 1 - offset) % CIRCLE_SIZE
    return pos


def calc_initial_position(final_pos, twists):
    """Apply twists in reverse.

    >>> calc_initial_position(0, [(0, 3), (3, 4), (3, 1), (1, 5)], 6)
    3
    >>> calc_initial_position(1, [(0, 3), (3, 4), (3, 1), (1, 5)], 6)
    4
    """
    return functools.reduce(
        lambda pos, tup: apply_twist_to_pos(pos, *tup), reversed(twists),
        final_pos)


def calc_simple_hash(input_line):
    twists = list(calc_twists(int(s) for s in input_line.split(',')))
    val1 = calc_initial_position(0, twists)
    val2 = calc_initial_position(1, twists)
    return val1 * val2


def calc_advanced_lengths(input_line):
    input_bytes = input_line.strip().encode('ascii')
    return list(input_bytes) + INPUT_SALT


def apply_twist_to_circle(circle, start, length):
    i1, i2 = start, (start + length - 1) % CIRCLE_SIZE
    for _ in range(length // 2):
        circle[i1], circle[i2] = circle[i2], circle[i1]
        i1 = (i1 + 1) % CIRCLE_SIZE
        i2 = (i2 - 1) % CIRCLE_SIZE


def to_dense(circle):
    for i in range(0, len(circle), DENSE_GROUP_SIZE):
        yield functools.reduce(operator.xor, circle[i:i + DENSE_GROUP_SIZE])


def encode_as_hex(dense_values):
    return bytes(dense_values).hex()


def calc_knot_hash(input_line):
    lengths = calc_advanced_lengths(input_line)
    pos = skip_size = 0
    circle = list(range(CIRCLE_SIZE))
    for _ in range(ROUNDS):
        for length in lengths:
            apply_twist_to_circle(circle, pos, length)
            pos = (pos + length + skip_size) % CIRCLE_SIZE
            skip_size += 1
    return encode_as_hex(to_dense(circle))


def main():
    with open('day10.in') as f:
        input_line = f.readline()
    print(calc_simple_hash(input_line))
    print(calc_knot_hash(input_line))


if __name__ == '__main__':
    main()
