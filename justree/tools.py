from typing import Sequence, Iterable, Tuple, TypeVar, NamedTuple, Any, Callable

T = TypeVar('T')


class _ImmediateReturn(NamedTuple):
    retval: Any


def reversed_enumerate(seq: Sequence[T]) -> Iterable[Tuple[int, T]]:
    i = len(seq)
    for x in reversed(seq):
        i -= 1
        yield i, x


def immediate_return_routine(routine: Callable[..., Any], args: Tuple[Any, ...]) -> Any:
    try:
        return routine(*args)
    except AssertionError as err:
        if err.args and isinstance(err.args[0], _ImmediateReturn):
            return err.args[0].retval
        raise
