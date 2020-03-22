import pytest

from justree import Tree


def test_default_usage():
    tpl = (1, [(2, []), (3, [])])
    tr = Tree(value=1, children=(Tree(value=2, children=()), Tree(value=3, children=()),))
    assert Tree.from_tuple(tpl) == tr


def test_freeze_assert():
    with pytest.raises(AssertionError):
        hash(Tree(None))
