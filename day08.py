from collections import defaultdict
import operator
import re

OPERATORS = {
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
}

INSTRUCTION_REGEX = re.compile(
    r'(\w+) (inc|dec) (-?\d+) if (\w+) (<=?|>=?|==|!=) (-?\d+)')


def execute_instruction(line, variables):
    m = INSTRUCTION_REGEX.match(line)
    change_var, change_op, change_val, test_var, test_op, test_val = m.groups()
    change_val, test_val = int(change_val), int(test_val)
    if OPERATORS[test_op](variables[test_var], test_val):
        if change_op == 'inc':
            variables[change_var] += change_val
        else:
            variables[change_var] -= change_val
    return variables[change_var]


def main():
    max_during_execution = 0
    variables = defaultdict(int)
    with open('day08.in') as f:
        for line in f:
            changed_val = execute_instruction(line, variables)
            max_during_execution = max(max_during_execution, changed_val)
    print(max(variables.values()), max_during_execution)


if __name__ == '__main__':
    main()
