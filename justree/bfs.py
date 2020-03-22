from collections import deque
from typing import Iterable, List, Tuple, Deque, Optional, Union

from .tools import reversed_enumerate, T
from .tree_node import TreeNode


def non_recursive_tree_bfs_forward_original(self: T) -> Iterable[T]:
    assert isinstance(self, TreeNode)
    q: Deque[TreeNode] = deque([self])
    while q:
        t = q.popleft()
        q.extend(t._children)
        yield t


def non_recursive_tree_bfs_forward_mirror(self: T) -> Iterable[T]:
    assert isinstance(self, TreeNode)
    q: Deque[TreeNode] = deque([self])
    while q:
        t = q.popleft()
        q.extend(reversed(t._children))
        yield t


def non_recursive_tree_bfs_reverse_original(self: T) -> List[T]:
    assert isinstance(self, TreeNode)
    q: Deque[TreeNode] = deque([self])
    r: List[TreeNode] = [self]
    while q:
        t = q.popleft()
        q.extend(t._children)
        r.extend(t._children)
    r.reverse()
    return r


def non_recursive_tree_bfs_reverse_mirror(self: T) -> List[T]:
    assert isinstance(self, TreeNode)
    q: Deque[TreeNode] = deque([self])
    r: List[TreeNode] = [self]
    while q:
        t = q.popleft()
        q.extend(reversed(t._children))
        r.extend(reversed(t._children))
    r.reverse()
    return r


_Int = Union[int, float]


def bfs_ex_preparation(depth: Optional[_Int]) -> _Int:
    return float('inf') if depth is None else depth


def non_recursive_tree_bfs_forward_original_ex(self: T, depth: Optional[_Int] = None) \
        -> Iterable[Tuple[T, int, Tuple[int, ...]]]:
    assert isinstance(self, TreeNode)
    depth = bfs_ex_preparation(depth)
    q: Deque[Tuple[TreeNode, int, Tuple[int, ...]]] = deque([(self, 1, ())])
    while q:
        t, d, i = q.popleft()
        if d < depth:
            q.extend((ct, d + 1, i + (ci,)) for ci, ct in enumerate(t._children))
        yield t, d, i


def non_recursive_tree_bfs_forward_mirror_ex(self: T, depth: Optional[_Int] = None) \
        -> Iterable[Tuple[T, int, Tuple[int, ...]]]:
    assert isinstance(self, TreeNode)
    depth = bfs_ex_preparation(depth)
    q: Deque[Tuple[TreeNode, int, Tuple[int, ...]]] = deque([(self, 1, ())])
    while q:
        t, d, i = q.popleft()
        if d < depth:
            q.extend((ct, d + 1, i + (ci,)) for ci, ct in reversed_enumerate(t._children))
        yield t, d, i


def non_recursive_tree_bfs_reverse_original_ex(self: T, depth: Optional[_Int] = None) \
        -> List[Tuple[T, int, Tuple[int, ...]]]:
    assert isinstance(self, TreeNode)
    depth = bfs_ex_preparation(depth)
    q: Deque[Tuple[TreeNode, int, Tuple[int, ...]]] = deque([(self, 1, ())])
    r: List[Tuple[TreeNode, int, Tuple[int, ...]]] = [(self, 1, ())]
    while q:
        t, d, i = q.popleft()
        if d < depth:
            q.extend((ct, d + 1, i + (ci,)) for ci, ct in enumerate(t._children))
            r.extend((ct, d + 1, i + (ci,)) for ci, ct in enumerate(t._children))
    r.reverse()
    return r


def non_recursive_tree_bfs_reverse_mirror_ex(self: T, depth: Optional[_Int] = None) \
        -> List[Tuple[T, int, Tuple[int, ...]]]:
    assert isinstance(self, TreeNode)
    depth = bfs_ex_preparation(depth)
    q: Deque[Tuple[TreeNode, int, Tuple[int, ...]]] = deque([(self, 1, ())])
    r: List[Tuple[TreeNode, int, Tuple[int, ...]]] = [(self, 1, ())]
    while q:
        t, d, i = q.popleft()
        if d < depth:
            q.extend((ct, d + 1, i + (ci,)) for ci, ct in reversed_enumerate(t._children))
            r.extend((ct, d + 1, i + (ci,)) for ci, ct in reversed_enumerate(t._children))
    r.reverse()
    return r
