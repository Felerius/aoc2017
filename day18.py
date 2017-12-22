import collections
import enum
import string


class Command(enum.Enum):
    SND = enum.auto()
    SET = enum.auto()
    ADD = enum.auto()
    MUL = enum.auto()
    MOD = enum.auto()
    RCV = enum.auto()
    JGZ = enum.auto()

    @property
    def has_dual_args(self):
        return self not in {Command.SND, Command.RCV}

    @classmethod
    def from_name(cls, name):
        return cls[name.upper()]


class ImmediateValue(int):
    def eval(self, _state):
        return self


class RegisterValue(str):
    def eval(self, state):
        return state.registers[self]


class State:
    def __init__(self):
        self.instr_ptr = 0
        self.out_queue = collections.deque()
        self.registers = {c: 0 for c in string.ascii_lowercase}
        self.send_counter = 0

    def send(self, value):
        self.out_queue.append(value)
        self.send_counter += 1


def parse_value(s):
    if s[0].isalpha():
        return RegisterValue(s[0])
    return ImmediateValue(s)


def parse_instruction(line):
    command = Command.from_name(line[:3])
    if command.has_dual_args:
        a, b = (parse_value(s) for s in line[4:].split(' '))
        return command, a, b
    return command, parse_value(line[4:])


def eval_instruction(instruction, state):
    command, *args = instruction
    if command == Command.SND:
        state.send(args[0].eval(state))
    elif command == Command.SET:
        state.registers[args[0]] = args[1].eval(state)
    elif command == Command.ADD:
        state.registers[args[0]] += args[1].eval(state)
    elif command == Command.MUL:
        state.registers[args[0]] *= args[1].eval(state)
    elif command == Command.MOD:
        state.registers[args[0]] %= args[1].eval(state)

    offset = 1
    if command == Command.JGZ and args[0].eval(state) > 0:
        offset = args[1].eval(state)
    state.instr_ptr += offset


def recover_single_value(instructions):
    """Executes a program until a frequency is recovered.

    >>> recover_single_value(
    ...   [parse_instruction(s) for s in ('set a 1', 'add a 2', 'mul a a',
    ...                                   'mod a 5', 'snd a', 'set a 0',
    ...                                   'rcv a', 'jgz a -1', 'set a 1',
    ...                                   'jgz a -2')])
    4
    """
    state = State()
    while 0 <= state.instr_ptr < len(instructions):
        instruction = instructions[state.instr_ptr]
        if instruction[0] == Command.RCV and instruction[1].eval(state):
            return state.out_queue[-1]
        eval_instruction(instruction, state)
    return None


def execute_until_blocked(instructions, state, in_queue):
    while 0 <= state.instr_ptr < len(instructions):
        instruction = instructions[state.instr_ptr]
        if instruction[0] == Command.RCV:
            if in_queue:
                state.registers[instruction[1]] = in_queue.popleft()
                state.instr_ptr += 1
            else:
                return False
        else:
            eval_instruction(instruction, state)
    return True


def execute_dual_programs(instructions):
    """Execute duet programs until termination or deadlock.

    >>> execute_dual_programs(
    ...   [parse_instruction(s) for s in ('snd 1', 'snd 2', 'snd p', 'rcv a',
    ...                                   'rcv b', 'rcv c', 'rcv d')])
    3
    """
    state0, state1 = State(), State()
    state1.registers['p'] = 1

    if execute_until_blocked(instructions, state0, state1.out_queue):
        return state1.send_counter
    if execute_until_blocked(instructions, state1, state0.out_queue):
        return state1.send_counter

    while True:
        if not state1.out_queue:
            return state1.send_counter
        if execute_until_blocked(instructions, state0, state1.out_queue):
            return state1.send_counter

        if not state0.out_queue:
            return state1.send_counter
        if execute_until_blocked(instructions, state1, state0.out_queue):
            return state1.send_counter


def main():
    with open('day18.in') as f:
        instructions = [parse_instruction(line) for line in f]
    print(recover_single_value(instructions))
    print(execute_dual_programs(instructions))


if __name__ == '__main__':
    main()
