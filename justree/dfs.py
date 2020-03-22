from itertools import repeat
from typing import Iterable, List, Tuple, Union, Optional

from .tools import reversed_enumerate, T
from .tree_node import TreeNode


def non_recursive_tree_dfs_forward_original(self: T) -> Iterable[T]:
    assert isinstance(self, TreeNode)
    q: List[TreeNode] = [self]
    while q:
        t = q.pop()
        q.extend(reversed(t._children))
        yield t


def non_recursive_tree_dfs_forward_mirror(self: T) -> Iterable[T]:
    assert isinstance(self, TreeNode)
    q: List[TreeNode] = [self]
    while q:
        t = q.pop()
        q.extend(t._children)
        yield t


def non_recursive_tree_dfs_reverse_original(self: T) -> Iterable[T]:
    assert isinstance(self, TreeNode)
    q: List[Tuple[bool, TreeNode]] = [(True, self)]
    while q:
        f, t = q[-1]
        if f:
            q[-1] = (False, t)
            q.extend(zip(repeat(True), t._children))
        else:
            yield q.pop()[1]


def non_recursive_tree_dfs_reverse_mirror(self: T) -> Iterable[T]:
    assert isinstance(self, TreeNode)
    q: List[Tuple[bool, TreeNode]] = [(True, self)]
    while q:
        f, t = q[-1]
        if f:
            q[-1] = (False, t)
            q.extend(zip(repeat(True), reversed(t._children)))
        else:
            yield q.pop()[1]


_Int = Union[int, float]


def bfs_ex_preparation(depth: Optional[_Int]) -> _Int:
    return float('inf') if depth is None else depth


def non_recursive_tree_dfs_forward_original_ex(self: T, depth: Optional[_Int] = None) \
        -> Iterable[Tuple[T, int, Tuple[int, ...]]]:
    assert isinstance(self, TreeNode)
    depth = bfs_ex_preparation(depth)
    q: List[Tuple[TreeNode, int, Tuple[int, ...]]] = [(self, 1, ())]
    while q:
        t, d, i = q.pop()
        if d < depth:
            q.extend((ct, d + 1, i + (ci,)) for ci, ct in reversed_enumerate(t._children))
        yield t, d, i


def non_recursive_tree_dfs_forward_mirror_ex(self: T, depth: Optional[_Int] = None) \
        -> Iterable[Tuple[T, int, Tuple[int, ...]]]:
    assert isinstance(self, TreeNode)
    depth = bfs_ex_preparation(depth)
    q: List[Tuple[TreeNode, int, Tuple[int, ...]]] = [(self, 1, ())]
    while q:
        t, d, i = q.pop()
        if d < depth:
            q.extend((ct, d + 1, i + (ci,)) for ci, ct in enumerate(t._children))
        yield t, d, i


def non_recursive_tree_dfs_reverse_original_ex(self: T, depth: Optional[_Int] = None) \
        -> Iterable[Tuple[T, int, Tuple[int, ...]]]:
    assert isinstance(self, TreeNode)
    depth = bfs_ex_preparation(depth)
    q: List[Tuple[bool, TreeNode, int, Tuple[int, ...]]] = [(True, self, 1, ())]
    while q:
        f, t, d, i = q[-1]
        if f:
            q[-1] = (False, t, d, i)
            if d < depth:
                q.extend((True, ct, d + 1, i + (ci,)) for ci, ct in enumerate(t._children))
        else:
            yield q.pop()[1:]


def non_recursive_tree_dfs_reverse_mirror_ex(self: T, depth: Optional[_Int] = None) \
        -> Iterable[Tuple[T, int, Tuple[int, ...]]]:
    assert isinstance(self, TreeNode)
    depth = bfs_ex_preparation(depth)
    q: List[Tuple[bool, TreeNode, int, Tuple[int, ...]]] = [(True, self, 1, ())]
    while q:
        f, t, d, i = q[-1]
        if f:
            q[-1] = (False, t, d, i)
            if d < depth:
                q.extend((True, ct, d + 1, i + (ci,)) for ci, ct in reversed_enumerate(t._children))
        else:
            yield q.pop()[1:]
