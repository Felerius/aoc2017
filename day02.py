def parse_table(in_file):
    return [[int(c) for c in r.split()] for r in in_file]


def all_pairs(row):
    for i, a in enumerate(row):
        for b in row[i + 1:]:
            yield a, b


def calc_row_checksum(row):
    """Largest value minus smallest value in the row.

    >>> calc_row_checksum([5, 1, 9, 5])
    8
    >>> calc_row_checksum([7, 5, 3])
    4
    >>> calc_row_checksum([2, 4, 6, 8])
    6
    """
    return max(row) - min(row)


def calc_table_checksum(table):
    """Sum of row checksums.

    >>> calc_table_checksum([[5, 1, 9, 5], [7, 5, 3], [2, 4, 6, 8]])
    18
    """
    return sum(calc_row_checksum(row) for row in table)


def calc_advanced_row_checksum(row):
    """Find numbers a, b where b divides a evenly and return a / b.

    >>> calc_advanced_row_checksum([5, 9, 2, 8])
    4
    >>> calc_advanced_row_checksum([9, 4, 7, 3])
    3
    >>> calc_advanced_row_checksum([3, 8, 6, 5])
    2
    """
    for a, b in all_pairs(row):
        x, y = max(a, b), min(a, b)
        if x % y == 0:
            return x // y


def calc_advanced_table_checksum(table):
    """Sum of the advanced checksums for each row.

    >>> calc_advanced_table_checksum([[5, 9, 2, 8], [9, 4, 7, 3], [3, 8, 6, 5]])
    9
    """
    return sum(calc_advanced_row_checksum(row) for row in table)


if __name__ == '__main__':
    with open('day02.in') as f:
        print(calc_table_checksum(parse_table(f)))
    with open('day02x.in') as f:
        print(calc_advanced_table_checksum(parse_table(f)))
