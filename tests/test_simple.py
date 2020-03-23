import pytest

from justree import Tree
from typing import Tuple, List


def test_default_usage():
    tpl = (1, [(2, []), (3, [])])
    tr = Tree(value=1, children=(Tree(value=2, children=()), Tree(value=3, children=()),))
    assert tr == Tree.from_tuple(tpl)


def test_tree_equals():
    tpl_f = (1, [(2, []), (3, [])])
    tpl_t = (1, [(2, []), (3, [(2, []), ]), ])

    # Check same trees for equality
    tree_1 = Tree.from_tuple(tpl_f)
    tree_2 = Tree.from_tuple(tpl_f)
    assert tree_1 == tree_2

    # Check different trees for equality
    tree_2 = Tree.from_tuple(tpl_t)
    assert tree_1 != tree_2


def test_tree_hash():
    tpl = (1, [(2, []), ])
    tree = Tree.from_tuple(tpl)

    # Check behavior for non-frozen tree
    with pytest.raises(AssertionError):
        _h = hash(tree)

    # Check default behavior
    tree.freeze()
    assert isinstance(hash(tree), int)


def test_tree_str():
    tpl = (1, [(2, []), ])
    expected_str = "(1 (2))"
    tree = Tree.from_tuple(tpl)
    assert str(tree) == expected_str


def test_tree_repr():
    tpl = (1, [(2, []), ])
    expected_str = "Tree(value=1, children=( Tree(value=2, children=()),))"
    tree = Tree.from_tuple(tpl)
    assert repr(tree) == expected_str


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
        tree[0] = Tree(value="a")


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


def test_tree_height():
    tpl = ("a", [(2, [(3, [("a", [(2, [(3, []), ]), ])]), ]), ])
    tree = Tree.from_tuple(tpl)
    assert tree.height() == 6
    tree.freeze()
    assert tree.height() == 6


def test_tree_freeze():
    tpl = ("a", [(2, [(3, [("a", [(2, [(3, []), ]), ])]), ]), ])
    tree = Tree.from_tuple(tpl)
    tree.freeze()
    assert tree._is_frozen == True
    assert tree[0]._is_frozen == True
    assert tree[(0, 0)]._is_frozen == True


def test_tree_unfreeze():
    tpl = ("a", [(2, [(3, [("a", [(2, [(3, []), ]), ])]), ]), ])
    tree = Tree.from_tuple(tpl)

    # Check for unsafe way of in-place unfreeze
    tree.freeze()
    tree.make_unfreezed(unsafe=True)
    assert tree._is_frozen == False
    assert tree[(0, 0)]._is_frozen == False

    # Check for copying way of unfreeze
    tree.freeze()
    new_tree = tree.make_unfreezed()
    assert tree == new_tree
    assert tree._is_frozen == True
    assert new_tree._is_frozen == False


def test_tree_clone():
    tpl = ([1, 2], [(2, [(3, [("a", [(2, [(3, []), ]), ])]), ]), ])
    tree = Tree.from_tuple(tpl)

    # Check behavior for shallow copy
    copied_tree = tree.clone()
    assert copied_tree == tree
    copied_tree.value.append(1)
    assert copied_tree == tree

    # Check behavior for deep copy
    copied_tree = tree.clone(deep=True)
    assert copied_tree == tree
    copied_tree.value.append(1)
    assert copied_tree != tree


def test_tree_bfs():
    tpl = ("a", [(2, [(3, [("a", []), ("b", [])])]), ])
    tpl_bfs_case = ['(a (2 (3 (a) (b))))', '(2 (3 (a) (b)))', '(3 (a) (b))', '(a)', '(b)']
    tpl_bfs_case_mirrored = ['(a (2 (3 (a) (b))))', '(2 (3 (a) (b)))', '(3 (a) (b))', '(b)', '(a)']
    tree = Tree.from_tuple(tpl)

    # Test case for basic bfs
    bfs_case = [str(t) for t in tree.bfs()]
    assert bfs_case == tpl_bfs_case

    # Test case for reversed bfs
    bfs_case_reversed = [str(t) for t in tree.bfs(reverse=True)]
    assert bfs_case_reversed == tpl_bfs_case[::-1]

    # Test case for mirrored bfs
    bfs_case_mirrored = [str(t) for t in tree.bfs(mirror=True)]
    assert bfs_case_mirrored == tpl_bfs_case_mirrored

    # Test case for both reversed and mirrored bfs
    bfs_case_mirrored_reversed = [str(t) for t in tree.bfs(reverse=True, mirror=True)]
    assert bfs_case_mirrored_reversed == tpl_bfs_case_mirrored[::-1]


def test_tree_bfs_extended():
    def extract_result(bfs_result: object) -> Tuple[List[str], List[int]]:
        container = list(bfs_result) if not isinstance(bfs_result, list) else bfs_result
        nodes_tuple_ = [str(t[0]) for t in container]
        nodes_positions_ = [t[1] for t in container]
        return nodes_tuple_, nodes_positions_

    tpl = ("a", [(2, [(3, [("a", []), ("b", [])])]), ])
    tpl_bfs_case_nodes = ['(a (2 (3 (a) (b))))', '(2 (3 (a) (b)))', '(3 (a) (b))', '(a)', '(b)']
    tpl_bfs_case_pos = [1, 2, 3, 4, 4]
    tree = Tree.from_tuple(tpl)

    # Test case for basic bfs_ex
    nodes_tuple, nodes_positions = extract_result(tree.bfs_ex())
    assert nodes_tuple == tpl_bfs_case_nodes
    assert nodes_positions == tpl_bfs_case_pos

    # Test case for specified depth of bfs
    nodes_tuple, nodes_positions = extract_result(tree.bfs_ex(depth=3))
    assert nodes_tuple == tpl_bfs_case_nodes[:3]
    assert nodes_positions == tpl_bfs_case_pos[:3]

    # Test case for specified depth of reversed bfs
    nodes_tuple, nodes_positions = extract_result(tree.bfs_ex(depth=3, reverse=True))
    assert nodes_tuple == tpl_bfs_case_nodes[-3:-6:-1]
    assert nodes_positions == tpl_bfs_case_pos[-3:-6:-1]

    # Test case for both reversed and mirrored bfs
    nodes_tuple, nodes_positions = extract_result(tree.bfs_ex(reverse=True, mirror=True))
    assert nodes_positions == tpl_bfs_case_pos[::-1]
    tpl_bfs_case_mirrored_nodes = ['(a)', '(b)', '(3 (a) (b))', '(2 (3 (a) (b)))', '(a (2 (3 (a) (b))))']
    assert nodes_tuple == tpl_bfs_case_mirrored_nodes


def test_freeze_assert():
    with pytest.raises(AssertionError):
        hash(Tree(None))
