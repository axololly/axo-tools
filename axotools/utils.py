from .types import Any, Func

def ret(value):
    def wrapper(self, *_):
        return value
    
    return wrapper


class _MissingType:
    __eq__ = __bool__ = ret(False)
    __hash__ = ret(0)
    __repr__ = ret("...")

MISSING: Any = _MissingType()


def silence_sys_exit(f: Func) -> Func:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            f(*args, **kwargs)
        except SystemExit:
            pass
    
    return wrapper


def error(message: str, exit_code: int = 1):
    def red(s: str) -> str:
        return f"\x1b[31m{s}\x1b[0m"

    print(red(f"ERROR: {message} (Exit code: {exit_code})"))
    
    exit(exit_code)