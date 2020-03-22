import pytest

from justree import Tree


def test_default_usage():
    tpl = (1, [(2, []), (3, [])])
    tr = Tree(value=1, children=(Tree(value=2, children=()), Tree(value=3, children=()),))
    assert tr == Tree.from_tuple(tpl)


def test_tree_append():
    tpl = (1, [(2, []), (4, [])])
    tree = Tree(value=1, children=(Tree(value=2, children=()),))
    tree.append(Tree(value=4, children=()))
    assert tree == Tree.from_tuple(tpl)


def test_freeze_assert():
    with pytest.raises(AssertionError):
        hash(Tree(None))
