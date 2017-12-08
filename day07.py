import re


class Node:
    _PARSE_REGEX = re.compile('(\w+) \((\d+)\)(?: -> )?(.*)')

    def __init__(self, children, weight):
        self.children = children
        self.parent = None
        self.weight = weight
        self.weight_sum = None

    def calc_weight_sum(self):
        for child in self.children:
            child.calc_weight_sum()
        self.weight_sum = self.weight + sum(c.weight_sum for c in self.children)

    def balance(self, imbalance):
        """Search place to balance an imbalance.

        Because only one node has to be modified to correct the imbalance, we
        simply follow the nodes with an outlier weight until we find a balanced
        node. We then adjust the weight for this node.

        The task guarantees that there will always be an unambiguous path to
        the node to balance, e.g. there will be no nodes with only two children.
        """
        common, outlier = find_outlier(self.children, lambda n: n.weight_sum)
        if outlier is None:
            return self.weight + imbalance
        assert common.weight_sum - outlier.weight_sum == imbalance
        return outlier.balance(imbalance)

    @classmethod
    def parse(cls, line):
        match = cls._PARSE_REGEX.match(line)
        name = match[1]
        weight = int(match[2])
        children_str = match[3]
        children = []
        if children_str:
            children = [s.strip() for s in children_str.split(', ')]
        return name, Node(children, weight)


def find_outlier(iterable, key):
    """Find the one element with a different key value.

    Returns an element with the common key and the outlier. The outlier can be
    `None` if all elements have the same key.
    """
    iterator = iter(iterable)
    a = next(iterator)
    b = next(iterator)
    if key(a) == key(b):
        for c in iterator:
            if key(c) != key(a):
                return a, c
        return a, None
    else:
        c = next(iterator)
        if key(a) == key(c):
            return a, b
        elif key(b) == key(c):
            return b, a
        else:
            raise Exception('More than 2 distinct values')


def parse_tree(lines):
    nodes = dict(Node.parse(l) for l in lines)
    for node in nodes.values():
        node.children = [nodes[name] for name in node.children]
        for child_node in node.children:
            child_node.parent = node
    return nodes


def find_root_node(nodes):
    return next(
        (name, node) for name, node in nodes.items() if node.parent is None)


def balance_nodes(root):
    root.calc_weight_sum()
    common, outlier = find_outlier(root.children, lambda n: n.weight_sum)
    return outlier.balance(common.weight_sum - outlier.weight_sum)


def main(in_file):
    nodes = parse_tree(in_file)
    root_name, root_node = find_root_node(nodes)
    print(root_name)
    print(balance_nodes(root_node))


if __name__ == '__main__':
    with open('day07.in') as f:
        main(f)
