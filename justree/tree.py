from collections import deque
from copy import copy, deepcopy
from itertools import repeat
from typing import Any, Callable, Iterable, List, NamedTuple, overload, Tuple, Optional

from .bfs import non_recursive_tree_bfs_forward_original, non_recursive_tree_bfs_forward_mirror, \
    non_recursive_tree_bfs_reverse_original, non_recursive_tree_bfs_reverse_mirror, \
    non_recursive_tree_bfs_forward_original_ex, non_recursive_tree_bfs_reverse_mirror_ex, \
    non_recursive_tree_bfs_reverse_original_ex, non_recursive_tree_bfs_forward_mirror_ex
from .dfs import non_recursive_tree_dfs_forward_original, non_recursive_tree_dfs_forward_mirror, \
    non_recursive_tree_dfs_reverse_original, non_recursive_tree_dfs_reverse_mirror, \
    non_recursive_tree_dfs_reverse_mirror_ex, non_recursive_tree_dfs_reverse_original_ex, \
    non_recursive_tree_dfs_forward_mirror_ex, non_recursive_tree_dfs_forward_original_ex
from .tree_node import TreeNode


class ImmediateReturn(NamedTuple):
    retval: Any


class Tree(TreeNode):
    value: Any
    _children: List['Tree']
    _is_frozen: bool
    _hash = None
    _size = None
    _height = None

    def __init__(self, value: Any, children: Iterable['Tree'] = ()) -> None:
        super().__init__()
        self.value = value
        self._children = list(children)
        self._is_frozen = False

    def __eq__(self, o: object) -> bool:
        return immediate_return_routine(non_recursive_tree_eq, (self, o))

    def __ne__(self, o: object) -> bool:
        return not (self == o)

    def __hash__(self) -> int:
        assert self._is_frozen
        if self._hash is None:
            self._hash = non_recursive_tree_hash(self)
        return self._hash

    def __str__(self) -> str:
        return non_recursive_tree_str(self)

    def __repr__(self) -> str:
        return non_recursive_tree_repr(self)

    def append(self, tree: 'Tree') -> None:
        assert not self._is_frozen
        self._children.append(tree)

    def emplace(self, o: Any) -> None:
        assert not self._is_frozen
        self._children.append(Tree(o))

    @overload
    def insert(self, index: int, tree: 'Tree') -> None:
        ...

    @overload
    def insert(self, indexes: Tuple[int, ...], tree: 'Tree') -> None:
        ...

    def insert(self, v: object, tree: 'Tree') -> None:
        assert not self._is_frozen
        if isinstance(v, int):
            self.insert((v,), tree)
        elif isinstance(v, tuple):
            non_recursive_tree_insert(self, v, tree)
        else:
            raise TypeError(indices_type_error(self, v))

    @overload
    def __getitem__(self, i: int) -> 'Tree':
        ...

    @overload
    def __getitem__(self, t: Tuple[int, ...]) -> 'Tree':
        ...

    def __getitem__(self, v: object) -> 'Tree':
        if isinstance(v, int):
            return self[v,]
        elif isinstance(v, tuple):
            return non_recursive_tree_getitem(self, v)
        else:
            raise TypeError(indices_type_error(self, v))

    @overload
    def __setitem__(self, i: int, o: 'Tree') -> None:
        ...

    @overload
    def __setitem__(self, t: Tuple[int, ...], o: 'Tree') -> None:
        ...

    def __setitem__(self, v: object, o: 'Tree') -> None:
        assert not self._is_frozen
        if isinstance(v, int):
            self[v,] = o
        elif isinstance(v, tuple):
            non_recursive_tree_setitem(self, v, o)
        else:
            raise TypeError(indices_type_error(self, v))

    @overload
    def __delitem__(self, i: int) -> None:
        ...

    @overload
    def __delitem__(self, t: Tuple[int, ...]) -> None:
        ...

    def __delitem__(self, v: object) -> None:
        assert not self._is_frozen
        if isinstance(v, int):
            del self[v,]
        elif isinstance(v, tuple):
            non_recursive_tree_delitem(self, v)
        else:
            raise TypeError(indices_type_error(self, v))

    def __len__(self) -> int:
        return len(self._children)

    def size(self) -> int:
        if self._is_frozen:
            if self._size is None:
                self._size = non_recursive_tree_size(self)
            return self._size
        else:
            return non_recursive_tree_size(self)

    def height(self) -> int:
        if self._is_frozen:
            if self._height is None:
                self._height = non_recursive_tree_height(self)
            return self._height
        else:
            return non_recursive_tree_height(self)

    def freeze(self) -> None:
        """
        Make Tree readonly in place
        :return: None
        """
        non_recursive_tree_freeze(self)

    def make_unfreezed(self, unsafe: bool = False, deep: bool = False) -> 'Tree':
        """
        Make writable copy of Tree
        :param unsafe: convert Tree to writable in place
        :param deep: cloning not only Tree's nodes but also nodes value
        :return: writable Tree
        """
        if unsafe:
            non_recursive_tree_unfreeze(self)
            return self
        else:
            return self.clone(deep)

    def clone(self, deep=False) -> 'Tree':
        """
        Clone the Tree
        :param deep: cloning not only Tree's nodes but also nodes value
        :return: clone of Tree
        """
        if deep:
            return deepcopy(self)
        else:
            return copy(self)

    def __copy__(self) -> 'Tree':
        return non_recursive_tree_copy(self)

    def __deepcopy__(self, memo=None) -> 'Tree':
        if memo is None:
            memo = {}
        return non_recursive_tree_deepcopy(self, memo)

    def bfs(self, reverse: bool = False, mirror: bool = False) -> Iterable['Tree']:
        """
        Breadth First Search
        :param reverse: reverse resulting order of nodes (require O(n) memory)
        :param mirror: used reversed children order on whole tree
        :return: nodes in requested order
        """
        if reverse:
            if mirror:
                return non_recursive_tree_bfs_reverse_mirror(self)
            else:
                return non_recursive_tree_bfs_reverse_original(self)
        else:
            if mirror:
                return non_recursive_tree_bfs_forward_mirror(self)
            else:
                return non_recursive_tree_bfs_forward_original(self)

    def bfs_ex(self, depth: Optional[int] = None, reverse: bool = False, mirror: bool = False) \
            -> Iterable[Tuple['Tree', int, Tuple[int, ...]]]:
        """
        Breadth First Search appended with nodes positions
        :param depth: limit search with max allowed depth
        :param reverse: reverse resulting order of nodes (require O(n) memory)
        :param mirror: used reversed children order on whole tree
        :return: nodes in requested order
        """
        if reverse:
            if mirror:
                return non_recursive_tree_bfs_reverse_mirror_ex(self, depth)
            else:
                return non_recursive_tree_bfs_reverse_original_ex(self, depth)
        else:
            if mirror:
                return non_recursive_tree_bfs_forward_mirror_ex(self, depth)
            else:
                return non_recursive_tree_bfs_forward_original_ex(self, depth)

    def dfs(self, reverse: bool = False, mirror: bool = False, post_order: bool = False) -> Iterable['Tree']:
        """
        Depth First Search
        :param reverse: reverse resulting order of nodes (require twice more time)
        :param mirror: used reversed children order on whole tree
        :param post_order: taking node on leaving (usually on entering)
        (require twice more time, incompatible with param `reverse`)
        :return: nodes in requested order
        """
        assert not (reverse and post_order), 'Param `post_order` incompatible with param `reverse`'
        if reverse:
            if mirror:
                return non_recursive_tree_dfs_reverse_mirror(self)
            else:
                return non_recursive_tree_dfs_reverse_original(self)
        elif post_order:
            if mirror:
                return non_recursive_tree_dfs_reverse_original(self)
            else:
                return non_recursive_tree_dfs_reverse_mirror(self)
        else:
            if mirror:
                return non_recursive_tree_dfs_forward_mirror(self)
            else:
                return non_recursive_tree_dfs_forward_original(self)

    def dfs_ex(self, depth: Optional[int] = None,
               reverse: bool = False, mirror: bool = False, post_order: bool = False) \
            -> Iterable[Tuple['Tree', int, Tuple[int, ...]]]:
        """
        Depth First Search appended with nodes positions
        :param depth: limit search with max allowed depth
        :param reverse: reverse resulting order of nodes (require twice more time)
        :param mirror: used reversed children order on whole tree
        :param post_order: taking node on leaving (usually on entering)
        (require twice more time, incompatible with param `reverse`)
        :return: nodes in requested order
        """
        assert not (reverse and post_order), 'Param `post_order` incompatible with param `reverse`'
        if reverse:
            if mirror:
                return non_recursive_tree_dfs_reverse_mirror_ex(self, depth)
            else:
                return non_recursive_tree_dfs_reverse_original_ex(self, depth)
        elif post_order:
            if mirror:
                return non_recursive_tree_dfs_reverse_original_ex(self, depth)
            else:
                return non_recursive_tree_dfs_reverse_mirror_ex(self, depth)
        else:
            if mirror:
                return non_recursive_tree_dfs_forward_mirror_ex(self, depth)
            else:
                return non_recursive_tree_dfs_forward_original_ex(self, depth)

    @classmethod
    def from_tuple(cls, itr: Tuple[Any, Iterable[Tuple]]) -> 'Tree':
        """
        Convert flat structure into Tree.
        :param itr: flat structure of tree
        :return: Tree with the same order of elements
        """
        return non_recursive_tree_from_tuple(itr)

    def to_tuple(self) -> Tuple[Any, Iterable[Tuple]]:
        """
        Convert Tree into flat structure.
        :return: flat structure with the same order of elements
        """
        return non_recursive_tree_to_tuple(self)


def indices_type_error(self: Tree, indices: object) -> str:
    return f'{type(self).__name__} indices must be int or tuple of int, not {type(indices).__name__}'


def immediate_return_routine(routine: Callable[..., Any], args: Tuple[Any, ...]) -> Any:
    try:
        return routine(*args)
    except AssertionError as err:
        if err.args and isinstance(err.args[0], ImmediateReturn):
            return err.args[0].retval
        raise


def non_recursive_tree_eq(self: Tree, other: object) -> bool:
    assert isinstance(other, Tree), ImmediateReturn(False)
    q = deque([(self, other)])
    while q:
        f, s = q.popleft()
        assert compare_nodes(f, s), ImmediateReturn(False)
        q.extend(zip(f._children, s._children))
    return True


def non_recursive_tree_hash(self: Tree) -> int:
    h = 0
    for t in self.dfs():
        h = hash((h, hash(t.value)))
    return h


def non_recursive_tree_copy(self: Tree) -> Tree:
    memo = {}
    t = Tree(self.value)
    memo[id(self)] = t
    q = deque(zip(self._children, repeat(t)))
    while q:
        ct, p = q.popleft()
        if id(ct) in memo:
            nt = memo[id(ct)]
        else:
            nt = Tree(ct.value)
        p.append(nt)
        q.extend(zip(ct._children, repeat(nt)))
    return t


def non_recursive_tree_deepcopy(self: Tree, memo=None) -> Tree:
    if memo is None:
        memo = {}
    t = Tree(deepcopy(self.value, memo))
    memo[id(self)] = t
    q = deque(zip(self._children, repeat(t)))
    while q:
        ct, p = q.popleft()
        if id(ct) in memo:
            nt = memo[id(ct)]
        else:
            nt = Tree(deepcopy(ct.value, memo))
        p.append(nt)
        q.extend(zip(ct._children, repeat(nt)))
    return t


def non_recursive_tree_str(self: Tree) -> str:
    s = ''
    p = -1
    q = deque([(self, 0)])
    while q:
        t, c = q.popleft()
        s += ')' * (p - c + 1) + ' (' + str(t.value)
        p = c
        q.extendleft(zip(reversed(t._children), repeat(c + 1)))
    return s[1:] + ')' * (p + 1)


def non_recursive_tree_repr(self: Tree) -> str:
    s = ''
    p = -1
    q = deque([(self, 0)])
    while q:
        t, c = q.popleft()
        s += ')),' * (p - c + 1) + f' Tree(value={repr(t.value)}, children=('
        p = c
        q.extendleft(zip(reversed(t._children), repeat(c + 1)))
    return s[1:] + (')),' * (p + 1))[:-1]


def non_recursive_tree_freeze(self: Tree) -> None:
    for t in self.dfs():
        t._is_frozen = True


def non_recursive_tree_unfreeze(self: Tree) -> None:
    for t in self.dfs():
        t._is_frozen = False
        t._hash = None
        t._size = None
        t._height = None


def non_recursive_tree_size(self: Tree) -> int:
    return sum(1 for _ in self.dfs())


def non_recursive_tree_height(self: Tree) -> int:
    h = 0
    q = deque([(self, 1)])
    while q:
        t, d = q.popleft()
        h = max(h, d)
        q.extend(zip(t._children, repeat(d + 1)))
    return h


def non_recursive_tree_from_tuple(itr: Tuple[Any, Iterable[Tuple]]) -> Tree:
    t = Tree(itr[0])
    q = deque(zip(itr[1], repeat(t)))
    while q:
        (d, i), p = q.popleft()
        nt = Tree(d)
        p.append(nt)
        q.extend(zip(i, repeat(nt)))
    return t


def non_recursive_tree_to_tuple(self: Tree) -> Tuple[Any, Iterable[Tuple]]:
    t: Tuple[Any, List[Tuple]] = (self.value, [])
    q = deque(zip(self._children, repeat(t[1])))
    while q:
        ct, l = q.popleft()
        nt: Tuple[Any, List[Tuple]] = (ct.value, [])
        l.append(nt)
        q.extend(zip(ct._children, repeat(nt[1])))
    return t


def dereference(t: Tree, ix: Tuple[int, ...]) -> Tree:
    for i in ix:
        t = t._children[i]
    return t


def non_recursive_tree_getitem(self: Tree, ix: Tuple[int, ...]) -> Tree:
    return dereference(self, ix)


def non_recursive_tree_setitem(self: Tree, ix: Tuple[int, ...], o: Tree) -> None:
    t = dereference(self, ix[:-1])
    t._children[ix[-1]] = o


def non_recursive_tree_delitem(self: Tree, ix: Tuple[int, ...]) -> None:
    t = dereference(self, ix[:-1])
    del t._children[ix[-1]]


def non_recursive_tree_insert(self: Tree, ix: Tuple[int, ...], o: Tree) -> None:
    t = dereference(self, ix[:-1])
    t._children.insert(ix[-1], o)


def compare_nodes(f: Tree, s: Tree) -> bool:
    return (f.value == s.value) and (len(f._children) == len(s._children))
