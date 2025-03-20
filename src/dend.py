from fractions import Fraction
from itertools import product

from vector import Vector


class PBT:
    """
    Represents a Planar Binary Tree (PBT).
    A planar binary tree is a rooted binary tree with a specific planar embedding.
    """

    def __init__(self, value=None):
        """
        Initializes a node in the planar binary tree.
        :param value: The value of the node (default is None).
        """
        self.value = value
        self.left = None  # Left child
        self.right = None  # Right child

    def insert_left(self, value=None):
        """
        Inserts a new node as the left child.
        :param value: The value of the new left child.
        """
        if self.left is None:
            self.left = PBT(value)
        else:
            new_node = PBT(value)
            new_node.left = self.left
            self.left = new_node

        return self

    def insert_right(self, value=None):
        """
        Inserts a new node as the right child.
        :param value: The value of the new right child.
        """
        if self.right is None:
            self.right = PBT(value)
        else:
            new_node = PBT(value)
            new_node.right = self.right
            self.right = new_node

        return self

    @classmethod
    def from_string(cls, s):
        """
        Parses a PBT from a string of balanced square brackets.
        For example, "[10[5][3]]" creates a node with value 10,
        left child 5, and right child 3.
        :param s: The string representation of the PBT.
        :return: A PBT object.
        """
        if not s or s == "[]":
            return PBT()

        # Extract the value (before any brackets)
        value = ""
        i = 1
        while i < len(s) and s[i] not in "[]":
            value += s[i]
            i += 1

        # Create root node
        node = PBT(int(value) if value.strip() else None)

        # If we have children to process
        if i < len(s) and s[i] == "[":
            # Find matched brackets for left child
            balance = 1
            j = i + 1
            while j < len(s) and balance > 0:
                if s[j] == "[":
                    balance += 1
                elif s[j] == "]":
                    balance -= 1
                j += 1

            # Parse left child and insert
            left_child = cls.from_string(s[i : j - 1])
            if left_child is not None:
                node.left = left_child

            # Check for right child
            if j < len(s) and s[j] == "[":
                balance = 1
                k = j + 1
                while k < len(s) and balance > 0:
                    if s[k] == "[":
                        balance += 1
                    elif s[k] == "]":
                        balance -= 1
                    k += 1

                # Parse right child and insert
                right_child = cls.from_string(s[j : k - 1])
                if right_child is not None:
                    node.right = right_child

        return node

    def __repr__(self):
        """
        Returns a string representation of the node and its children.
        """
        left = f"{self.left}" if self.left is not None else ""
        right = f"{self.right}" if self.right is not None else ""
        val = self.value if self.value is not None else ""
        return f"[{val}{left}{right}]"

    def __hash__(self):
        """
        Returns a hash of the node.
        """
        return hash(str(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def is_leaf(self):
        return True if self.left is None and self.right is None else False


class Dend(Vector):
    def __reduce(self):
        self.data = {k: v for (k, v) in self.items() if v != 0}

    def vee(self, other):
        output = Dend()
        for x, y in product(self.items(), other.items()):
            b1, s1 = x
            b2, s2 = y
            s = s1 * s2
            b = PBT()
            b.left = b1
            b.right = b2
            output += Dend({b: s})

        return output

    def prec(self, other):
        if self.is_zero() or other.is_zero():
            return Dend()

        @Dend.linear_map
        def prec_basis(b):
            if b.is_leaf():
                return Dend()
            left = Dend.to_vec(b.left)
            right = Dend.to_vec(b.right)
            return left.vee(right @ other)

        return prec_basis(self)

    def succ(self, other):
        if self.is_zero() or other.is_zero():
            return Dend()

        @Dend.linear_map
        def succ_basis(b):
            if b.is_leaf():
                return Dend()
            left = Dend.to_vec(b.left)
            right = Dend.to_vec(b.right)
            return (left @ self).vee(right)

        return succ_basis(other)

    def __matmul__(self, other):
        u = Dend.to_vec(PBT())
        s = self - u
        t = other - u
        result = self + other + self.prec(t) + s.succ(other)
        return result if not s.is_zero() and not t.is_zero() else result - u
