from dend.word import QShuffle, Word
from fractions import Fraction

def shuffle_exp(x, n):
    """
    Compute the shuffle product of x with itself n times.
    """
    result = QShuffle.unit()
    c = result
    for k in range(1, n + 1):
        c = Fraction(1, k) * c @ x
        result = result + c
    return result

def quasishuffle_exp(x, n):
    """
    Compute the shuffle product of x with itself n times.
    """
    result = QShuffle.unit()
    c = result
    for k in range(1, n + 1):
        c = Fraction(1, k) * c * x
        result = result + c
    return result


def cat_exp(x, n):
    """
    Compute the shuffle product of x with itself n times.
    """
    result = QShuffle.unit()
    c = result
    for k in range(1, n + 1):
        c = Fraction(1, k) * c.cat(x)
        result = result + c
    return result

if __name__ == "__main__":
    x = QShuffle.to_vec(Word([1,2])) 
    y = QShuffle.to_vec(Word([3]))

    # Note that in all that follows the printed terms are not naturally ordered
    # ε stands for the empty word
    print("x:", x)
    print("y:", y)
    print("Shuffle product:", x @ y) # Shuffle product
    print("Quasi-shuffle product:", x * y) # Quasi-shuffle product
    print("Quasi-shuffle exponential (n = 5):", quasishuffle_exp(y, 5)) # Quasi-shuffle exponential
    print("Shuffle exponential (n = 5):", shuffle_exp(y, 5)) # Shuffle exponential
    print("Concatenation exponential (n = 5):", cat_exp(y, 5)) # Concatenation exponential