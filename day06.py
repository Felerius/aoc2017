import numpy as np


def redistribute(banks, from_index):
    """Redistribute allocations from one bank to all others.

    >>> redistribute([0, 2, 7, 0], 2)
    [2, 4, 1, 2]
    """
    num_banks = len(banks)
    smaller, num_larger = divmod(banks[from_index], num_banks)
    banks[from_index] = 0
    for offset in range(1, num_banks + 1):
        increment = smaller + 1 if offset <= num_larger else smaller
        banks[(from_index + offset) % num_banks] += increment
    return banks


def find_redistribution_cycle(banks):
    """Redistribute elements until a cycle is found.

    >>> find_redistribution_cycle([0, 2, 7, 0])
    (5, 4)
    """
    known_states = {tuple(banks): 0}
    while True:
        banks = redistribute(banks, np.argmax(banks))
        banks_tuple = tuple(banks)
        if banks_tuple in known_states:
            return len(known_states), len(known_states) - known_states[
                banks_tuple]
        known_states[banks_tuple] = len(known_states)


if __name__ == '__main__':
    with open('day06.in') as f:
        print(find_redistribution_cycle(
            np.array([int(s) for s in f.readline().split()])))
