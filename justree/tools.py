from typing import Sequence, Iterable, Tuple, TypeVar

T = TypeVar('T')


def reversed_enumerate(seq: Sequence[T]) -> Iterable[Tuple[int, T]]:
    i = len(seq)
    for x in reversed(seq):
        i -= 1
        yield i, x
