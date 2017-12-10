def remove_cancelled(chars):
    """Remove exclamation marks and the char followed by them.

    >>> ''.join(remove_cancelled('{{<!>},{<!>},{<!>},{<a>}}'))
    '{{<},{<},{<},{<a>}}'
    """
    char_iter = iter(chars)
    while True:
        try:
            c = next(char_iter)
            if c == '!':
                next(char_iter)
            else:
                yield c
        except StopIteration:
            break


def remove_garbage(chars, count_callback):
    """Remove everything between < > pairs.

    >>> ''.join(remove_garbage('{{<},{<},{<},{<a>}}'))
    '{{}}'
    """
    char_iter = iter(chars)
    while True:
        try:
            c = next(char_iter)
            if c == '<':
                count = 0
                while c != '>':
                    count += 1
                    c = next(char_iter)
                count_callback(count - 1)
            else:
                yield c
        except StopIteration:
            break


def calc_score(chars):
    """Sum nesting levels of { } groups.

    >>> calc_score('{}')
    1
    >>> calc_score('{{{}}}')
    6
    >>> calc_score('{{},{}}')
    5
    >>> calc_score('{{{},{},{{}}}}')
    16
    """
    score = 0
    level = 1
    for c in chars:
        if c == '{':
            score += level
            level += 1
        elif c == '}':
            level -= 1
    return score


def main():
    with open('day09.in') as f:
        data = f.readline()
        garbage_count = 0

        def incr_garbage_count(count):
            nonlocal garbage_count
            garbage_count += count

        print(calc_score(
            remove_garbage(remove_cancelled(data), incr_garbage_count)))
        print(garbage_count)


if __name__ == '__main__':
    main()
