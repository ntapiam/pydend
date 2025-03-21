from dend import STree, Tridend
from fractions import Fraction

u = Tridend.unit()
y = Tridend.vee(u, u)
w = Tridend.vee(u, u, u)
ly = Tridend.vee(u, y)
yl = Tridend.vee(y, u)


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
    result = y.prec_sh(y)

    assert result == ly

def test_product():
    x = y

    assert x @ u == x
    assert u @ y == y

    assert x * u == x
    assert u * y == y

    expected = ly + yl

    assert x @ y == expected

    expected += w

    assert x * y == expected

def test_parse():
    # Test single node
    assert repr(STree.parse("[]")) == "[]"
    
    # Test two children
    assert repr(STree.parse("[[][]]")) == "[[][]]"
    assert STree.parse("[[][]]") == STree().insert_left().insert_right()
    
    # Test three children
    assert repr(STree.parse("[[][][]]")) == "[[][][]]"
    assert STree.parse("[[][][]]") == STree().insert_left().insert_left().insert_right()
    
    # Test deeply nested structure
    nested = "[[[][]][[][]]]"  # Tree with two children, each having two children
    parsed = STree.parse(nested)
    manual = STree()
    manual.insert_left()
    manual.insert_right()
    manual.children[0].insert_left()
    manual.children[0].insert_right()
    manual.children[1].insert_left()
    manual.children[1].insert_right()
    assert repr(parsed) == nested
    assert parsed == manual
    
    # Test error cases
    try:
        STree.parse("[")  # Unmatched bracket
        assert False, "Should raise ValueError for unmatched bracket"
    except ValueError:
        pass

def test_coprod_sh():
    result = u.coprod_sh()
    expected = u.outer(u)

    assert result == expected

    result = y.coprod_sh()
    expected = y.outer(u) + u.outer(y)

    assert result == expected

    result = w.coprod_sh()
    expected = w.outer(u) + u.outer(w)

    assert result == expected

    z = w.prec_sh(y)
    result = z.coprod_sh()
    expected = z.outer(u) + u.outer(z) + y.outer(w)

    assert result == expected

    z = ly.dot(y)
    result = z.coprod_sh()
    expected = z.outer(u) + u.outer(z)

    assert result == expected

def test_coprod_qsh():
    result = u.coprod_qsh()
    expected = u.outer(u)

    assert result == expected

    result = y.coprod_qsh()
    expected = y.outer(u) + u.outer(y)

    assert result == expected

    result = w.coprod_qsh()
    expected = w.outer(u) + u.outer(w)

    assert result == expected

    z = w.prec_qsh(y)
    result = z.coprod_qsh()
    expected = z.outer(u) + u.outer(z) + y.outer(w)

    assert result == expected

    z = ly.dot(y)
    result = z.coprod_qsh()
    expected = z.outer(u) + u.outer(z) + y.outer(w)

    assert result == expected
