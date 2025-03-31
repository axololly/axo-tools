from atexit import register as _after_end
from .commands import command, rename # noqa
from .utils import error # noqa

__author__ = 'axololly'
__version__ = '0.1.0'

@_after_end
def f():
    from .parser import parse

    parse()