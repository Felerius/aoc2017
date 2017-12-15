import string

from knothash import calc_knot_hash


SIZE = 128


def calc_row_hash(input_str, row_num):
    return calc_knot_hash(f'{input_str}-{row_num}')


def count_used_squares(row_hash):
    return sum(bin(b).count('1') for b in row_hash)


def hash_to_matrix_row(row_hash):
    return list(''.join(bin(b)[2:].rjust(8, '0') for b in row_hash))


def flood_fill_region(matrix, x, y, c):
    queue = {(x, y)}
    while queue:
        x, y = queue.pop()
        matrix[y][x] = c
        if x > 0 and matrix[y][x - 1] == '1':
            queue.add((x - 1, y))
        if x + 1 < 128 and matrix[y][x + 1] == '1':
            queue.add((x + 1, y))
        if y > 0 and matrix[y - 1][x] == '1':
            queue.add((x, y - 1))
        if y + 1 < 128 and matrix[y + 1][x] == '1':
            queue.add((x, y + 1))


def find_regions(row_hashes):
    matrix = [hash_to_matrix_row(h) for h in row_hashes]
    count = 0
    for x in range(128):
        for y in range(128):
            if matrix[y][x] == '1':
                flood_fill_region(matrix, x, y, '#')
                count += 1
    return count


def main():
    with open('day14.in') as f:
        input_str = f.readline().rstrip('\n')
    row_hashes = [calc_row_hash(input_str, i) for i in range(SIZE)]
    print(sum(count_used_squares(h) for h in row_hashes))
    print(find_regions(row_hashes))


if __name__ == '__main__':
    main()
