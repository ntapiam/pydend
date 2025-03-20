from dend import STree, Tridend
from fractions import Fraction

Y = STree().insert_left().insert_right()
lY = STree().insert_left().insert_right([STree().insert_left().insert_right()])
Yl = STree().insert_right().insert_left([STree().insert_left().insert_right()])
W = STree().insert_left().insert_left().insert_left()

def test_repr_single_node():
    root = STree()
    assert repr(root) == "[]"

def test_repr_with_children():
    root = STree()
    root.insert_left().insert_right()
    assert repr(root) == "[[][]]"

def test_deeply_nested_tree():
    root = STree()
    root.insert_left()
    root.insert_right()
    root.children[0].insert_left()
    root.children[0].insert_right()
    root.children[1].insert_left()
    root.children[1].insert_right()
    assert repr(root) == "[[[][]][[][]]]"

def test_prec_sh():
    x = Tridend.to_vec(Y)
    y = Tridend.to_vec(Y)

    result = x.prec_sh(y)

    expected = Tridend.to_vec(lY)

    assert result == expected

def test_product():
    x = Tridend.to_vec(Y)
    y = Tridend.to_vec(Y)
    u = Tridend.to_vec(STree())

    assert x @ u == x
    assert u @ y == y

    assert x * u == x
    assert u * y == y

    expected = Tridend.to_vec(lY) + Tridend.to_vec(Yl)

    assert x @ y == expected

    expected += Tridend.to_vec(W)

    assert x * y == expected
