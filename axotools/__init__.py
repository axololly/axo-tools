from atexit import register as _after_end
from .commands import command # noqa
from .utils import error # noqa

@_after_end
def f():
    from .parser import parse

    parse()