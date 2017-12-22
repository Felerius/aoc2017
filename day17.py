STEPS = 370


def execute_spinlock(max_num, steps):
    """Execute `max_num` spinlock steps.

    >>> execute_spinlock(9, 3)
    ([0, 9, 5, 7, 2, 4, 3, 8, 6, 1], 1)
    """
    values = [0]
    pos = 0
    for i in range(1, max_num + 1):
        pos = (pos + steps) % len(values) + 1
        values.insert(pos, i)
    return values, pos


def find_value_after_zero(max_num, steps):
    """Find the number standing behind 0 after `max_num` iterations.

    >>> find_value_after_zero(2017, STEPS)
    1157
    """
    pos = 0
    after_zero = 0
    for i in range(1, max_num + 1):
        pos = (pos + steps) % i + 1
        if pos == 1:
            after_zero = i
    return after_zero


def main():
    values, pos = execute_spinlock(2017, STEPS)
    print(values[(pos + 1) % len(values)])
    print(find_value_after_zero(50000000, STEPS))


if __name__ == '__main__':
    main()
