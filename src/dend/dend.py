import math
from itertools import product

from .vector import Vector


class STree:
    """
    Represents an undecorated Schröder Tree
    """

    def __init__(self):
        """
        Initializes a node in the tree.
        """
        self.children = None

    def insert_left(self, children=None):
        """
        Sets the forest represented by `children` as the left-most children of the root
        If no argument is given then we insert a single leaf
        """
        if self.children is None:
            self.children = [STree()] if children is None else children
        elif children is None:
            self.children = [STree()] + self.children
        else:
            self.children = children + self.children

        return self

    def insert_right(self, children=None):
        """
        Sets the forest represented by `children` as the left-most children of the root
        If no argument is given then we insert a single leaf
        """
        if self.children is None:
            self.children = [STree()] if children is None else children
        elif children is None:
            self.children += [STree()]
        else:
            self.children += children

        return self

    @staticmethod
    def parse(s: str) -> "STree":
        """
        Parses a balanced string of square brackets into a Schröder tree.

        Examples:
            "[]" -> leaf node
            "[[][]]" -> root with two leaf children
            "[[][][]]" -> root with three leaf children
        """

        def parse_rec(s: str, pos: int) -> tuple[STree, int]:
            if pos >= len(s):
                raise ValueError("Unexpected end of string")
            if s[pos] != "[":
                raise ValueError(f"Expected '[' at position {pos}")

            tree = STree()
            pos += 1  # skip '['
            children = []

            while pos < len(s) and s[pos] != "]":
                child, new_pos = parse_rec(s, pos)
                children.append(child)
                pos = new_pos

            if pos >= len(s) or s[pos] != "]":
                raise ValueError("Unmatched '['")

            if children:
                tree.children = children

            return tree, pos + 1

        tree, end = parse_rec(s, 0)
        if end != len(s):
            raise ValueError("Extra characters after valid tree")
        return tree

    def __repr__(self):
        """
        Returns a string representation of the node and its children.
        """
        children = [repr(c) for c in self.children] if self.children is not None else []
        return f"[{''.join(children)}]"

    def __hash__(self):
        """
        Returns a hash of the node.
        """
        return hash(str(self))

    def __eq__(self, other):
        if self.is_leaf() and other.is_leaf():
            return True
        if len(self.children) != len(other.children):
            return False
        return all(
            left == right for (left, right) in zip(self.children, other.children)
        )

    def is_leaf(self):
        return self.children is None


class Tridend(Vector):
    @staticmethod
    def unit():
        return Tridend.to_vec(STree())

    def vee(*trees):
        output = Tridend()
        for tup in product(*[t.items() for t in trees]):
            s = math.prod(t[1] for t in tup)
            b = STree().insert_left([t[0] for t in tup])
            output += Tridend({b: s})

        return output

    def prec_sh(self, other):
        if self.is_zero() or other.is_zero():
            return Tridend()

        @Tridend.linear_map
        def prec_basis(b):
            b1, b2 = b
            if b1.is_leaf():
                return Tridend()
            if b2.is_leaf():
                return self

            left = [Tridend.to_vec(bb) for bb in b1.children[:-1]]
            right = Tridend.to_vec(b1.children[-1])
            other_b = Tridend.to_vec(b2)
            return Tridend.vee(*left, right @ other_b)

        return prec_basis(self.outer(other))

    def prec_qsh(self, other):
        if self.is_zero() or other.is_zero():
            return Tridend()

        @Tridend.linear_map
        def prec_basis(b):
            b1, b2 = b
            if b1.is_leaf():
                return Tridend()
            if b2.is_leaf():
                return self

            left = [Tridend.to_vec(bb) for bb in b1.children[:-1]]
            right = Tridend.to_vec(b1.children[-1])
            other_b = Tridend.to_vec(b2)
            return Tridend.vee(*left, right * other_b)

        return prec_basis(self.outer(other))

    def succ_sh(self, other):
        if self.is_zero() or other.is_zero():
            return Tridend()

        @Tridend.linear_map
        def succ_basis(b):
            b1, b2 = b
            if b1.is_leaf():
                return other
            if b2.is_leaf():
                return Tridend()

            left = Tridend.to_vec(b2.children[0])
            right = [Tridend.to_vec(bb) for bb in b2.children[1:]]
            self_b = Tridend.to_vec(b1)
            return Tridend.vee(left @ self_b, *right)

        return succ_basis(self.outer(other))

    def succ_qsh(self, other):
        if self.is_zero() or other.is_zero():
            return Tridend()

        @Tridend.linear_map
        def succ_basis(b):
            b1, b2 = b
            if b1.is_leaf():
                return other
            if b2.is_leaf():
                return Tridend()

            left = Tridend.to_vec(b2.children[0])
            right = [Tridend.to_vec(bb) for bb in b2.children[1:]]
            self_b = Tridend.to_vec(b1)
            return Tridend.vee(left * self_b, *right)

        return succ_basis(self.outer(other))

    def dot(self, other):
        if (
            self.is_zero()
            or other.is_zero()
            or self == Tridend.unit()
            or other == Tridend.unit()
        ):
            return Tridend()

        @Tridend.linear_map
        def dot_basis(b):
            left = [Tridend.to_vec(bb) for bb in b.children[:-1]]
            mid1 = Tridend.to_vec(b.children[-1])
            result = Tridend()
            for b2, s in other.items():
                mid2 = Tridend.to_vec(b2.children[0])
                mid = mid1 * mid2
                right = [Tridend.to_vec(bb) for bb in b2.children[1:]]
                result += s * Tridend.vee(*left, mid, *right)

            return result

        return dot_basis(self)

    def coprod_sh(self):
        @Tridend.linear_map
        def coprod_basis(b):
            u = Tridend.unit()
            if b.is_leaf():
                return u.outer(u)

            left = Tridend.to_vec(b.children[0])
            mid = [Tridend.to_vec(bb) for bb in b.children[1:-1]]
            right = Tridend.to_vec(b.children[-1])

            delta1 = left.coprod_sh()
            delta2 = right.coprod_sh()

            result = Tridend()

            for (x, y) in product(delta1.items(), delta2.items()):
                b1, k1 = x
                b2, k2 = y
                result += k1 * k2 * (Tridend.to_vec(b1[0]) @ Tridend.to_vec(b2[0])).outer(Tridend.vee(Tridend.to_vec(b1[1]), *mid, Tridend.to_vec(b2[1])))

            return result + self.outer(u)

        return coprod_basis(self)

    def coprod_qsh(self):
        @Tridend.linear_map
        def coprod_basis(b):
            u = Tridend.unit()
            if b.is_leaf():
                return u.outer(u)

            deltas = [Tridend.to_vec(bb).coprod_qsh() for bb in b.children]

            result = Tridend()

            for x in product(*[delta.items() for delta in deltas]):
                k = math.prod(it[1] for it in x)
                result += k * math.prod(Tridend.to_vec(it[0][0]) for it in x).outer(Tridend.vee(*[Tridend.to_vec(it[0][1]) for it in x]))

            return result + self.outer(u)

        return coprod_basis(self)


    def __mul__(self, other):
        return self.prec_qsh(other) + self.succ_qsh(other) + self.dot(other)

    def __matmul__(self, other):
        return self.prec_sh(other) + self.succ_sh(other)
