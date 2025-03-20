from dend import PBT, Dend
from fractions import Fraction

def test_add():
    x = Dend({PBT(): Fraction(1)})
    y = Dend({PBT(): Fraction(-2)})

    assert (x + y) == Dend({PBT(): Fraction(-1),})

def test_repr_single_node_with_value():
    root = PBT(10)
    assert repr(root) == "[10]"

def test_repr_single_node_without_value():
    root = PBT()
    assert repr(root) == "[]"

def test_repr_with_children():
    root = PBT(10)
    root.insert_left(5)
    root.insert_right(15)
    assert repr(root) == "[10[5][15]]"

def test_repr_with_none_values():
    root = PBT().insert_left().insert_right(15)
    assert repr(root) == "[[][15]]"

def test_deeply_nested_tree():
    root = PBT(1)
    root.insert_left(2)
    root.insert_right(3)
    root.left.insert_left(4)
    root.left.insert_right(5)
    root.right.insert_left(6)
    root.right.insert_right(7)
    assert repr(root) == "[1[2[4][5]][3[6][7]]]"

def test_parse():
    string = "[10[5][3]]"
    result = PBT.from_string(string)
    expected = PBT(10).insert_left(5).insert_right(3)

    assert hash(result) == hash(expected)

def test_prec():
    Y = PBT().insert_left().insert_right()
    x = Dend.to_vec(Y)
    y = Dend.to_vec(Y)

    result = x.prec(y)
    expected = PBT()
    expected.left = PBT()
    expected.right = Y

    expected = Dend.to_vec(expected)

    assert result == expected

def test_product():
    x = Dend.to_vec(PBT().insert_left().insert_right())
    y = Dend.to_vec(PBT().insert_left().insert_right())
    u = Dend.to_vec(PBT())

    assert x @ u == x
    assert u @ y == y

    expected = Dend.to_vec(PBT.from_string("[[][[][]]]")) + Dend.to_vec(PBT.from_string("[[[][]][]]"))

    assert x @ y == expected
