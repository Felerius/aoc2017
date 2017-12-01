import sys


def circular_tuples(iterable):
    it = iter(iterable)
    first = previous = next(it)
    for i in it:
        yield previous, i
        previous = i
    yield previous, first


def halfway_around_tuples(l):
    middle = len(l) // 2
    return zip(l[:middle], l[middle:])


def solve_captcha(captcha):
    """Sum digits were the next digit has the same value.

    >>> solve_captcha('1122')
    3
    >>> solve_captcha('1111')
    4
    >>> solve_captcha('1234')
    0
    >>> solve_captcha('91212129')
    9
    """
    return sum(int(a) for a, b in circular_tuples(captcha) if a == b)


def solve_advanced_captcha(captcha):
    """Sum digits where the digit halfway around the list matches.

    >>> solve_advanced_captcha('1212')
    6
    >>> solve_advanced_captcha('1221')
    0
    >>> solve_advanced_captcha('123425')
    4
    >>> solve_advanced_captcha('123123')
    12
    >>> solve_advanced_captcha('12131415')
    4
    """
    return sum(
        int(a) + int(b) for a, b in halfway_around_tuples(captcha) if a == b)


if __name__ == '__main__':
    with open('day01.in') as f:
        print(solve_captcha(f.readline()))
    with open('day01x.in') as f:
        print(solve_advanced_captcha(f.readline()))
