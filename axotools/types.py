from typing import Any, Callable, Sequence

type Aliases = Sequence[str]
type Returns[T] = Callable[..., T]
type Func = Returns[Any]