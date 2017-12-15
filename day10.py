import functools

from knothash import calc_knot_hash, CIRCLE_SIZE


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


def main():
    with open('day10.in') as f:
        input_line = f.readline()
    print(calc_simple_hash(input_line))
    print(calc_knot_hash(input_line.strip()).hex())


if __name__ == '__main__':
    main()
