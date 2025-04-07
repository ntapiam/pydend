import pytest
from collections import Counter
from dend.word import Letter, Word, QShuffle

# Tests for Letter class equality
def test_letter_equality_same_content():
    # Same content, different initialization
    letter1 = Letter({1: 2, 3: 1})
    letter2 = Letter({1: 2, 3: 1})
    letter3 = Letter(Counter({1: 2, 3: 1}))
    letter4 = Letter((1, 1, 3))
    
    assert letter1 == letter2
    assert letter1 == letter3
    assert letter1 == letter4
    assert letter3 == letter4

def test_letter_equality_different_content():
    letter1 = Letter({1: 2, 3: 1})
    letter2 = Letter({1: 1, 3: 2})
    letter3 = Letter({1: 2, 2: 1})
    letter4 = Letter((1, 1, 2))
    
    assert letter1 != letter2
    assert letter1 != letter3
    assert letter1 != letter4
    assert letter3 == letter4

# Tests for Word class equality
def test_word_equality_same_content():
    # Same content, different initialization
    word1 = Word([Letter({1: 2, 3: 1}), Letter({2: 1, 4: 2})])
    word2 = Word([Letter({1: 2, 3: 1}), Letter({2: 1, 4: 2})])
    word3 = Word([Counter({1: 2, 3: 1}), Counter({2: 1, 4: 2})])
    word4 = Word([(1, 1, 3), (2, 4, 4)])
    
    assert word1 == word2
    assert word1 == word3
    assert word2 == word4

def test_word_equality_different_content():
    word1 = Word([Letter({1: 2, 3: 1}), Letter({2: 1, 4: 2})])
    word2 = Word([Letter({1: 2, 3: 1}), Letter({2: 1, 4: 1})])  # Different second letter
    word3 = Word([Letter({1: 2, 3: 1})])  # Different length
    word4 = Word([Letter({2: 1, 4: 2}), Letter({1: 2, 3: 1})])  # Same letters, different order
    
    assert word1 != word2
    assert word1 != word3
    assert word1 != word4

def test_word_equality_complex_cases():
    # Words with multiple, complex letters
    word1 = Word([Letter({1: 3, 2: 2, 5: 1}), Letter({3: 4, 7: 2, 9: 1}), Letter({0: 1, 6: 3})])
    word2 = Word([(1, 1, 1, 2, 2, 5), (3, 3, 3, 3, 7, 7, 9), (0, 6, 6, 6)])
    word3 = Word([Counter({1: 3, 2: 2, 5: 1}), Counter({3: 4, 7: 2, 9: 1}), Counter({0: 1, 6: 3})])
    
    assert word1 == word2
    assert word1 == word3
    assert word2 == word3

def test_word_equality_non_word():
    word = Word([Letter({1: 2, 3: 1}), Letter({2: 1, 4: 2})])
    list_obj = [Letter({1: 2, 3: 1}), Letter({2: 1, 4: 2})]
    
    assert word != list_obj
    assert word != "not a word"
    assert word != 42

# Tests for QShuffle.cat
def test_qshuffle_init():
    # Create simple QShuffle objects
    w1 = Word([Letter({1: 1}), Letter({2: 1})])
    qs1 = QShuffle.to_vec(w1)
    
    # Check that the QShuffle was created correctly
    assert w1 in qs1.keys()
    assert qs1[w1] == 1

def test_qshuffle_cat_simple():
    
    # Create simple QShuffle objects
    w1 = Word([Letter((1,))])  # Word with single letter {1: 1}
    w2 = Word([Letter((2,))])  # Word with single letter {2: 1}
    
    qs1 = QShuffle.to_vec(w1)
    qs2 = QShuffle.to_vec(w2)
    
    # Expected result: a word with two letters [Letter((1,)), Letter((2,))]
    expected = QShuffle.to_vec(Word([Letter((1,)), Letter((2,))]))
    result = qs1.cat(qs2)
    
    assert result == expected

def test_qshuffle_cat_complex():
    # Create more complex QShuffle objects
    w1 = Word([Letter({1: 2, 3: 1}), Letter({4: 1})])
    w2 = Word([Letter({5: 1}), Letter({6: 2, 7: 1})])
    w3 = Word([Letter({8: 3, 9: 1})])
    
    # Create linear combinations
    qs1 = 2 * QShuffle.to_vec(w1) + 3 * QShuffle.to_vec(w2)
    qs2 = 4 * QShuffle.to_vec(w3)
    
    result = qs1.cat(qs2)
    
    # Expected words in the result
    expected_w1_w3 = Word([Letter({1: 2, 3: 1}), Letter({4: 1}), Letter({8: 3, 9: 1})])
    expected_w2_w3 = Word([Letter({5: 1}), Letter({6: 2, 7: 1}), Letter({8: 3, 9: 1})])
    
    # Check that the result has the expected terms with correct coefficients
    assert expected_w1_w3 in result.keys()
    assert expected_w2_w3 in result.keys()
    assert result[expected_w1_w3] == 2 * 4  # 2 (coefficient of w1) * 4 (coefficient of w3)
    assert result[expected_w2_w3] == 3 * 4  # 3 (coefficient of w2) * 4 (coefficient of w3)

def test_qshuffle_cat_identity():
    # Create a QShuffle object
    w = Word([Letter({1: 2, 3: 1}), Letter({4: 1})])
    qs = QShuffle.to_vec(w)
    unit = QShuffle.unit()
    
    # Test identity property: unit().cat(qs) = qs = qs.cat(unit())
    left_identity = unit.cat(qs)
    right_identity = qs.cat(unit)
    
    assert w in left_identity.keys() and left_identity[w] == 1
    assert w in right_identity.keys() and right_identity[w] == 1
    assert left_identity == qs
    assert right_identity == qs

def test_qshuffle_cat_associativity():
    # Create QShuffle objects
    w1 = Word([Letter({1: 1})])
    w2 = Word([Letter({2: 1})])
    w3 = Word([Letter({3: 1})])
    
    qs1 = QShuffle.to_vec(w1)
    qs2 = QShuffle.to_vec(w2)
    qs3 = QShuffle.to_vec(w3)
    
    # Test associativity: (qs1.cat(qs2)).cat(qs3) = qs1.cat(qs2.cat(qs3))
    left_assoc = (qs1.cat(qs2)).cat(qs3)
    right_assoc = qs1.cat(qs2.cat(qs3))
    
    # Both should equal a QShuffle containing Word([Letter({1: 1}), Letter({2: 1}), Letter({3: 1})])
    expected_word = Word([Letter({1: 1}), Letter({2: 1}), Letter({3: 1})])
    
    assert expected_word in left_assoc.keys() and left_assoc[expected_word] == 1
    assert expected_word in right_assoc.keys() and right_assoc[expected_word] == 1
    assert left_assoc == right_assoc

def test_qshuffle_succ_sh_empty_words():
    
    # Test with empty word on left
    empty = QShuffle.to_vec(Word([]))
    w1 = QShuffle.to_vec(Word([Letter({1: 1})]))
    
    result = empty.succ_sh(w1)
    assert result == w1
    
    # Test with empty word on right
    result = w1.succ_sh(empty)
    assert result == QShuffle()

def test_qshuffle_succ_sh_simple():
    
    # Test with single letter words
    w1 = QShuffle.to_vec(Word([Letter({1: 1})]))
    w2 = QShuffle.to_vec(Word([Letter({2: 1})]))
    
    result = w1.succ_sh(w2)
    expected_word = Word([Letter({1: 1}), Letter({2: 1})])
    assert result == QShuffle.to_vec(expected_word)

def test_qshuffle_matmul():

    w1 = Word([Letter({1: 1})])
    w2 = Word([Letter({2: 1}), Letter((3,))])

    qs1 = QShuffle.to_vec(w1)
    qs2 = QShuffle.to_vec(w2)
    result = qs1 @ qs2
    expected = QShuffle.to_vec(Word([Letter((1,)), Letter((2,)), Letter((3,))])) + QShuffle.to_vec(Word([Letter((2,)), Letter((1,)), Letter((3,))])) + QShuffle.to_vec(Word([Letter((2,)), Letter((3,)), Letter((1,))]))

    assert result == expected

def test_qshuffle_mul():
    w1 = Word([Letter({1: 1})])
    w2 = Word([Letter({2: 1}), Letter((3,))])

    qs1 = QShuffle.to_vec(w1)
    qs2 = QShuffle.to_vec(w2)
    result = qs1 * qs2
    expected = QShuffle.to_vec(Word([Letter((1,)), Letter((2,)), Letter((3,))]))  \
        + QShuffle.to_vec(Word([Letter((2,)), Letter((1,)), Letter((3,))]))  \
        + QShuffle.to_vec(Word([Letter((2, 1)), Letter((3,))]))  \
        + QShuffle.to_vec(Word([Letter((2,)), Letter((3,)), Letter((1,))]))  \
        + QShuffle.to_vec(Word([Letter((2,)), Letter((1,3))]))

    assert result == expected