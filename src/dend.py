import math
from fractions import Fraction
from itertools import product

from vector import Vector


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
        return hash(self) == hash(other)

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
            if b.is_leaf():
                return Tridend()
            left = [Tridend.to_vec(bb) for bb in b.children[:-1]]
            right = Tridend.to_vec(b.children[-1])
            return Tridend.vee(*left, right @ other)

        return prec_basis(self)

    def prec_qsh(self, other):
        if self.is_zero() or other.is_zero():
            return Tridend()

        @Tridend.linear_map
        def prec_basis(b):
            if b.is_leaf():
                return Tridend()
            left = [Tridend.to_vec(bb) for bb in b.children[:-1]]
            right = Tridend.to_vec(b.children[-1])
            return Tridend.vee(*left, right * other)

        return prec_basis(self)

    def succ_sh(self, other):
        if self.is_zero() or other.is_zero():
            return Tridend()

        @Tridend.linear_map
        def succ_basis(b):
            if b.is_leaf():
                return Tridend()
            left = Tridend.to_vec(b.children[0])
            right = [Tridend.to_vec(bb) for bb in b.children[1:]]
            return Tridend.vee(left @ self, *right)

        return succ_basis(other)

    def succ_qsh(self, other):
        if self.is_zero() or other.is_zero():
            return Tridend()

        @Tridend.linear_map
        def succ_basis(b):
            if b.is_leaf():
                return Tridend()
            left = Tridend.to_vec(b.children[0])
            right = [Tridend.to_vec(bb) for bb in b.children[1:]]
            return Tridend.vee(left * self, *right)

        return succ_basis(other)

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

    def __mul__(self, other):
        u = Tridend.unit()
        s = self - u
        t = other - u
        result = self + other + self.prec_qsh(t) + s.succ_qsh(other) + self.dot(other)
        return result if not s.is_zero() and not t.is_zero() else result - u

    def __matmul__(self, other):
        u = Tridend.unit()
        s = self - u
        t = other - u
        result = self + other + self.prec_sh(t) + s.succ_sh(other)
        return result if not s.is_zero() and not t.is_zero() else result - u
