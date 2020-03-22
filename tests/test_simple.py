import pytest

from justree import Tree


def test_default_usage():
    tpl = (1, [(2, []), (3, [])])
    tr = Tree(value=1, children=(Tree(value=2, children=()), Tree(value=3, children=()),))
    assert tr == Tree.from_tuple(tpl)


def test_tree_append():
    tpl = (1, [(2, []), (4, [])])
    tree = Tree(value=1, children=(Tree(value=2, children=()),))

    # Check for default behavior
    tree.append(Tree(value=4, children=()))
    assert tree == Tree.from_tuple(tpl)

    # Check append behavior for a frozen tree
    tree.freeze()
    with pytest.raises(AssertionError):
        tree.append(Tree(value=1))


def test_tree_emplace():
    tpl = (1, [(2, []), (4, [])])
    tree = Tree(value=1, children=(Tree(value=2, children=()),))

    # Check for default behavior
    tree.emplace(4)
    assert tree == Tree.from_tuple(tpl)

    # Check emplace behavior for a frozen tree
    tree.freeze()
    with pytest.raises(AssertionError):
        tree.emplace(1)


def test_tree_insert():
    # Check behavior for a single-layer insertion
    tpl = (1, [(2, []), ])
    tree = Tree(value=1)
    tree.insert(0, Tree(value=2))
    assert tree == Tree.from_tuple(tpl)

    # Check behavior for a deep insertion
    tpl = ("a", [(2, [("a", []), ("b", [])]), (3, [("a", []), ])])
    tree = Tree(value="a", children=(Tree(value=2, children=()), Tree(value=3, children=()),))
    node_a = Tree(value="a")
    node_b = Tree(value="b")
    tree.insert((0, 1), node_a)
    tree.insert((0, 1), node_b)
    tree.insert((1, 1), node_a)
    assert tree == Tree.from_tuple(tpl)

    # Check for IndexError when invalid index is presented
    with pytest.raises(IndexError):
        tree.insert((1, 2, 3, 4, 5), node_a)

    # Check for TypeError when invalid type of index is presented
    with pytest.raises(TypeError):
        tree.insert("b", node_a)

    # Check insert behavior for a frozen tree
    tree.freeze()
    with pytest.raises(AssertionError):
        tree.insert(0, node_a)


def test_tree_getitem():
    tpl = ("a", [(2, [(3, []), ]), ])
    tree = Tree.from_tuple(tpl)

    # Check for single indexing
    assert tree[0].value == tpl[1][0][0]

    # Check for deep indexing
    assert tree[(0, 0)].value == tpl[1][0][1][0][0]

    # Check for IndexError when invalid index is presented
    with pytest.raises(IndexError):
        _ = tree[1]

    # Check for TypeError when invalid type of index is presented
    with pytest.raises(TypeError):
        _ = tree["a"]


def test_tree_setitem():
    original_tpl = ("a", [(2, [(3, []), ]), ])
    mutated_tpl = ("a", [("b", [("c", []), ]), ])
    tree = Tree.from_tuple(original_tpl)
    tree[0] = Tree(value="b", children=(Tree(value="c", children=()),))

    # Check for default behavior
    assert tree == Tree.from_tuple(mutated_tpl)

    # Check for IndexError when invalid index is presented
    with pytest.raises(IndexError):
        tree[4] = Tree(value="dd")

    # Check for IndexError when invalid type of index is presented
    with pytest.raises(TypeError):
        tree["a"] = Tree(value="a")

    # Check behavior for a frozen tree
    tree.freeze()
    with pytest.raises(AssertionError):
        tree["b"] = Tree(value="a")


def test_tree_len():
    original_tpl = ("a", [(2, []), (2, []), ])
    tree = Tree.from_tuple(original_tpl)
    assert len(original_tpl[1]) == len(tree)


def test_tree_size():
    original_tpl = ("a", [(2, [("a", []), ("b", [])]), (3, [("a", []), ])])
    tree = Tree.from_tuple(original_tpl)
    assert tree.size() == 6
    tree.freeze()
    assert tree.size() == 6


def test_tree_delitem():
    original_tpl = ("a", [(2, [(3, [("a", [(2, [(3, []), ]), ])]), ]), ])
    mutated_tpl = ("a", [(2, [(3, [("a", [])]), ]), ])
    tree = Tree.from_tuple(original_tpl)

    # Check for default behavior
    del tree[(0, 0, 0, 0)]
    assert tree == Tree.from_tuple(mutated_tpl)

    # Check for IndexError when invalid index is presented
    with pytest.raises(IndexError):
        del tree[(0, 0, 0, 1)]

    # Check for IndexError when invalid type of index is presented
    with pytest.raises(TypeError):
        del tree["a"]

    # Check behavior for a frozen tree
    tree.freeze()
    with pytest.raises(AssertionError):
        del tree[(0, 0, 0)]


def test_freeze_assert():
    with pytest.raises(AssertionError):
        hash(Tree(None))
