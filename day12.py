import re


LINE_REGEX = re.compile(r'(\d+) <-> (\d+)((, \d+)*)')


def parse_tree(lines):
    tree = {}
    for line in lines:
        match = LINE_REGEX.match(line)
        node = int(match[1])
        tree[node] = [int(match[2])]
        if match[3]:
            for s in match[3][2:].split(', '):
                tree[node].append(int(s))
    return tree


def depth_first_search(tree, node, visited=None):
    if visited is None:
        visited = {node}
    else:
        visited.add(node)
    for neighbour in tree[node]:
        if neighbour not in visited:
            depth_first_search(tree, neighbour, visited)
    return visited


def main():
    with open('day12.in') as f:
        tree = parse_tree(f)
    visited = depth_first_search(tree, 0)
    print(len(visited))
    num_groups = 1
    for i in range(1, len(tree)):
        if i not in visited:
            visited = depth_first_search(tree, i, visited)
            num_groups += 1
    print(num_groups)


if __name__ == '__main__':
    main()
