def count_jumps(jump_list, jump_adaptor):
    """Count jumps until we land outside the list.

    >>> count_jumps([0, 3, 0, 1, -3], lambda i: i + 1)
    5
    >>> count_jumps([0, 3, 0, 1, -3], lambda i: i - 1 if i > 2 else i + 1)
    10
    """
    i = 0
    jumps = 0
    while 0 <= i < len(jump_list):
        offset = jump_list[i]
        jump_list[i] = jump_adaptor(jump_list[i])
        i += offset
        jumps += 1
    return jumps


if __name__ == '__main__':
    with open('day05.in') as f:
        print(count_jumps([int(l) for l in f], lambda i: i + 1))
    with open('day05x.in') as f:
        print(count_jumps([int(l) for l in f],
                          lambda i: i - 1 if i > 2 else i + 1))
