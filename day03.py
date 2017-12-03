import itertools
import math


def to_ring(num):
    """Converts from a number on the spiral to its ring.

    >>> to_ring(1)
    0
    >>> to_ring(9)
    1
    >>> to_ring(10)
    2
    """
    return int((math.sqrt(num - 1) + 1) // 2)


def to_pos(num):
    """Converts from a number to its (x, y) position.

    >>> to_pos(1)
    (0, 0)
    >>> to_pos(2)
    (1, 0)
    >>> to_pos(4)
    (0, 1)
    >>> to_pos(20)
    (-2, -1)
    >>> to_pos(25)
    (2, -2)
    """
    ring = to_ring(num)
    ring_size = 2 * ring + 1
    num_on_ring = num - (ring_size - 2) ** 2 - 1

    # Bottom side
    if num_on_ring < ring_size - 1:
        return ring, -ring + 1 + num_on_ring
    num_on_ring -= ring_size - 1

    # Top side
    if num_on_ring < ring_size - 1:
        return ring - 1 - num_on_ring, ring
    num_on_ring -= ring_size - 1

    # Left side
    if num_on_ring < ring_size - 1:
        return -ring, ring - 1 - num_on_ring
    num_on_ring -= ring_size - 1

    return -ring + 1 + num_on_ring, -ring


def carrying_distance(num):
    """Manhattan distance from nums field to (0, 0).

    >>> carrying_distance(1)
    0
    >>> carrying_distance(12)
    3
    >>> carrying_distance(23)
    2
    >>> carrying_distance(1024)
    31
    """
    x, y = to_pos(num)
    return abs(x) + abs(y)


def spiral_positions():
    """Positions of the spiraling elements.

    >>> list(itertools.islice(spiral_positions(), 1))
    [(0, 0)]
    >>> list(itertools.islice(spiral_positions(), 24, 25))
    [(2, -2)]
    """
    x, y = 0, 0
    yield x, y
    for ring_size in itertools.count(start=3, step=2):
        x += 1
        y -= 1
        for i in range(ring_size - 1):
            y += 1
            yield x, y
        for i in range(ring_size - 1):
            x -= 1
            yield x, y
        for i in range(ring_size - 1):
            y -= 1
            yield x, y
        for i in range(ring_size - 1):
            x += 1
            yield x, y


def stress_test_values():
    """Spiraling values calculated by summing all neighbours.

    >>> list(itertools.islice(stress_test_values(), 1))
    [1]
    >>> list(itertools.islice(stress_test_values(), 9))
    [1, 1, 2, 4, 5, 10, 11, 23, 25]
    """
    grid_values = {(0, 0): 1}
    yield 1

    offsets = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
    for x, y in itertools.islice(spiral_positions(), 1, None):
        value = sum(
            grid_values.get((x + delta_x, y + delta_y), 0) for delta_x, delta_y
            in offsets)
        grid_values[(x, y)] = value
        yield value


def find_first_larger_in_stress_test(num):
    return next(itertools.dropwhile(lambda x: x <= num, stress_test_values()))


if __name__ == '__main__':
    with open('day03.in') as f:
        print(carrying_distance(int(f.readline())))
    with open('day03x.in') as f:
        print(find_first_larger_in_stress_test(int(f.readline())))
