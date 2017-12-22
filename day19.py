import enum


EXAMPLE_DIAGRAM = [
    '     |          ',
    '     |  +--+    ',
    '     A  |  C    ',
    ' F---|----E|--+ ',
    '     |  |  |  D ',
    '     +B-+  +--+ ',
]


class Direction(enum.Enum):
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3

    def step(self):
        if self == Direction.LEFT:
            return -1, 0
        if self == Direction.RIGHT:
            return 1, 0
        if self == Direction.UP:
            return 0, -1
        return 0, 1

    def turns(self):
        if self in {Direction.LEFT, Direction.RIGHT}:
            return Direction.UP, Direction.DOWN
        return Direction.LEFT, Direction.RIGHT


def valid_next_pos(matrix, x, y):
    outside_rect = x < 0 or x >= len(matrix[0]) or y < 0 or y >= len(matrix)
    return not outside_rect and matrix[y][x] != ' '


def follow_line(matrix):
    """Follow a path through the matrix and collect letters.

    >>> follow_line(EXAMPLE_DIAGRAM)
    ('ABCDEF', 38)
    """
    x = matrix[0].find('|')
    y = 0
    chars = []
    direction = Direction.DOWN
    steps = 0
    while True:
        steps += 1
        xd, yd = direction.step()
        if not valid_next_pos(matrix, x + xd, y + yd):
            valid = False
            for turn_dir in direction.turns():
                xd, yd = turn_dir.step()
                if valid_next_pos(matrix, x + xd, y + yd):
                    direction = turn_dir
                    valid = True
                    break
            if not valid:
                break
        x += xd
        y += yd
        if matrix[y][x] not in {'|', '-', '+'}:
            chars.append(matrix[y][x])
    return ''.join(chars), steps


def main():
    with open('day19.in') as f:
        matrix = [line.rstrip('\n') for line in f]
    letters, steps = follow_line(matrix)
    print(letters)
    print(steps)


if __name__ == '__main__':
    main()
