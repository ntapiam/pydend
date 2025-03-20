from fractions import Fraction

from vector import Vector


def test_add():
    x = Vector({(): Fraction(1), (1,): Fraction(2, 1)})
    y = Vector({(1,): Fraction(-2, 1)})

    assert (x + y) == Vector({(): Fraction(1),})

def test_vector_repr():
    v = Vector({0: Fraction(-3, 2), -1: Fraction(-4, 3), 2: Fraction(5)})
    expected = "-3/2·0 - 4/3·-1 + 5·2"
    assert repr(v) == expected

def test_is_zero():
    # Empty vector should be zero
    v1 = Vector({})
    assert v1.is_zero()
    
    # Vector with only zero components should be zero
    v2 = Vector({(): Fraction(0), (1,): Fraction(0)})
    assert v2.is_zero()
    
    # Vector with any non-zero component should not be zero
    v3 = Vector({(): Fraction(0), (1,): Fraction(1)})
    assert not v3.is_zero()

def test_linear_map():
    v = Vector({0: Fraction(2), 1: Fraction(3)})
    func = lambda x: Vector({x + 1: Fraction(1)})
    lin_map = Vector.linear_map(func)

    result = lin_map(v)
    expected = Vector({1: Fraction(2), 2: Fraction(3)})

    assert result == expected
