class BVS():
    def __init__(self, v=None, r=None, l=None, p=None):
        self.v = v
        self.r = r
        self.l = l
        self.p = p

    def __str__(self, level=0):
        sep = '\t'
        if self.is_leaf():
            return sep*level + "|\n"
        s = self.r.__str__(level=level+1)
        s += sep*level + str(self.v) + "\n"
        s += self.l.__str__(level=level+1)
        return s

    def is_leaf(self):
        return self.v is None

    @classmethod
    def from_string(cls, s):
        s = s.replace('(', ' ( ')
        s = s.replace(')', ' ) ')
        s = ' '.join(s.split())
        if len(s.split()) > 1:
            i, s = s.strip().split(' ', 1)
        else:
            i, s = s, ""
        stack = [cls(v=int(i), l=cls(), r=cls())]
        while s != "":
            s = s.strip()
            if s[0] == '(':
                s = s[1:].strip()
                i, s = s.split(' ', 1)
                node = cls(v=int(i), l=cls(), r=cls(), p=stack[-1])
                node.l.p, node.r.p = node, node
                stack[-1].l = node
                stack.append(node)
            elif s[0] == ')':
                s = s[1:].strip()
                stack.pop()
            else:
                stack.pop()
                i, s = s.split(' ', 1)
                node = cls(v=int(i), l=cls(), r=cls(), p=stack[-1])
                node.l.p, node.r.p = node, node
                stack[-1].r = node
                stack.append(node)
        return stack[0]


def find(tree, key):
    while tree.v != key and tree.v is not None:
        if key < tree.v:
            tree = tree.l
        else:
            tree = tree.r
    return tree


def member(tree, key):
    node = find(tree, key)
    if node.is_leaf():
        return False
    else:
        return True


def insert(tree, key):
    node = find(tree, key)
    if node.is_leaf():
        node.v = key
        node.l, node.r = BVS(p=node), BVS(p=node)


def min_node(tree):
    while not tree.l.is_leaf():
        tree = tree.l
    return tree


def max_node(tree):
    while not tree.r.is_leaf():
        tree = tree.r
    return tree


def delete(tree, key):
    n = find(tree, key)
    if not n.is_leaf():
        if n.r.is_leaf() or n.l.is_leaf():
            repl_node = n.l if n.r.is_leaf() else n.r
            repl_node.p = n.p
            if not n.p:
                n.v, n.l, n.r = repl_node.v, repl_node.l, repl_node.r
            elif n is n.p.l:
                n.p.l = repl_node
            else:
                n.p.r = repl_node
        else:
            prev_max = n.l
            while not prev_max.r.is_leaf():
                prev_max = prev_max.r
            n.v, prev_max.l.p = prev_max.v, prev_max.p
            if prev_max is prev_max.p.r:
                prev_max.p.r = prev_max.l
            else:
                prev_max.p.l = prev_max.l


def delete2(tree, key):
    node = find(tree, key)
    if not node.is_leaf():
        if not node.l.is_leaf():
            if not node.l.r.is_leaf():
                prev_node = max_node(node.l)
                prev_node.p.r = prev_node.l
            else:
                prev_node = node.l
                prev_node.p.l = prev_node.l
            node.v = prev_node.v
            prev_node.l.p = prev_node.p
        elif not node.r.is_leaf():
            if not node.r.l.is_leaf():
                foll_node = min_node(node.r)
                foll_node.p.l = foll_node.r
            else:
                foll_node = node.r
                foll_node.p.r = foll_node.r
            node.v = foll_node.v
            foll_node.r.p = foll_node.p
        else:
            node.l.p = node.p
            if node is node.p.l:
                node.p.l = node.l
            else:
                node.p.r = node.l


t = BVS.from_string('5')
assert t.__str__() == "\t|\n5\n\t|\n"

t = BVS.from_string('5(3 7)')
assert member(t, 5) is True
assert member(t, 3) is True
assert member(t, 7) is True
assert member(t, 6) is False

if __name__ == "__main__":
    insert(t, 2)
    insert(t, 4)
    insert(t, 6)
    insert(t, 8)
    insert(t, 9)
    insert(t, 10)
    insert(t, 11)
    print t
    delete(t, 5)
    print t
    delete(t, 11)
    print t
    delete(t, 8)
    delete(t, 3)
    print t
    delete(t, 4)
    print t
    delete(t, 2)
    print t
    insert(t, 8)
    print t
