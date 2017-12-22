import collections
import re

VECTOR_REGEX = re.compile(r'[a-z]=<(-?\d+),(-?\d+),(-?\d+)>')
ITERATIONS = 1000


def parse_particle(line):
    return [[int(s) for s in VECTOR_REGEX.match(v).groups()] for v in
            line.split(', ')]


def particle_staying_closest(particles):
    """Find the particle staying closest to (0, 0, 0).

    >>> particle_staying_closest([
    ...   ((3, 0, 0), (2, 0, 0), (-1, 0, 0)),
    ...   ((4, 0, 0), (0, 0, 0), (-2, 0, 0))])
    0
    """

    def absolute_acceleration_sum(args):
        return sum(abs(i) for i in args[1][2])

    return min(enumerate(particles), key=absolute_acceleration_sum)[0]


def simulate_tick(particles):
    position_counts = collections.defaultdict(int)
    moved_particles = []
    for pos, vel, acc in particles:
        vel = tuple(i + j for i, j in zip(vel, acc))
        pos = tuple(i + j for i, j in zip(pos, vel))
        moved_particles.append((pos, vel, acc))
        position_counts[pos] += 1
    return ((pos, vel, acc) for pos, vel, acc in moved_particles if
            position_counts[pos] == 1)


def count_non_colliding(particles):
    for _ in range(ITERATIONS):
        particles = simulate_tick(particles)
    return len(list(particles))


def main():
    with open('day20.in') as f:
        particles = [parse_particle(l) for l in f]
    print(particle_staying_closest(particles))
    print(count_non_colliding(particles))


if __name__ == '__main__':
    main()
