from collections import UserList, Counter

from .vector import Vector

class Letter(Counter):
    def __init__(self, input_data):
        if isinstance(input_data, (Counter, Letter, dict)):
            super().__init__(input_data)
        elif isinstance(input_data, int):
            super().__init__(Counter({input_data: 1}))
        elif isinstance(input_data, tuple) and all(isinstance(x, int) for x in input_data):
            super().__init__(Counter(input_data))
        else:
            raise ValueError("Input must be a Counter, Letter, or tuple of integers")

    def __mul__(self, other):
        return Letter(self + other)

    def __hash__(self):
        return hash(frozenset(self.items()))

    def __repr__(self):
        if len(self) == 1:
            return f"{list(self.items())[0][0]}"
        return '(' + ''.join([f"{k}^{v}" if v>1 else f"{k}" for k, v in self.items()]) + ')'

    def __eq__(self, other):
        if isinstance(other, Letter):
            return dict(self) == dict(other)
        else:
            return False
    
class Word(UserList):
    def __init__(self, input_data):
        if all(isinstance(x, Letter) for x in input_data):
            self.data = list(input_data)
        elif all(isinstance(x, (Counter, int)) for x in input_data):
            self.data = [Letter(x) for x in input_data]
        elif all(isinstance(x, tuple) and all(isinstance(y, int) for y in x) for x in input_data):
            self.data = [Letter(x) for x in input_data]
        else:
            raise ValueError("Input must be a list of Letters, Counters, or tuples of integers")

    def __hash__(self):
        return hash(frozenset(self.data))
    
    def __eq__(self, other):
        if isinstance(other, Word):
            return self.data == other.data
        else:
            return False

    def __repr__(self):
        if len(self) == 0:
            return 'ε'
        return ''.join(map(str, self.data))


class QShuffle(Vector):
    @staticmethod
    def unit():
        return QShuffle.to_vec(Word([]))

    def succ_sh(self, other):
        if not isinstance(other, QShuffle):
            raise ValueError("Can only shuffle with another QShuffle")
        
        @QShuffle.linear_map
        def succ_basis(b):
            w1, w2 = b
            if w1.data == []:
                return QShuffle.to_vec(w2)
            if w2.data == []:
                return QShuffle()

            left = QShuffle.to_vec(w1)
            right = QShuffle.to_vec(w2[:-1])
            last = QShuffle.to_vec((w2[-1],))
            return (left @ right).cat(last)

        return succ_basis(self.outer(other))

    def succ_qsh(self, other):
        if not isinstance(other, QShuffle):
            raise ValueError("Can only shuffle with another QShuffle")
        
        @QShuffle.linear_map
        def succ_basis(b):
            w1, w2 = b
            if w1.data == []:
                return QShuffle.to_vec(w2)
            if w2.data == []:
                return QShuffle()

            left = QShuffle.to_vec(w1)
            right = QShuffle.to_vec(w2[:-1])
            last = QShuffle.to_vec((w2[-1],))
            return (left * right).cat(last)

        return succ_basis(self.outer(other))

    def dot(self, other):
        if not isinstance(other, QShuffle):
            raise ValueError("Can only dot with another QShuffle")
        
        @QShuffle.linear_map
        def dot_basis(b):
            w1, w2 = b
            if w1.data == [] or w2.data == []:
                return QShuffle()
            left = QShuffle.to_vec(w1[:-1])
            right = QShuffle.to_vec(w2[:-1])
            last = QShuffle.to_vec((w1[-1]*w2[-1],))

            return (left * right).cat(last)

        return dot_basis(self.outer(other))

    def __matmul__(self, other):
        if not isinstance(other, QShuffle):
            raise ValueError("Can only multiply with another QShuffle")
        
        if self == QShuffle.unit():
            return other
        if other == QShuffle.unit():
            return self
        
        return self.succ_sh(other) + other.succ_sh(self)

    def __mul__(self, other):
        if not isinstance(other, QShuffle):
            raise ValueError("Can only multiply with another QShuffle")
        
        if self == QShuffle.unit():
            return other
        if other == QShuffle.unit():
            return self
        
        return self.succ_qsh(other) + other.succ_qsh(self) + self.dot(other)

    def cat(self, other):
        if not isinstance(other, QShuffle):
            raise ValueError("Can only concatenate QShuffle with another QShuffle")
        
        @QShuffle.linear_map
        def cat_basis(b):
            w1, w2 = b
            return QShuffle.to_vec(w1 + w2)
        
        return cat_basis(self.outer(other))
