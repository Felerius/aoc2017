import functools
import operator


INPUT_SALT = [17, 31, 73, 47, 23]
CIRCLE_SIZE = 256
ROUNDS = 64
DENSE_GROUP_SIZE = 16


def _apply_twist_to_circle(circle, start, length):
    i1, i2 = start, (start + length - 1) % CIRCLE_SIZE
    for _ in range(length // 2):
        circle[i1], circle[i2] = circle[i2], circle[i1]
        i1 = (i1 + 1) % CIRCLE_SIZE
        i2 = (i2 - 1) % CIRCLE_SIZE


def _to_dense(circle):
    for i in range(0, len(circle), DENSE_GROUP_SIZE):
        yield functools.reduce(operator.xor, circle[i:i + DENSE_GROUP_SIZE])


def calc_knot_hash(input_str):
    lengths = list(input_str.encode('ascii')) + INPUT_SALT
    pos = skip_size = 0
    circle = list(range(CIRCLE_SIZE))
    for _ in range(ROUNDS):
        for length in lengths:
            _apply_twist_to_circle(circle, pos, length)
            pos = (pos + length + skip_size) % CIRCLE_SIZE
            skip_size += 1
    return bytes(_to_dense(circle))
