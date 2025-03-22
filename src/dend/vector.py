from collections import UserDict
from fractions import Fraction
from functools import reduce
from operator import add


class Vector(UserDict):
    # constructor should call super() and then __reduce
    def __init__(self, data=None):
        super().__init__(data)
        self.__reduce()

    @classmethod
    def to_vec(cls, b):
        return cls({b: Fraction(1, 1)})

    def outer(self, other):
        return self.__class__(
            {
                (b1, b2): k1 * k2
                for (b1, k1) in self.items()
                for (b2, k2) in other.items()
            }
        )

    def __reduce(self):
        self.data = {k: v for (k, v) in self.items() if v != 0}

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Operand must be of type Vector")

        result = self.__class__()
        for key in self.keys() | other.keys():
            result[key] = self.get(key, Fraction()) + other.get(key, Fraction())
        result.__reduce()
        return result

    def __neg__(self):
        result = self.__class__()
        for key in self.keys():
            result[key] = -self[key]

        result.__reduce()
        return result

    def __sub__(self, other):
        return self + (-other)

    def __repr__(self):
        output = ""
        for n, (k, v) in enumerate(self.items()):
            coef = ""
            s = ' ⊗ '.join(str(b) for b in k) if isinstance(k, tuple) else str(k)
            if v != Fraction(1) and v != -Fraction(1):
                coef += f"{abs(v)}·"

            if n == 0:
                if v >= 0:
                    output += f"{coef}{s}"
                else:
                    output += f"-{coef}{s}"

            else:
                if v >= 0:
                    output += f" + {coef}{s}"
                else:
                    output += f" - {coef}{s}"

        return output

    def is_zero(self):
        self._Vector__reduce()
        return True if self.data == {} else False

    def __rmul__(self, k):
        return self.__class__({b: s * k for b, s in self.items()})

    def __rmatmul__(self, k):
        return self.__class__({b: s * k for b, s in self.items()})

    @classmethod
    def linear_map(cls, func):
        def lin_ext(v):
            return reduce(add, (r * func(b) for (b, r) in v.items()), cls())

        return lin_ext
