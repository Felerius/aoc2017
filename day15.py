import itertools


UPPER_BOUND = 2147483647
FACTOR_A = 16807
FACTOR_B = 48271


def generator(seed, factor):
    val = seed
    while True:
        val = val * factor % UPPER_BOUND
        yield val


def compare_pair(val1, val2):
    return val1 & 0xFFFF == val2 & 0xFFFF


def calc_unfiltered_count(seed_a, seed_b):
    pairs = zip(generator(seed_a, FACTOR_A), generator(seed_b, FACTOR_B))
    first_40m = itertools.islice(pairs, 40000000)
    return sum(1 for a, b in first_40m if compare_pair(a, b))


def calc_filtered_count(seed_a, seed_b):
    generator_a = (v for v in generator(seed_a, FACTOR_A) if v % 4 == 0)
    generator_b = (v for v in generator(seed_b, FACTOR_B) if v % 8 == 0)
    first_pairs = itertools.islice(zip(generator_a, generator_b), 5000000)
    return sum(1 for a, b in first_pairs if compare_pair(a, b))


def main():
    with open('day15.in') as f:
        seed_a = int(f.readline())
        seed_b = int(f.readline())
    print(calc_unfiltered_count(seed_a, seed_b))
    print(calc_filtered_count(seed_a, seed_b))


if __name__ == '__main__':
    main()
