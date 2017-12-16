import enum


class DanceMove(enum.Enum):
    SPIN = 1
    EXCHANGE = 2
    PARTNER = 3


def parse_command(s):
    if s[0] == 's':
        return DanceMove.SPIN, int(s[1:])
    elif s[0] == 'x':
        a, b = (int(p) for p in s[1:].split('/'))
        return DanceMove.EXCHANGE, a, b
    return DanceMove.PARTNER, s[1], s[3]


def execute_command(cmd, programs, renames):
    move, *args = cmd
    if move == DanceMove.SPIN:
        programs[:] = programs[-args[0]:] + programs[:-args[0]]
    elif move == DanceMove.EXCHANGE:
        a, b = args
        programs[a], programs[b] = programs[b], programs[a]
    else:
        a, b = args
        renames[a], renames[b] = renames[b], renames[a]


def parse_and_execute(cmd_text, programs):
    """Parse dance moves and execute them.

    >>> parse_and_execute('s1,x3/4,pe/b', 'abcde')
    'baedc'
    """
    cmds = (parse_command(s) for s in cmd_text.split(','))
    renames = {c: c for c in programs}
    programs_list = list(programs)
    for cmd in cmds:
        execute_command(cmd, programs_list, renames)
    reverse_renames = {b: a for a, b in renames.items()}
    return ''.join(reverse_renames[c] for c in programs_list)


def main():
    with open('day16.in') as f:
        cmd_text = f.read()
    after_first = parse_and_execute(cmd_text, 'abcdefghijklmnop')
    print(after_first)
    last = parse_and_execute(cmd_text, after_first)
    cycle_length = 1
    while last != after_first:
        last = parse_and_execute(cmd_text, last)
        cycle_length += 1
    for _ in range(10**9 % cycle_length - 1):
        last = parse_and_execute(cmd_text, last)
    print(last)


if __name__ == '__main__':
    main()
