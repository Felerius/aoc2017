import itertools


def read_scanners(lines):
    return {int(s1): int(s2) for s1, s2 in (l.split(': ') for l in lines)}


def trip_severity(scanners, delay):
    severity = 0
    caught = False
    for depth, scanner_range in scanners.items():
        if (depth + delay) % (2 * scanner_range - 2) == 0:
            severity += depth * scanner_range
            caught = True
    return severity, caught


def main():
    with open('day13.in') as f:
        scanners = read_scanners(f)
    print(trip_severity(scanners, 0)[0])
    for delay in itertools.count():
        if not trip_severity(scanners, delay)[1]:
            print(delay)
            break


if __name__ == '__main__':
    main()
